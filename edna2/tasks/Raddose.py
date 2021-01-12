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
__date__ = "11/01/2021"



from edna2.tasks.AbstractTask import AbstractTask




class Raddose(AbstractTask):
    """
    This task runs the program raddose
    """
    HENDERSON_LIMIT = 2e7

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "exposureTime": {"type": "number"},
                "flux": {"type": "number"},
                "beamSizeX": {"type": "number"},
                "beamSizeY": {"type": "number"},
                "wavelength": {"type": "number"},
                "numberOfImages": {"type": "number"},
            }
        }

    def run(self, inData):
        commandLine, listCommand = self.createCommandLine(inData)
        self.runCommandLine(commandLine, listCommand=listCommand)
        dictResults = self.parseLogFile(self.getLogPath())
        outData = self.createOutData(inData, dictResults, pathToLogFile=self.getLogPath())
        return outData

    @staticmethod
    def createCommandLine(inData):
        commandLine = "raddose__v20090103"
        listCommand = [
            "BEAM {beamSizeX} {beamSizeY}".format(**inData),
            "PHOSEC {flux}".format(**inData),
            "WAVELENGTH {wavelength}".format(**inData),
            "CRYSTAL {crystalSizeX} {crystalSizeY} {crystalSizeZ}".format(**inData),
            "NRES {crystalNRES}".format(**inData),
            "NMON {crystalNMON}".format(**inData),
            "CELL {a} {b} {c} {alpha} {beta} {gamma}".format(**inData["cell"]),
            "EXPOSURE {exposureTime}".format(**inData),
            "IMAGES {numberOfImages}".format(**inData),
        ]
        patmLine = "PATM"
        for patm in inData["crystalPATM"]:
            patmLine += " {symbol} {numberOf}".format(**patm)
        listCommand.append(patmLine)
        listCommand.append("END")
        return commandLine, listCommand

    @staticmethod
    def parseLogFile(logFilePath):
        dictResults = {}
        with open(str(logFilePath), "rb") as fd:
            content = fd.read()
        # Cut off the last 150 bytes
        content = content[0:len(content) - 150]
        for line in content.decode('utf-8').split("\n"):
            if "Dose in Grays" in line:
                dictResults["doseInGrays"] = float(line.split()[-1])
            elif "Total absorbed dose (Gy)" in line:
                dictResults["totalAbsorbedDose"] = float(line.split()[-1])
            elif "Solvent Content (%)" in line:
                dictResults["solventContent"] = float(line.split()[-1])
        return dictResults

    @staticmethod
    def createOutData(inData, dictResults, pathToLogFile=None):
        outData = {}
        numberOfImages = inData["numberOfImages"]
        exposureTime = inData["exposureTime"]
        totalExposureTime = numberOfImages * exposureTime
        if "doseInGrays" in dictResults:
            absorbedDose = dictResults["doseInGrays"]
        elif "totalAbsorbedDose" in dictResults:
            absorbedDose = dictResults["totalAbsorbedDose"]
        else:
            raise RuntimeError["Neither doseInGrays nor totalAbsorbedDose in results!"]
        absorbedDoseRate = absorbedDose / totalExposureTime
        timeToReachHendersonLimit = round(Raddose.HENDERSON_LIMIT / absorbedDoseRate, 1)
        outData = {
            "absorbedDose": absorbedDose,
            "absorbedDoseRate": absorbedDoseRate,
            "pathToLogFile": pathToLogFile,
            "timeToReachHendersonLimit": timeToReachHendersonLimit
        }
        return outData
