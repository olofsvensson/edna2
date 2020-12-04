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

import os
import numpy
import pprint

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsLogging
from edna2.utils import UtilsDetector


logger = UtilsLogging.getLogger()

class DozorM(AbstractTask):  # pylint: disable=too-many-instance-attributes
    """
    The DozorM is responsible for executing the 'dozorm' program.
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                # "listDozorAllFile": {
                #     "type": "array",
                #     "items": {"type": "string"},
                # },
                "name_template_scan": {"type": "string"},
                "detectorType": {"type": "string"},
                "beamline": {"type": "string"},
                "detector_distance": {"type": "number"},
                "wavelength": {"type": "number"},
                "orgx": {"type": "number"},
                "orgy": {"type": "number"},
                "number_row": {"type": "number"},
                "number_images": {"type": "number"},
                "isZigZag": {"type": "boolean"},
                "step_h": {"type": "number"},
                "step_v": {"type": "number"},
                "beam_shape": {"type": "string"},
                "beam_h": {"type": "number"},
                "beam_v": {"type": "number"},
                "number_apertures": {"type": "integer"},
                "aperture_size": {"type": "string"},
                "reject_level": {"type": "integer"}
            }
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "dozorMap": {"type": "string"},
                "listPositions":  {
                    "type": "array",
                    "items": {"type": "object"}
                },
            },
        }

    def run(self, inData):
        outData = {}
        commands = self.generateCommands(inData)
        with open(str(self.getWorkingDirectory() / 'dozorm.dat'), 'w') as f:
            f.write(commands)
        commandLine = "dozorm dozorm.dat"
        logPath = self.getWorkingDirectory() / 'dozorm.log'
        self.runCommandLine(commandLine, logPath=logPath)
        outData = self.parseOutput(self.getWorkingDirectory(), logPath)
        return outData

    def generateCommands(self, inData):
        """
        This method creates the input file for dozorm
        """
        detectorType = inData['detectorType']
        nx = UtilsDetector.getNx(detectorType)
        ny = UtilsDetector.getNy(detectorType)
        pixelSize = UtilsDetector.getPixelsize(detectorType)
        if inData.get('isZigZag', False):
            mesh_direct = "-h"
        else:
            mesh_direct = "-h"
        nameTemplateScan = self.getWorkingDirectory() / "dozorm_00?"
        os.symlink(inData["dozorAllFile"], str(self.getWorkingDirectory() / "dozorm_001"))
        firstScanNumber = 1
        command = '!\n'
        command += 'detector {0}\n'.format(detectorType)
        command += 'nx %d\n' % nx
        command += 'ny %d\n' % ny
        command += 'pixel %f\n' % pixelSize
        command += 'detector_distance {0}\n'.format(inData['detector_distance'])
        command += 'X-ray_wavelength {0}\n'.format(inData['wavelength'])
        command += 'orgx {0}\n'.format(inData['orgx'])
        command += 'orgy {0}\n'.format(inData['orgy'])
        command += 'number_row {0}\n'.format(inData['number_row'])
        command += 'number_images {0}\n'.format(inData['number_images'])
        command += 'mesh_direct {0}\n'.format(mesh_direct)
        command += 'step_h {0}\n'.format(inData['step_h'])
        command += 'step_v {0}\n'.format(inData['step_v'])
        command += 'beam_shape {0}\n'.format(inData['beam_shape'])
        command += 'beam_h {0}\n'.format(inData['beam_h'])
        command += 'beam_v {0}\n'.format(inData['beam_v'])
        command += 'number_apertures {0}\n'.format(inData['number_apertures'])
        command += 'aperture_size {0}\n'.format(inData['aperture_size'])
        command += 'reject_level {0}\n'.format(inData['reject_level'])
        command += 'name_template_scan {0}\n'.format(nameTemplateScan)
        command += 'number_scans {0}\n'.format(inData['number_scans'])
        command += 'first_scan_number {0}\n'.format(firstScanNumber)
        command += 'end\n'
        # logger.debug('command: {0}'.format(command))
        return command

    @staticmethod
    def parseOutput(workingDir, logPath):
        outData = {}
        pathDozormMap = workingDir / "dozorm_001.map"
        if pathDozormMap.exists():
            listPositions = DozorM.parseDozormLogFile(logPath)
            arrayScore, arrayCrystal, arrayImageNumber = \
                DozorM.parseMap(pathDozormMap)
            outData = {
                "dozorMap": str(pathDozormMap),
                "listPositions": listPositions,
                "arrayScore": arrayScore,
                "arrayCrystal": arrayCrystal,
                "arrayImageNumber": arrayImageNumber
            }
        return outData

    @staticmethod
    def parseDozormLogFile(logPath):
        listPositions = []
        #    Total N.of crystals in Loop =  2
        # Cryst Aperture Central  Coordinate    Int/Sig N.of Images Score  Helic   Start     Finish   Int/Sig
        # number size     image      X    Y            All dX dY    sum           x     y     x    y   helical
        # --------------------------------------------------------------------------------------------------
        #     1   100.0     260    8.1   15.1  545.7  12   3   5  1242.5   NO
        #     2   100.0      82    9.9    5.0  354.0   7   3   3   670.6   NO
        #     3    10.0     183    2.7   10.8   31.2   3   2   2   169.1   NO
        #     4    10.0     170   10.8    9.7   26.7   3   2   3   128.6  YES    11    10    12    11   100.7

        with open(str(logPath)) as fd:
            listLogLines = fd.readlines()
        doParseLine = False
        for line in listLogLines:
            if line.startswith("------"):
                doParseLine = True
            elif doParseLine:
                listValues = line.split()
                position = {
                    "number": int(listValues[0]),
                    "apertureSize": float(listValues[1]),
                    "imageNumber": int(listValues[2]),
                    "xPosition": float(listValues[3]),
                    "yPosition": float(listValues[4]),
                    "iOverSigma": float(listValues[5]),
                    "numberOfImagesTotal": int(listValues[6]),
                    "numberOfImagesTotalX": int(listValues[7]),
                    "numberOfImagesTotalY": int(listValues[8]),
                    "score": float(listValues[9]),
                    "helical": listValues[10] == 'YES'
                }
                if position["helical"]:
                    position["helicalStartX"] = listValues[11]
                    position["helicalStartY"] = listValues[12]
                    position["helicalStopX"] = listValues[13]
                    position["helicalStopY"] = listValues[14]
                    position["helicalIoverSigma"] = listValues[15]
                listPositions.append(position)
        return listPositions

    @staticmethod
    def makePlots(mapPath):
        heatMapPath = None
        crystalMapPath = None
        npArrayScores, npArrayCrystal = DozorM.parseMap(mapPath)

        return heatMapPath, crystalMapPath

    @staticmethod
    def parseMatrix(index, listLines, isFloat=True):
        arrayValues = []
        # Parse matrix - starts and ends with "---" line
        while not listLines[index].startswith("-------"):
            index += 1
        index += 1
        while not listLines[index].startswith("-------"):
            listScores = listLines[index].split()[1:]
            if isFloat:
                listScores = list(map(float, listScores))
            else:
                listScores = list(map(int, listScores))
            arrayValues.append(listScores)
            index += 1
        index += 1
        return index, arrayValues

    @staticmethod
    def parseMap(mapPath):
        with open(str(mapPath)) as fd:
            listLines = fd.readlines()
        index = 0
        # Parse scores
        index, arrayScore = DozorM.parseMatrix(index, listLines, isFloat=True)
        # Parse crystals
        index, arrayCrystal = DozorM.parseMatrix(index, listLines, isFloat=False)
        # Parse image number
        index, arrayImageNumber = DozorM.parseMatrix(index, listLines, isFloat=True)
        return arrayScore, arrayCrystal, arrayImageNumber

    @staticmethod
    def updateMeshPositions(meshPositions, arrayScore):
        newMeshPositions = []
        for position in meshPositions:
            # pprint.pprint(position)
            indexY = position["indexY"]
            indexZ = position["indexZ"]
            # print(indexY, indexZ)
            dozormScore = arrayScore[indexZ][indexY]
            dozorScore = position["dozor_score"]
            # print(dozorScore, dozormScore)
            newPosition = dict(position)
            newPosition["dozor_score_orig"] = dozorScore
            newPosition["dozor_score"] = dozormScore
            newMeshPositions.append(newPosition)
        return newMeshPositions

