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
__updated__ = "2021-07-20"

import os
import numpy
import textwrap
import matplotlib
import matplotlib.cm
import matplotlib.pyplot as plt

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsLogging
from edna2.utils import UtilsDetector


logger = UtilsLogging.getLogger()

class DozorM2(AbstractTask):  # pylint: disable=too-many-instance-attributes
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
                "reject_level": {"type": "integer"},
                "isHorizontalScan": {"type": "boolean"},
                "number_scans": {"type": "integer"},
                "grid_x0": {"type": "number"},
                "grid_x1": {"type": "number"},
                "phi_values": {
                    "type": "array",
                    "items": {"type": "number"}
                },
                "sampx": {"type": "number"},
                "sampy": {"type": "number"},
                "phiy": {"type": "number"},
            }
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "logPath": {"type": "string"},
                "workingDirectory": {"type": "string"},
            },
        }

    def run(self, inData):
        if len(inData["list_dozor_all"]) > 1:
            commandLine = "dozorm2 -avs -cr dozorm2.dat"
        else:
            commandLine = "dozorm2 dozorm2.dat"
        commands = self.generateCommands(inData, self.getWorkingDirectory())
        with open(str(self.getWorkingDirectory() / 'dozorm2.dat'), 'w') as f:
            f.write(commands)
        logPath = self.getWorkingDirectory() / 'dozorm2.log'
        self.runCommandLine(commandLine, logPath=logPath)
        outData = self.parseOutput(self.getWorkingDirectory(), logPath)
        outData["logPath"] = str(logPath)
        outData["workingDirectory"] = str(self.getWorkingDirectory())
        return outData

    @staticmethod
    def generateCommands(inData, workingDirectory):
        """
        This method creates the input file for dozorm
        """
        detectorType = inData['detectorType']
        nx = UtilsDetector.getNx(detectorType)
        ny = UtilsDetector.getNy(detectorType)
        pixelSize = UtilsDetector.getPixelsize(detectorType)
        for index, dozor_all_file in enumerate(inData["list_dozor_all"]):
            os.symlink(dozor_all_file, str(workingDirectory / "d_00{0}".format(index+1)))
        nameTemplateScan = "d_00?"
        if inData.get('isHorizontalScan', True):
            meshDirect = "-h"
        else:
            meshDirect = "-v"
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
        command += 'mesh_direct {0}\n'.format(meshDirect)
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
        command += 'first_scan_number 1\n'
        if 'phi_values' in inData:
            for index, phi_value in enumerate(inData['phi_values']):
                command += 'phi{0} {1}\n'.format(index+1, phi_value)
            command += 'axis_zero {0} {1}\n'.format(inData["grid_x0"], inData["grid_y0"])
        if "sampx" in inData:
            command += 'sampx {0}\n'.format(inData["sampx"])
        if "sampy" in inData:
            command += 'sampy {0}\n'.format(inData["sampy"])
        if "phiy" in inData:
            command += 'phiy {0}\n'.format(inData["phiy"])
        command += 'end\n'
        # logger.debug('command: {0}'.format(command))
        return command

    @staticmethod
    def parseOutput(workingDir, logPath):
        outData = {}
        pathDozorm2Map = workingDir / "dozorm_001.map"
        if pathDozorm2Map.exists():
            dictMap = DozorM2.parseMap(pathDozorm2Map)
            nx = dictMap["nx"]
            ny = dictMap["ny"]
            dictCoord = DozorM2.parseDozorm2LogFile(logPath)
            # Fix for problem with 1D scans
            # listPositions = DozorM2.check1Dpositions(listPositions, nx, ny)
            crystalMapPath = DozorM2.makeCrystalPlot(dictMap["crystal"], workingDir)
            if nx != 1 and ny != 1:
                imageNumberMapPath = DozorM2.makeImageNumberMap(dictMap["imageNumber"], workingDir)
            else:
                imageNumberMapPath = None
            outData = {
                "dozorMap": str(pathDozorm2Map),
                "dictCoord": dictCoord,
                "nx": nx,
                "ny": ny,
                "score": dictMap["score"],
                "crystal": dictMap["crystal"],
                "imageNumber": dictMap["imageNumber"],
                "crystalMapPath": crystalMapPath,
                "imageNumberMapPath": imageNumberMapPath
            }
        return outData

    @staticmethod
    def parseDozorm2LogFile(logPath):
        #                    SCAN 1
        #                    ======
        #
        #    Total N.of crystals in Loop =  8
        # Cryst Aperture Central  Coordinate  Int/Sig  N.of Images CRsize Score  Helic   Start     Finish     Int/Sig
        # number size     image      X    Y          All  dX  dY   X   Y   sum           x     y     x     y   helical
        # ------------------------------------------------------------------------------------------------------------> X
        #     1   100.0      23   13.5    1.9  261.4   6   6   1   6   1   550.0   NO
        #     2    30.0      50   14.0    2.9   92.8   3   3   1   3   1   151.7  YES    14     3    16     3   317.9
        #     3    30.0      53   17.0    2.9   54.7   2   2   1   2   1    70.4   NO
        #     4    30.0      26   11.0    1.9   31.0   1   1   1   1   1    66.2   NO
        with open(str(logPath)) as fd:
            listLogLines = fd.readlines()
        doParseLine = False
        do3dCoordinates = False
        scan1 = None
        scan2 = None
        listCoord = None
        for line in listLogLines:
            # print([line])
            if "SCAN 1" in line:
                listPositions = []
            elif "SCAN 2" in line:
                scan1 = listPositions
                listPositions = []
            elif "3D COORDINATES" in line:
                scan2 = listPositions
                do3dCoordinates = True
                listCoord = []
            if line.startswith("------"):
                doParseLine = True
            elif len(line) == 1:
                doParseLine = False
            elif doParseLine:
                listValues = line.split()
                if not do3dCoordinates:
                    try:
                        iOverSigma = float(listValues[5])
                    except:
                        iOverSigma = listValues[5]
                    position = {
                        "number": int(listValues[0]),
                        "apertureSize": str(int(float(listValues[1]))),
                        "imageNumber": int(listValues[2]),
                        "xPosition": float(listValues[3]),
                        "yPosition": float(listValues[4]),
                        "iOverSigma": iOverSigma,
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
                else:
                    coord = {
                        "number": int(listValues[0]),
                        "averageScore": float(listValues[1]),
                        "sc1": int(listValues[2]),
                        "sc2": int(listValues[3]),
                        "size": float(listValues[4]),
                        "scanX":  float(listValues[5]),
                        "scanY1": float(listValues[6]),
                        "scanY2": float(listValues[7]),
                        "dx": float(listValues[8]),
                        "dy1": float(listValues[9]),
                        "dy2": float(listValues[10]),
                        "x": float(listValues[11]),
                        "y": float(listValues[12]),
                        "z": float(listValues[13]),
                        "alfa": float(listValues[14]),
                        "sampx": float(listValues[15]),
                        "sampy": float(listValues[16]),
                        "phiy": float(listValues[17])
                    }
                    listCoord.append(coord)
        if scan1 is None:
            scan1 = listPositions
        dictCoord = {
            "scan1": scan1,
            "scan2": scan2,
            "coord": listCoord
        }
        return dictCoord

    @staticmethod
    def makeCrystalPlot(arrayCrystal, workingDirectory, debug=False):
        npArrayCrystal = numpy.array(arrayCrystal)
        ySize, xSize = npArrayCrystal.shape
        if xSize == 1:
            # Vertical line scan - transpose the matrix
            npArrayCrystal = numpy.transpose(npArrayCrystal)
            ySize, xSize = npArrayCrystal.shape
        npArrayCrystalAbs = numpy.abs(npArrayCrystal)
        # Make '999' be the max crystal number + 1
        maxNumber = numpy.amax(numpy.where(npArrayCrystalAbs < 999, npArrayCrystalAbs, 0))
        npArrayCrystalAbs = numpy.where(npArrayCrystalAbs == 999, maxNumber + 1, npArrayCrystalAbs)
        # minValue = numpy.amin(npArrayCrystal)
        # newZeroValue = minValue - 1
        # npArrayCrystal = numpy.where(npArrayCrystal == 0.0, newZeroValue, npArrayCrystal)

        maxSize = max(xSize, ySize)
        if maxSize < 10:
            fontSize = 12
            dpi = 75
        elif maxSize < 50:
            fontSize = 8
            dpi = 100
        else:
            fontSize =5
            dpi = 150

        font = {'family': 'normal',
                'weight': 'normal',
                'size': fontSize}

        matplotlib.rc('font', **font)

        fig, ax = plt.subplots()

        im = ax.imshow(
            npArrayCrystalAbs,
            cmap=matplotlib.cm.Spectral
        )

        ax.set_xticks(numpy.arange(len(range(xSize))))
        ax.set_yticks(numpy.arange(len(range(ySize))))

        ax.set_xticklabels(list(range(1, xSize+1)))
        ax.set_yticklabels(list(range(1, ySize+1)))

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(ySize):
            for j in range(xSize):
                if abs(npArrayCrystal[i, j]) > 0.001:
                    text = ax.text(j, i, npArrayCrystal[i, j],
                                   ha="center", va="center", color="b")

        ax.set_title("Crystal map")
        fig.tight_layout(pad=2)
        w, h = fig.get_size_inches()
        x1, x2 = ax.get_xlim()
        y1, y2 = ax.get_ylim()
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        fig.set_size_inches(w + 2, abs(y2 - y1) / (x2 - x1) * w + 2)
        if debug:
            plt.show()
        crystalMapPath = os.path.join(workingDirectory, "crystalMap.png")
        plt.savefig(crystalMapPath, dpi=dpi)

        return crystalMapPath

    @staticmethod
    def makeImageNumberMap(arrayImageNumber, workingDirectory, debug=False):
        npImageNumber = numpy.array(arrayImageNumber)
        npArrayImageNumber = numpy.zeros(npImageNumber.shape)
        ySize, xSize = npImageNumber.shape

        maxSize = max(xSize, ySize)
        if maxSize < 10:
            fontSize = 12
            dpi = 75
        elif maxSize < 50:
            fontSize = 8
            dpi = 100
        else:
            fontSize =5
            dpi = 150

        font = {'family': 'normal',
                'weight': 'normal',
                'size': fontSize}

        matplotlib.rc('font', **font)

        fig, ax = plt.subplots()
        im = ax.imshow(
            npArrayImageNumber,
            cmap=matplotlib.cm.Greys
        )

        ax.set_xticks(numpy.arange(len(range(xSize))))
        ax.set_yticks(numpy.arange(len(range(ySize))))

        ax.set_xticklabels(list(range(1, xSize+1)))
        ax.set_yticklabels(list(range(1, ySize+1)))

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(ySize):
            for j in range(xSize):
                text = ax.text(j, i, arrayImageNumber[i][j],
                               ha="center", va="center", color="b")

        ax.set_title("Image numbers")
        fig.tight_layout(pad=2)
        w, h = fig.get_size_inches()
        x1, x2 = ax.get_xlim()
        y1, y2 = ax.get_ylim()
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        fig.set_size_inches(w + 2, abs(y2 - y1) / (x2 - x1) * w + 2)
        if debug:
            plt.show()
        imageNumberPath = os.path.join(workingDirectory, "imageNumber.png")
        plt.savefig(imageNumberPath, dpi=dpi)

        return imageNumberPath

    @staticmethod
    def parseMatrix(index, listLines, spacing, isFloat=True):
        arrayValues = []
        # Parse matrix - starts and ends with "---" line
        while not listLines[index].startswith("-------"):
            index += 1
        index += 1
        while not listLines[index].startswith("-------"):
            # listScores = textwrap.wrap(listLines[index][5:], spacing)
            listScores = []
            for line_pos in range(0, len(listLines[index]), spacing):
                sub_string = listLines[index][line_pos + 5:line_pos + spacing + 5].strip()
                if sub_string != "":
                    if isFloat:
                        listScores.append(float(sub_string))
                    else:
                        listScores.append(int(sub_string))
            arrayValues.append(listScores)
            index += 1
        index += 1
        return index, arrayValues



    @staticmethod
    def parseMap(mapPath):
        with open(str(mapPath)) as fd:
            listLines = fd.readlines()
        # Parse map dimensions
        index = 1
        nx, ny = map(int, listLines[index].split())
        # Parse scores
        index, arrayScore = DozorM2.parseMatrix(index, listLines, spacing=6, isFloat=True)
        # Parse rel. contamination
        index, relContamination = DozorM2.parseMatrix(index, listLines, spacing=6, isFloat=True)
        # Parse crystals
        index, arrayCrystal = DozorM2.parseMatrix(index, listLines, spacing=4, isFloat=False)
        # Parse image number
        index, arrayImageNumber = DozorM2.parseMatrix(index, listLines, spacing=5, isFloat=False)
        dictMap = {
            "nx": nx,
            "ny": ny,
            "score": arrayScore,
            "relContamination": relContamination,
            "crystal": arrayCrystal,
            "imageNumber": arrayImageNumber
        }
        return dictMap

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

    @staticmethod
    def check1Dpositions(listPositions, nx, ny):
        newListPositions = []
        for position in listPositions:
            newPosition = dict(position)
            if nx == 1:
                newPosition["xPosition"] = 1.0
            if ny == 1:
                newPosition["yPosition"] = 1.0
            newListPositions.append(newPosition)
        return newListPositions
