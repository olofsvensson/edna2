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
__date__ = "23/11/2020"



from edna2.tasks.AbstractTask import AbstractTask

# aimedCompleteness : XSDataDouble optional
# aimedIOverSigma : XSDataDouble optional
# aimedRedundancy : XSDataDouble optional
# aimedResolution : XSDataDouble optional
# anomalousData : XSDataBoolean optional
# beamExposureTime : XSDataTime
# beamMaxExposureTime : XSDataTime optional
# beamMinExposureTime : XSDataTime optional
# bestFileContentDat : XSDataString
# bestFileContentHKL : XSDataString []
# bestFileContentPar : XSDataString
# complexity : XSDataString optional
# crystalAbsorbedDoseRate : XSDataAbsorbedDoseRate optional
# crystalShape : XSDataDouble optional
# crystalSusceptibility : XSDataDouble optional
# detectorDistanceMax : XSDataLength optional
# detectorDistanceMin : XSDataLength optional
# detectorType : XSDataString
# doseLimit : XSDataDouble optional
# goniostatMaxRotationSpeed : XSDataAngularSpeed optional
# goniostatMinRotationWidth : XSDataAngle optional
# minTransmission : XSDataDouble optional
# numberOfCrystalPositions : XSDataInteger optional
# radiationDamageModelBeta : XSDataDouble optional
# radiationDamageModelGamma : XSDataDouble optional
# rFriedel : XSDataDouble optional
# strategyOption : XSDataString optional
# transmission : XSDataDouble optional
# userDefinedRotationRange : XSDataAngle optional
# userDefinedRotationStart : XSDataAngle optional
# xdsBackgroundImage : XSDataFile optional
# xdsCorrectLp : XSDataFile optional
# xdsBkgpixCbf : XSDataFile optional
# xdsAsciiHkl : XSDataFile [] optional



