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

__author__ = "Olof Svensson"
__contact__ = "svensson@esrf.eu"
__copyright__ = "ESRF"
__updated__ = "2022-02-13"

import os

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsLogging


logger = UtilsLogging.getLogger()


class DozorRD(AbstractTask):  # pylint: disable=too-many-instance-attributes
    """
    The DozorM2 is responsible for executing the 'dozorm2' program.
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "list_dozor_all": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "wavelength": {"type": "number"},
                "exposureTime": {"type": "number"},
                "numberOfImages": {"type": "number"},
            },
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "logPath": {"type": "string"},
                "noSpotDecrease": {"type": "number"},
                "mainScore": {"type": "number"},
                "spotIntensity": {"type": "number"},
                "sumIntensity": {"type": "number"},
                "average": {"type": "number"},
            },
        }

    def run(self, inData):
        outData = {}
        commandLine = "dozorrd dozorrd.dat"
        for index, dozor_all_file in enumerate(inData["list_dozor_all"]):
            os.symlink(
                dozor_all_file, str(self.getWorkingDirectory() / "d_00{0}".format(index + 1))
            )
        commands = self.generateCommands(inData)
        with open(str(self.getWorkingDirectory() / "dozorrd.dat"), "w") as f:
            f.write(commands)
        logPath = self.getWorkingDirectory() / "dozorrd.log"
        self.runCommandLine(commandLine, logPath=logPath)
        outData = self.parseDozorRDLogFile(logPath)
        outData["logPath"] = str(logPath)
        return outData

    @staticmethod
    def generateCommands(inData):
        """
        This method creates the input file for dozorm
        """
        nameTemplateScan = "d_0??"
        command = "X-ray_wavelength {0}\n".format(inData["wavelength"])
        command += "exposure {0}\n".format(inData["exposureTime"])
        command += "number_images {0}\n".format(inData["numberOfImages"])
        command += "first_scan_number 1\n"
        command += "number_scans {0}\n".format(len(inData["list_dozor_all"]))
        command += "name_template_scan {0}\n".format(nameTemplateScan)
        command += "end\n"
        return command

    @staticmethod
    def parseDozorRDLogFile(logPath):
        #  Program dozorrd /A.Popov,G.Bourenkov /
        #  Version 1.1 //  31.01.2022
        #  Copyright 2020 by Alexander Popov and Gleb Bourenkov
        #   T1/2 estimates
        #  N.of spot decrease= 1.751
        #       main score   =10.719
        #   spot intensity   =67.269
        #   sum  intensity   = 2.218
        #   average   =26.735
        with open(str(logPath)) as fd:
            listLogLines = fd.readlines()
        outData = {}
        for line in listLogLines:
            if "=" in line:
                key, value = line.split("=")
                if key.strip() == "N.of spot decrease":
                    outData["noSpotDecrease"] = float(value)
                elif key.strip() == "main score":
                    outData["mainScore"] = float(value)
                elif key.strip() == "spot intensity":
                    outData["spotIntensity"] = float(value)
                elif key.strip() == "sum  intensity":
                    outData["sumIntensity"] = float(value)
                elif key.strip() == "average":
                    outData["average"] = float(value)
        print(outData)
        return outData

