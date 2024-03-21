#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "21/04/2019"

import os
import sys
import json
import pathlib

import billiard
import traceback
import jsonschema
import subprocess

from edna2.utils import UtilsPath
from edna2.utils import UtilsSlurm
from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


class EDNA2Process(billiard.Process):
    """
    See https://stackoverflow.com/a/33599967.
    """

    def __init__(self, *args, **kwargs):
        billiard.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = billiard.Pipe()
        self._exception = None

    def run(self):
        try:
            billiard.Process.run(self)
            self._cconn.send(None)
        except BaseException as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


class AbstractTask:  # noqa R0904
    """
    Parent task to all EDNA2 tasks.
    """

    def __init__(self, inData, workingDirectorySuffix=None):
        self._dictInOut = billiard.Manager().dict()
        self._dictInOut["inData"] = json.dumps(inData, default=str)
        self._dictInOut["outData"] = json.dumps({})
        self._dictInOut["isFailure"] = False
        self._process = EDNA2Process(target=self.executeRun, args=())
        self._workingDirectorySuffix = workingDirectorySuffix
        self._workingDirectory = None
        self._logFileName = None
        self._errorLogFileName = None
        self._schemaPath = pathlib.Path(__file__).parents[1] / "schema"
        self._persistInOutData = True
        self._oldDir = os.getcwd()

    def getSchemaUrl(self, schemaName):
        return "file://" + str(self._schemaPath / schemaName)

    def executeRun(self):
        inData = self.getInData()
        hasValidInDataSchema = False
        hasValidOutDataSchema = False
        if self.getInDataSchema() is not None:
            instance = inData
            schema = self.getInDataSchema()
            try:
                jsonschema.validate(instance=instance, schema=schema)
                hasValidInDataSchema = True
            except Exception as e:
                logger.exception(e)
        else:
            hasValidInDataSchema = True
        if hasValidInDataSchema:
            self._workingDirectory = UtilsPath.getWorkingDirectory(
                self, inData, workingDirectorySuffix=self._workingDirectorySuffix
            )
            self.writeInputData(inData)
            self._oldDir = os.getcwd()
            os.chdir(str(self._workingDirectory))
            outData = self.run(inData)
            os.chdir(self._oldDir)
        else:
            raise RuntimeError("Schema validation error for inData")
        if self.getOutDataSchema() is not None:
            instance = outData
            schema = self.getOutDataSchema()
            try:
                jsonschema.validate(instance=instance, schema=schema)
                hasValidOutDataSchema = True
            except Exception as e:
                logger.exception(e)
        else:
            hasValidOutDataSchema = True
        if hasValidOutDataSchema:
            self.writeOutputData(outData)
        else:
            raise RuntimeError("Schema validation error for outData")
        if not os.listdir(str(self._workingDirectory)):
            os.rmdir(str(self._workingDirectory))

    def getInData(self):
        return json.loads(self._dictInOut["inData"])

    def setInData(self, inData):
        self._dictInOut["inData"] = json.dumps(inData, default=str)

    inData = property(getInData, setInData)

    def getOutData(self):
        return json.loads(self._dictInOut["outData"])

    def setOutData(self, outData):
        self._dictInOut["outData"] = json.dumps(outData, default=str)

    outData = property(getOutData, setOutData)

    def writeInputData(self, inData):
        # Write input data
        if self._persistInOutData and self._workingDirectory is not None:
            jsonName = "inData" + self.__class__.__name__ + ".json"
            with open(str(self._workingDirectory / jsonName), "w") as f:
                f.write(json.dumps(inData, default=str, indent=4))

    def writeOutputData(self, outData):
        self.setOutData(outData)
        if self._persistInOutData and self._workingDirectory is not None:
            jsonName = "outData" + self.__class__.__name__ + ".json"
            with open(str(self._workingDirectory / jsonName), "w") as f:
                f.write(json.dumps(outData, default=str, indent=4))

    def getLogPath(self):
        if self._logFileName is None:
            self._logFileName = self.__class__.__name__ + ".log.txt"
        logPath = self._workingDirectory / self._logFileName
        return logPath

    def setLogFileName(self, logFileName):
        self._logFileName = logFileName

    def getLogFileName(self):
        return self._logFileName

    def getErrorLogPath(self):
        if self._errorLogFileName is None:
            self._errorLogFileName = self.__class__.__name__ + ".error.txt"
        errorLogPath = self._workingDirectory / self._errorLogFileName
        return errorLogPath

    def setErrorLogFileName(self, errorLogFileName):
        self._errorLogFileName = errorLogFileName

    def getErrorLogFileName(self):
        return self._errorLogFileName

    def getLog(self):
        with open(str(self.getLogPath())) as f:
            log = f.read()
        return log

    def getErrorLog(self):
        with open(str(self.getErrorLogPath())) as f:
            errorLog = f.read()
        return errorLog

    def submit(
        self,
        command_line,
        job_name,
        partition,
        log_path,
        error_path,
        ignore_errors,
        no_cores=10,
    ):
        working_dir = str(self._workingDirectory)
        if working_dir.startswith("/mntdirect/_users"):
            working_dir = working_dir.replace("/mntdirect/_users", "/home/esrf")
        nodes = 1
        time = "1:00:00"
        mem = 16000  # 16 Gb memory by default
        script = "#!/bin/bash\n"
        script += '#SBATCH --job-name="{0}"\n'.format(job_name)
        if partition is None:
            partition = "mx"
        else:
            partition = "{0}".format(partition)
        script += "#SBATCH --partition={0}\n".format(partition)
        script += "#SBATCH --mem={0}\n".format(mem)
        script += "#SBATCH --nodes={0}\n".format(nodes)
        script += "#SBATCH --cpus-per-task={0}\n".format(no_cores)
        script += "#SBATCH --time={0}\n".format(time)
        script += "#SBATCH --chdir={0}\n".format(working_dir)
        script += f"#SBATCH --output={log_path}\n"
        script += f"#SBATCH --error={error_path}\n"
        script += command_line + "\n"
        shellFile = self._workingDirectory / (job_name + "_slurm.sh")
        with open(str(shellFile), "w") as f:
            f.write(script)
            f.close()
        shellFile.chmod(0o755)
        slurmCommandLine = "sbatch --wait {0}".format(shellFile)
        pipes = subprocess.Popen(
            slurmCommandLine,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            cwd=str(self._workingDirectory),
        )
        stdout, stderr = pipes.communicate()
        slurmLogPath = self._workingDirectory / (job_name + "_slurm.log")
        slurmErrorLogPath = self._workingDirectory / (job_name + "_slurm.error.log")
        if len(stdout) > 0:
            log = str(stdout, "utf-8")
            with open(str(slurmLogPath), "w") as f:
                f.write(log)
        if len(stderr) > 0:
            if not ignore_errors:
                logger.warning(
                    "Error messages from command {0}".format(command_line.split(" ")[0])
                )
            with open(str(slurmErrorLogPath), "w") as f:
                f.write(str(stderr, "utf-8"))
        if pipes.returncode != 0:
            # Error!
            warningMessage = "{0}, code {1}".format(stderr, pipes.returncode)
            logger.warning(warningMessage)
            # raise RuntimeError(errorMessage)

    def runCommandLine(
        self,
        command_line,
        log_path=None,
        list_command=None,
        ignore_errors=False,
        do_submit=False,
        partition=None,
        no_cores=None,
    ):
        if log_path is None:
            log_path = self.getLogPath()
        job_name = self.__class__.__name__
        log_file_name = os.path.basename(log_path)
        error_log_path = self.getErrorLogPath()
        error_log_file_name = os.path.basename(error_log_path)
        if list_command is not None:
            if do_submit:
                command_line += " << EOF-EDNA2\n"
            else:
                command_line += (
                    f" 1>{log_file_name} 2>{error_log_file_name} << EOF-EDNA2\n"
                )
            for command in list_command:
                command_line += command + "\n"
            command_line += "EOF-EDNA2"
        elif not do_submit:
            command_line += f" 1>{log_file_name} 2>{error_log_file_name}\n"
        if do_submit:
            self.submit(
                command_line=command_line,
                job_name=job_name,
                partition=partition,
                log_path=log_path,
                error_path=error_log_path,
                ignore_errors=ignore_errors,
                no_cores=no_cores,
            )
        else:
            script_file_name = job_name + ".sh"
            script_path = self._workingDirectory / script_file_name
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(command_line + "\n")
            script_path.chmod(0o755)
            result = subprocess.run(
                str(script_path), shell=True, capture_output=True, text=True
            )
            if len(result.stdout) > 0:
                with open(str(log_path), "w") as f:
                    f.write(result.stdout)
            if len(result.stderr) > 0:
                if not ignore_errors:
                    logger.warning(
                        "Error messages from command {0}".format(
                            command_line.split(" ")[0]
                        )
                    )
                error_log_path = self._workingDirectory / error_log_file_name
                with open(str(error_log_path), "w") as f:
                    f.write(result.stderr)
            if result.returncode != 0:
                # Error!
                errorMessage = "{0}, code {1}".format(result.stderr, result.returncode)
                raise RuntimeError(errorMessage)

    def onError(self):
        pass

    def start(self):
        self._process.start()

    def join(self):
        self._process.join()
        if self._process.exception:
            error, trace = self._process.exception
            logger.error(error)
            logger.error(trace)
            self._dictInOut["isFailure"] = True
            self.onError()

    def execute(self):
        self.start()
        self.join()

    def setFailure(self):
        self._dictInOut["isFailure"] = True

    def isFailure(self):
        return self._dictInOut["isFailure"]

    def isSuccess(self):
        return not self.isFailure()

    def getWorkingDirectory(self):
        return self._workingDirectory

    def setWorkingDirectory(self, inData):
        self._workingDirectory = UtilsPath.getWorkingDirectory(self, inData)

    def getInDataSchema(self):
        return None

    def getOutDataSchema(self):
        return None

    def setPersistInOutData(self, value):
        self._persistInOutData = value

    @classmethod
    def launch_on_slurm(
        cls, working_dir, in_data, partition, no_cores=1, environment=None
    ):
        # Save input data
        edna2_module_name = cls.__module__
        edna2_task_name = cls.__name__
        input_path = working_dir / f"{edna2_task_name}.json"
        with open(input_path, "w") as f:
            f.write(json.dumps(in_data, indent=4))
        # Prepare script
        python_intepreter = sys.executable
        script = f"#!{python_intepreter}\n"
        script += "import os\n"
        script += "import json\n"
        script += "from edna2.utils import UtilsLogging\n"
        script += f"from {edna2_module_name} import {edna2_task_name}\n"
        script += "\n"
        script += f'os.chdir("{working_dir}")\n'
        script += "\n"
        script += "# Remove start and end file if existing\n"
        script += f'start_file = "{working_dir}/STARTED"\n'
        script += f'finish_file = "{working_dir}/FINISHED"\n'
        script += "if os.path.exists(start_file):\n"
        script += "    os.remove(start_file)\n"
        script += "if os.path.exists(finish_file):\n"
        script += "    os.remove(finish_file)\n"
        script += "\n"
        for key, value in environment.items():
            script += f'os.environ["{key}"] = "{value}"\n'
        script += "\n"
        script += "# Set up local logging\n"
        script += "logger = UtilsLogging.getLogger()\n"
        script += f'UtilsLogging.addFileHandler(logger, "{working_dir}/{edna2_task_name}_log_DATETIME.txt")\n'

        script += f'in_data = json.loads(open("{input_path}").read())\n'
        script += f"task = {edna2_task_name}(inData=in_data)\n"

        script += f'print("Start of execution of EDNA2 task {edna2_task_name}")\n'
        script += 'open(start_file, "w").write("Started")\n'
        script += "task.execute()\n"
        script += 'open(finish_file, "w").write("Finished")\n'
        script_path = working_dir / f"{edna2_task_name}.py"
        with open(f"{script_path}", "w") as f:
            f.write(script)
        script_path.chmod(0o755)
        slurm_script_path, slurm_id, stdout, stderr = UtilsSlurm.submit_job_to_slurm(
            command_line=str(script_path),
            working_directory=str(working_dir),
            nodes=1,
            core=4,
            time="2:00:00",
            host=None,
            queue="mx",
            name=edna2_task_name,
            mem=None,
        )
        return slurm_script_path, slurm_id, stdout, stderr