class Best(AbstractTask):
    """
    This task runs the program BEST
    http://www.embl-hamburg.de/BEST
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "aimedCompleteness": { "type": "number" },
                "aimedIOverSigma": { "type": "number" },
                "aimedRedundancy": { "type": "number" },
                "aimedResolution": { "type": "number" },
                "anomalousData": { "type": "number" },
                "beamExposureTime": { "type": "number" },
                "beamMaxExposureTime": { "type": "number" },
                "beamMinExposureTime": { "type": "number" },
                "complexity": { "type": "string" },
                "crystalAbsorbedDoseRate": { "type": "number" },
                "crystalShape": { "type": "number" },
                "crystalSusceptibility": { "type": "number" },
                "detectorDistanceMax": { "type": "number" },
                "detectorDistanceMin": { "type": "number" },
                "detectorType": { "type": "string" },
                "doseLimit": { "type": "number" },
                "goniostatMaxRotationSpeed": { "type": "number" },
                "goniostatMinRotationWidth": { "type": "number" },
                "minTransmission": { "type": "number" },
                "numberOfCrystalPositions": { "type": "integer" },
                "radiationDamageModelBeta": { "type": "number" },
                "radiationDamageModelGamma": { "type": "number" },
                "rFriedel": { "type": "number" },
                "strategyOption": { "type": "string" },
                "transmission": { "type": "number" },
                "userDefinedRotationRange": { "type": "number" },
                "userDefinedRotationStart": { "type": "number" },
                "xdsBackgroundImage": { "type": "string" },
                "xdsCorrectLp": { "type": "string" },
                "xdsBkgpixCbf": { "type": "string" },
                "xdsAsciiHkl": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    }
                }
            }
        }

    def run(self, inData):
        commandLine = self.createBestCommandLine(inData)
        self.runCommandLine(commandLine, listCommand=[])
        outData = {}
        return outData

    @staticmethod
    def createBestCommandLine(inData):
        firstSubWedge = inData["subWedge"][0]
        experimentalCondition = firstSubWedge["experimentalCondition"]
        detector = experimentalCondition["detector"]
        beam = experimentalCondition["beam"]
        commandLine = "best__v4.1.1_test_20201220"
        # Detector
        detectorType = detector["type"]
        commandLine += " -f " + detectorType
        # Exposure time
        exposureTime = beam["exposureTime"]
        commandLine += " -t " + str(exposureTime)
        # Integration data
        # commandLine += " -xds " + inData["bkgpixCbf"]
        # commandLine += " " + inData["correctLp"]
        commandLine += " -xds " + inData["bkgpixCbf"]
        for xdsAsciiHklPath in inData["xdsAsciiHkl"]:
            commandLine += " " + xdsAsciiHklPath
        # fExposureTime = self.dataInput.beamExposureTime.value
        # fMaxExposureTime = self.dataInput.beamMaxExposureTime.value
        #
        # self.strCommandBest = "-f " + strDetectorName + " " + "-t " + str(fExposureTime) + " "
        #
        # # Add output of gle files only if version is 4.1.0 (or higher)
        # if self.bVersionHigherThan4_0:
        #     self.strCommandBest = self.strCommandBest + "-g "
        #
        # if self.dataInput.beamMinExposureTime is not None:
        #     strBeamMinExposureTime = str(self.dataInput.beamMinExposureTime.value)
        #     self.strCommandBest = self.strCommandBest + "-M " + strBeamMinExposureTime + " "
        #
        # if self.dataInput.goniostatMaxRotationSpeed is not None:
        #     strGoniostatMaxRotationSpeed = str(self.dataInput.goniostatMaxRotationSpeed.value)
        #     self.strCommandBest = self.strCommandBest + "-S " + strGoniostatMaxRotationSpeed + " "
        #
        # if self.dataInput.goniostatMinRotationWidth is not None:
        #     strGoniostatMinRotationWidth = str(self.dataInput.goniostatMinRotationWidth.value)
        #     self.strCommandBest = self.strCommandBest + "-w " + strGoniostatMinRotationWidth + " "
        #
        # if self.dataInput.aimedResolution is not None:
        #     strAimedResolution = str(self.dataInput.aimedResolution.value)
        #     self.strCommandBest = self.strCommandBest + "-r " + strAimedResolution + " "
        #
        # if (self.dataInput.userDefinedRotationStart is not None) and \
        #    (self.dataInput.userDefinedRotationRange is not None):
        #     self.strCommandBest += " -phi {0} {1} ".format(self.dataInput.userDefinedRotationStart.value,
        #                                                   self.dataInput.userDefinedRotationRange.value)
        #     if self.dataInput.aimedRedundancy is not None:
        #         self.warning("Aimed redundancy of {0} igored as the oscillation range has been specified.".format(self.dataInput.aimedRedundancy.value))
        # elif self.dataInput.aimedRedundancy is not None:
        #     strAimedRedundancy = str(self.dataInput.aimedRedundancy.value)
        #     self.strCommandBest = self.strCommandBest + "-R " + strAimedRedundancy + " "
        #
        # if self.dataInput.aimedCompleteness is not None:
        #     strAimedCompleteness = str(self.dataInput.aimedCompleteness.value)
        #     self.strCommandBest = self.strCommandBest + "-C " + strAimedCompleteness + " "
        #
        # if self.dataInput.aimedIOverSigma is not None:
        #     strAimedIOverSigma = str(self.dataInput.aimedIOverSigma.value)
        #     self.strCommandBest = self.strCommandBest + "-i2s " + strAimedIOverSigma + " "
        #
        # if self.dataInput.crystalAbsorbedDoseRate is not None:
        #     strCrystalAbsorbedDoseRate = str(self.dataInput.crystalAbsorbedDoseRate.value)
        #     self.strCommandBest = self.strCommandBest + "-GpS " + strCrystalAbsorbedDoseRate + " "
        #
        # if self.dataInput.crystalShape is not None:
        #     strCrystalShape = str(self.dataInput.crystalShape.value)
        #     self.strCommandBest = self.strCommandBest + "-sh " + strCrystalShape + " "
        #
        # if self.dataInput.crystalSusceptibility is not None:
        #     strCrystalSusceptibility = str(self.dataInput.crystalSusceptibility.value)
        #     self.strCommandBest = self.strCommandBest + "-su " + strCrystalSusceptibility + " "
        #
        # if self.dataInput.transmission is not None:
        #     strTransmission = str(self.dataInput.transmission.value)
        #     self.strCommandBest = self.strCommandBest + "-Trans " + strTransmission + " "
        #
        # if self.dataInput.minTransmission is not None:
        #     strMinTransmission = str(self.dataInput.minTransmission.value)
        #     self.strCommandBest = self.strCommandBest + "-TRmin " + strMinTransmission + " "
        #
        # if self.dataInput.numberOfCrystalPositions is not None:
        #     iNumberOfCrystalPositions = str(self.dataInput.numberOfCrystalPositions.value)
        #     self.strCommandBest = self.strCommandBest + "-Npos " + iNumberOfCrystalPositions + " "
        #
        #
        # if self.dataInput.detectorDistanceMin is not None:
        #     fDetectorDistanceMin = str(self.dataInput.detectorDistanceMin.value)
        #     self.strCommandBest = self.strCommandBest + "-DIS_MIN " + fDetectorDistanceMin + " "
        #
        #
        # if self.dataInput.detectorDistanceMax is not None:
        #     fDetectorDistanceMax = str(self.dataInput.detectorDistanceMax.value)
        #     self.strCommandBest = self.strCommandBest + "-DIS_MAX " + fDetectorDistanceMax + " "
        #
        #
        # if self.dataInput.anomalousData is not None:
        #     bAnomalousData = self.dataInput.anomalousData.value
        #     if bAnomalousData:
        #         if self.dataInput.numberOfCrystalPositions is not None:
        #             self.strCommandBest = self.strCommandBest + "-a -p 0 360 "
        #         elif self.dataInput.crystalAbsorbedDoseRate is not None:
        #             self.strCommandBest = self.strCommandBest + "-asad "
        #         else:
        #             self.strCommandBest = self.strCommandBest + "-a "
        #
        # strStrategyOption = self.dataInput.strategyOption
        # if strStrategyOption is not None:
        #     self.strCommandBest = self.strCommandBest + "%s " % strStrategyOption.value
        #
        # if self.dataInput.getRadiationDamageModelBeta() is not None:
        #     fRadiationDamageModelBeta = str(self.dataInput.getRadiationDamageModelBeta().value)
        #     self.strCommandBest = self.strCommandBest + "-beta " + fRadiationDamageModelBeta + " "
        #
        # if self.dataInput.getRadiationDamageModelGamma() is not None:
        #     fRadiationDamageModelGamma = str(self.dataInput.getRadiationDamageModelGamma().value)
        #     self.strCommandBest = self.strCommandBest + "-gama " + fRadiationDamageModelGamma + " "
        #
        # if self.dataInput.doseLimit is not None:
        #     self.strCommandBest += " -DMAX {0} ".format(self.dataInput.doseLimit.value)
        #
        # if self.dataInput.rFriedel is not None:
        #     self.strCommandBest += " -Rf {0} ".format(self.dataInput.rFriedel.value)
        #
        # self.strCommandBest = self.strCommandBest + "-T " + str(fMaxExposureTime) + " " + \
        #                              "-dna " + self.getScriptBaseName() + "_dnaTables.xml" + " " + \
        #                              "-o " + os.path.join(self.getWorkingDirectory(), self.getScriptBaseName() + "_plots.mtv ") + \
        #                              "-e " + self.strComplexity + " "
        #
        # if self.dataInput.xdsBackgroundImage is not None:
        #     strPathToXdsBackgroundImage = self.dataInput.getXdsBackgroundImage().getPath().value
        #     self.strCommandBest = self.strCommandBest + "-MXDS " + self.getFileBestPar() + " " + strPathToXdsBackgroundImage + " " + listFileBestHKLCommand
        # elif self.dataInput.bestFileContentPar is not None:
        #     self.strCommandBest = self.strCommandBest + "-mos " + self.getFileBestDat() + " " + self.getFileBestPar() + " " + listFileBestHKLCommand
        # elif self.dataInput.xdsCorrectLp is not None:
        #     self.strCommandBest = self.strCommandBest + "-xds " + self.strPathToCorrectLp + " " + self.strPathToBkgpixCbf + " " + self.strListFileXdsAsciiHkl
        #
        #
        # self.setScriptCommandline(self.strCommandBest)
        return commandLine