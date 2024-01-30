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
__date__ = "13/10/2023"

import os
import shlex
import subprocess
import threading


def run_command_line(command_line, timeout_sec=120):
    proc = subprocess.Popen(
        shlex.split(command_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    kill_proc = lambda p: p.kill()  # noqa E731
    timer = threading.Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        binaryStdout, binaryStderr = proc.communicate()
        stdout = binaryStdout.decode("utf-8")
        stderr = binaryStderr.decode("utf-8")
    finally:
        timer.cancel()
    return stdout, stderr


def parse_salloc_stderr(stderr):
    job_id = None
    list_lines = stderr.split("\n")
    for line in list_lines:
        if line.startswith("salloc: Granted job allocation"):
            job_id = int(line.split(" ")[-1])
            break
    return job_id


def salloc(partition, exclusive=False):
    timeout_sec = 100
    salloc_command_line = f"salloc --no-shell -p {partition}"
    if exclusive:
        salloc_command_line += " --exclusive"
    stdout, stderr = run_command_line(salloc_command_line, timeout_sec)
    job_id = parse_salloc_stderr(stderr)
    if job_id is None:
        print(stdout)
        print(stderr)
    return job_id


def srun(job_id, command):
    timeout_sec = 10
    srun_command_line = f"srun --jobid {job_id} {command}"
    stdout, stderr = run_command_line(srun_command_line, timeout_sec)
    return stdout, stderr


def scancel(job_id):
    timeout_sec = 10
    scancel_command_line = f"scancel {job_id}"
    stdout, stderr = run_command_line(scancel_command_line, timeout_sec)


def submit_job_to_slurm(
    command_line,
    working_directory,
    nodes=1,
    core=4,
    time="2:00:00",
    host=None,
    queue="mx",
    name=None,
    mem=None,
):
    slurm_id = None
    script = "#!/bin/bash\n"
    if name is not None:
        script += '#SBATCH --job-name="{0}"\n'.format(name)
    script += "#SBATCH --partition={0}\n".format(queue)
    if mem is None:
        mem = 8000  # 8 Gb memory by default
    script += "#SBATCH --mem={0}\n".format(mem)
    script += "#SBATCH --ntasks={0}\n".format(nodes)
    script += "#SBATCH --nodes=1\n"  # Necessary for not splitting jobs! See ATF-57
    script += "#SBATCH --cpus-per-task={0}\n".format(core)
    script += "#SBATCH --time={0}\n".format(time)
    script += "#SBATCH --output={0}/stdout.txt\n".format(working_directory)
    script += "#SBATCH --error={0}/stderr.txt\n".format(working_directory)
    script += command_line + "\n"
    script_name = "slurm.sh"
    slurm_script_path = os.path.join(working_directory, script_name)
    with open(slurm_script_path, "w") as f:
        f.write(script)
    stdout, stderr = run_command_line("sbatch {0}".format(slurm_script_path))
    if "Submitted batch job" in stdout:
        slurm_id = int(stdout.split("job")[1])
    return slurm_script_path, slurm_id, stdout, stderr


def split_at_equal(line, dict_line={}):
    if "=" in line:
        key, value = line.split("=", 1)
        if "=" in value:
            if " " in value:
                part1, part2 = value.split(" ", 1)
            elif "," in value:
                part1, part2 = value.split(",", 1)
            dict_line[key.strip()] = part1.strip()
            dict_line = split_at_equal(part2, dict_line=dict_line)
        else:
            dict_line[key.strip()] = value.strip()
    return dict_line


def parse_slurm_stat(slurmStat):
    list_lines = slurmStat.split("\n")
    dict_slurm_stat = {}
    for line in list_lines:
        if line != "":
            dictLine = split_at_equal(line)
            dict_slurm_stat.update(dictLine)
    return dict_slurm_stat


def get_slurm_stat(slurm_job_id):
    dict_stat = None
    stdout, stderr = run_command_line("scontrol show job {0}".format(slurm_job_id))
    if stderr is None or stderr == "":
        dict_stat = parse_slurm_stat(stdout)
    return dict_stat


def are_jobs_pending(partition_name=None):
    jobs_are_pending = False
    if partition_name is not None:
        stdout, stderr = run_command_line(
            "squeue -p {0} -t PENDING".format(partition_name)
        )
    else:
        stdout, stderr = run_command_line("squeue -t PENDING")
    list_lines = stdout.split("\n")
    no_pending = 0
    for line in list_lines:
        if "Resources" in line or "Priority" in line:
            no_pending += 1
    if no_pending > 2:
        jobs_are_pending = True
    return jobs_are_pending
