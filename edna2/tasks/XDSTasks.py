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
__date__ = "20/04/2020"

# Corresponding EDNA code:
# https://github.com/olofsvensson/edna-mx

# mxPluginExec/plugins/EDPluginGroupXDS-v1.0/plugins/EDPluginXDSv1_0.py
# mxPluginExec/plugins/EDPluginGroupXDS-v1.0/plugins/EDPluginXDSIndexingv1_0.py

import os
import math
import shutil
import numpy as np

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsImage
from edna2.utils import UtilsConfig
from edna2.utils import UtilsLogging
from edna2.utils import UtilsDetector
from edna2.utils import UtilsSymmetry


logger = UtilsLogging.getLogger()


class XDSTask(AbstractTask):
    """
    Common base class for all XDS tasks
    """

    def run(self, inData):
        commandLine = 'xds_par'
        listXDS_INP = self.generateXDS_INP(inData)
        self.writeXDS_INP(listXDS_INP, self.getWorkingDirectory())
        self.setLogFileName('xds.log')
        self.runCommandLine(commandLine, listCommand=[])
        # Work in progress!
        outData = self.parseXDSOutput(self.getWorkingDirectory())
        return outData

    @staticmethod
    def generateImageLinks(inData, workingDirectory=None):
        listImageLink = []
        firstSubWedge = inData["subWedge"][0]
        firstImagePath = firstSubWedge["image"][0]["path"]
        prefix = UtilsImage.getPrefix(firstImagePath)
        suffix = UtilsImage.getSuffix(firstImagePath)
        template = "%s_xdslink_?????.%s" % (prefix, suffix)
        xdsLowestImageNumberGlobal = 1
        # First we have to find the smallest goniostat rotation axis start:
        oscillationStartMin = 0
        # for subWedge in inData["subWedge"]:
        #     goniostat = subWedge["experimentalCondition"]["goniostat"]
        #     oscillationStart = goniostat["rotationAxisStart"]
        #     if oscillationStartMin is None or \
        #         oscillationStartMin > oscillationStart:
        #         oscillationStartMin = oscillationStart

        # Loop through the list of sub wedges

        for subWedge in inData["subWedge"]:
            imageList = subWedge["image"]
            xsDataGoniostat = subWedge["experimentalCondition"]["goniostat"]
            oscillationStart = xsDataGoniostat["rotationAxisStart"]
            oscillationRange = xsDataGoniostat["oscillationWidth"]

            # First find the lowest and highest image numbers
            lowestImageNumber = None
            for dictImage in imageList:
                imageNumber = dictImage["number"]
                if lowestImageNumber is None or imageNumber < lowestImageNumber:
                    lowestImageNumber = imageNumber

            # Loop through the list of images
            lowestXDSImageNumber = None
            highestXDSImageNumber = None
            for dictImage in imageList:
                imageNumber = dictImage["number"]
                imageOscillationStart = \
                    oscillationStart + (imageNumber - lowestImageNumber) * oscillationRange
                # if xdsLowestImageNumberGlobal is None:
                #     xdsLowestImageNumberGlobal = 1 + int((imageOscillationStart - oscillationStartMin) / oscillationRange)
                xdsImageNumber = xdsLowestImageNumberGlobal + \
                                 int((imageOscillationStart - oscillationStartMin) / oscillationRange)
                print(xdsImageNumber, imageOscillationStart, oscillationStartMin, oscillationRange)
                sourcePath = dictImage["path"]
                target = "%s_xdslink_%05d.%s" % (prefix, xdsImageNumber, suffix)
                print([sourcePath, target])
                listImageLink.append([sourcePath, target])
                if workingDirectory is not None:
                    os.symlink(sourcePath, target)
                if lowestXDSImageNumber is None or \
                        lowestXDSImageNumber > xdsImageNumber:
                    lowestXDSImageNumber = xdsImageNumber
                if highestXDSImageNumber is None or \
                        highestXDSImageNumber < xdsImageNumber:
                    highestXDSImageNumber = xdsImageNumber
        dictImageLinks = {
            "imageLink": listImageLink,
            "dataRange": [lowestXDSImageNumber, highestXDSImageNumber],
            "template": template
        }
        return dictImageLinks



    @staticmethod
    def generateXDS_INP(inData):
        """
        This method creates a list of XDS.INP commands
        """
        # Take the first sub webge in input as reference
        firstSubwedge = inData["subWedge"][0]
        listImage = firstSubwedge['image']
        image = listImage[0]
        experimentalCondition = firstSubwedge['experimentalCondition']
        detector = experimentalCondition['detector']
        dictXDSDetector = XDSTask.getXDSDetector(detector)
        beam = experimentalCondition['beam']
        goniostat = experimentalCondition['goniostat']
        distance = round(detector['distance'], 3)
        wavelength = round(beam['wavelength'], 3)
        oscRange = goniostat['oscillationWidth']
        startAngle = goniostat['rotationAxisStart'] - int(goniostat['rotationAxisStart'])
        dataRange = '1 360'
        listXDS_INP = [
            'OVERLOAD=10048500',
            'DIRECTION_OF_DETECTOR_X-AXIS={0}'.format(UtilsConfig.get('XDSTask', 'DIRECTION_OF_DETECTOR_X-AXIS')),
            'DIRECTION_OF_DETECTOR_Y-AXIS={0}'.format(UtilsConfig.get('XDSTask', 'DIRECTION_OF_DETECTOR_Y-AXIS')),
            'ROTATION_AXIS={0}'.format(UtilsConfig.get('XDSTask', 'ROTATION_AXIS')),
            'INCIDENT_BEAM_DIRECTION={0}'.format(UtilsConfig.get('XDSTask', 'INCIDENT_BEAM_DIRECTION')),
            'NX={0} NY={1} QX={2} QY={2}'.format(
                dictXDSDetector["nx"], dictXDSDetector["ny"], dictXDSDetector["pixel"]),
            'ORGX={0} ORGY={1}'.format(
                dictXDSDetector["orgX"], dictXDSDetector["orgY"]),
            'DETECTOR={0}  MINIMUM_VALID_PIXEL_VALUE={1}  OVERLOAD={2}'.format(
                dictXDSDetector["name"],
                dictXDSDetector["minimumValidPixelValue"],
                dictXDSDetector["overload"]
            ),
            'SENSOR_THICKNESS={0}'.format(
                dictXDSDetector["sensorThickness"]),
            'TRUSTED_REGION={0} {1}'.format(
                dictXDSDetector["trustedRegion"][0],
                dictXDSDetector["trustedRegion"][1]
            )]
        # for trustedRegion in dictXDSDetector["untrustedRectangle"]:
        #     listXDS_INP.append('UNTRUSTED_RECTANGLE={0} {1} {2} {3}'.format(
        #         trustedRegion[0], trustedRegion[1],
        #         trustedRegion[2],trustedRegion[3]
        #     ))
        listXDS_INP += [
            'DETECTOR_DISTANCE={0}'.format(distance),
            'X-RAY_WAVELENGTH={0}'.format(wavelength),
            'OSCILLATION_RANGE={0}'.format(oscRange),
            'STARTING_ANGLE={0}'.format(startAngle),
            'INDEX_QUALITY= 0.25'
        ]
        if "spaceGroupNumber" in inData:
            spaceGroupNumber = inData["spaceGroupNumber"]
            cell = inData["cell"]
            unitCellConstants = "{a} {b} {c} {alpha} {beta} {gamma}".format(**cell)
            listXDS_INP += [
                'SPACE_GROUP_NUMBER={0}'.format(spaceGroupNumber),
                'UNIT_CELL_CONSTANTS={0}'.format(unitCellConstants)
            ]
        return listXDS_INP

    @staticmethod
    def createSPOT_XDS(listDozorSpotFile, oscRange):
        """
              implicit none
              integer nmax
              parameter(nmax=10000000)
              real*4 x(3),j
              integer n,i,k
              real*4 xa(nmax,3),ja(nmax)
              logical new
        c
              n=0
              do while(.true.)
                 read(*,*,err=1,end=1)x,j
                 new = .true.
                 do i = n,1,-1
                    if (abs(xa(i,3)-x(3)) .gt. 20.0 ) goto 3
                    do k = 1,2
                       if (abs(x(k)-xa(i,k)) .gt. 6.0) goto 2
                    enddo
                    new = .false.
                    xa(i,:)=(xa(i,:)*ja(i)+x*j)/(ja(i)+j)
                    ja(i)=ja(i)+j
          2         continue
                 enddo
          3       if (new) then
                    n=n+1
                    xa(n,:)=x
                    ja(n)=j
                 endif
              enddo
          1   continue
              do i=1,n
                 write(*,*)xa(i,:), ja(i)
              enddo
              end
        """
        listSpotXds = []
        n = 0
        firstFrame = True
        for dozorSpotFile in listDozorSpotFile:
            # Read the file
            with open(str(dozorSpotFile)) as f:
                dozorLines = f.readlines()
            omega = float(dozorLines[2].split()[1])
            frame = int((omega - oscRange/2)/oscRange) + 1
            frame = frame % 360
            for dozorLine in dozorLines[3:]:
                new = True
                listValues = dozorLine.split()
                n, xPos, yPos, intensity, sigma = list(map(float, listValues))
                # Subtracting 1 from X and Y: this is because for dozor the upper left pixel in the image is (1,1),
                # whereas for the rest of the world it is (0,0)
                xPos = xPos - 1
                yPos = yPos - 1
                index = 0
                for spotXds in listSpotXds:
                    frameOld = spotXds[2]
                    if abs(frameOld - frame) > 20:
                        break
                    xPosOld = spotXds[0]
                    yPosOld = spotXds[1]
                    intensityOld = spotXds[3]
                    if abs(xPosOld - xPos) <= 6 and abs(yPosOld - yPos) <= 6:
                        new = False
                        intensityNew = intensity + intensityOld
                        xPosNew = (xPosOld*intensityOld + xPos*intensity) / intensityNew
                        yPosNew = (yPosOld*intensityOld + yPos*intensity) / intensityNew
                        listSpotXds[index] = [xPosNew, yPosNew, frameOld, intensityNew]
                    index += 1

                if new:
                    spotXds = [xPos, yPos, frame, intensity]
                    listSpotXds.append(spotXds)


        strSpotXds = ''
        for spotXds in listSpotXds:
            strSpotXds += '{0:13.6f}{1:17.6f}{2:17.8f}{3:17.6f}    \n'.format(*spotXds)
        return strSpotXds

    @staticmethod
    def writeSPOT_XDS(listDozorSpotFile, oscRange, workingDirectory):
        spotXds = XDSTask.createSPOT_XDS(listDozorSpotFile, oscRange)
        filePath = workingDirectory / 'SPOT.XDS'
        with open(str(filePath), 'w') as f:
            f.write(spotXds)

    def writeXDS_INP(self, listXDS_INP, workingDirectory):
        fileName = 'XDS.INP'
        filePath = workingDirectory / fileName
        with open(str(filePath), 'w') as f:
            for line in listXDS_INP:
                f.write(line + '\n')

    @staticmethod
    def getXDSDetector(dictDetector):
        dictXDSDetector = None
        detectorType = dictDetector["type"]
        nx = UtilsDetector.getNx(detectorType)
        ny = UtilsDetector.getNy(detectorType)
        pixel = UtilsDetector.getPixelsize(detectorType)
        orgX = round(dictDetector['beamPositionX'] / pixel, 3)
        orgY = round(dictDetector['beamPositionY'] / pixel, 3)
        if detectorType == "pilatus2m":
            untrustedRectangle = \
                [[487, 495, 0, 1680],
                 [981, 989, 0, 1680],
                 [0, 1476, 195, 213],
                 [0, 1476, 407, 425],
                 [0, 1476, 619, 637],
                 [0, 1476, 831, 849],
                 [0, 1476, 1043, 1061],
                 [0, 1476, 1255, 1273],
                 [0, 1476, 1467, 1485]]
            sensorThickness = 0.32
        elif detectorType == "pilatus6m":
            listUntrustedRectangle = \
               [[ 487, 495, 0, 2528],
                [ 981, 989, 0, 2528],
                [1475, 1483, 0, 2528],
                [1969, 1977, 0, 2528],
                [   0, 2464, 195, 213],
                [   0, 2464, 407, 425],
                [   0, 2464, 619, 637],
                [   0, 2464, 831, 849],
                [   0, 2464, 1043, 1061],
                [   0, 2464, 1255, 1273],
                [   0, 2464, 1467, 1485],
                [   0, 2464, 1679, 1697],
                [   0, 2464, 1891, 1909],
                [   0, 2464, 2103, 2121],
                [   0, 2464, 2315, 2333]]
            sensorThickness = 0.32
        elif detectorType == "eiger4m":
            untrustedRectangle = \
                [[1029, 1040, 0, 2167],
                 [0, 2070, 512, 550],
                 [0, 2070, 1063, 1103],
                 [0, 2070, 1614, 1654],
                 ]
            sensorThickness = 0.32
        elif detectorType == "eiger9m":
            untrustedRectangle = \
                [[1029, 1040, 0, 3269],
                 [2069, 2082, 0, 3269],
                 [0, 3110, 513, 553],
                 [0, 3110, 1064, 1104],
                 [0, 3110, 1615, 1655],
                 [0, 3110, 2166, 2206],
                 [0, 3110, 2717, 2757],
                 ]
        else:
            raise RuntimeError("Unknown detector: {0}".format(detectorType))
        dictXDSDetector = {
            "name": "PILATUS",
            "nx": nx,
            "ny": ny,
            "orgX": orgX,
            "orgY": orgY,
            "pixel": pixel,
            # "untrustedRectangle": untrustedRectangle,
            "trustedRegion": [0.0, 1.41],
            "trustedpixel": [7000, 30000],
            "minimumValidPixelValue": 0,
            "overload": 1048500,
            "sensorThickness": sensorThickness
        }
        return dictXDSDetector


class XDSIndexing(XDSTask):

    def generateXDS_INP(self, inData):
        firstSubWedge = inData["subWedge"][0]
        listDozorSpotFile = inData['dozorSpotFile']
        experimentalCondition = firstSubWedge['experimentalCondition']
        goniostat = experimentalCondition['goniostat']
        oscRange = goniostat['oscillationWidth']
        XDSTask.writeSPOT_XDS(listDozorSpotFile, oscRange=oscRange, workingDirectory=self.getWorkingDirectory())
        listXDS_INP = XDSTask.generateXDS_INP(inData)
        listXDS_INP.insert(0, 'JOB= IDXREF')
        listXDS_INP.append("DATA_RANGE= 1 360")
        return listXDS_INP

    @staticmethod
    def parseXDSOutput(workingDirectory):
        idxrefPath = workingDirectory / 'IDXREF.LP'
        xparmPath = workingDirectory / 'XPARM.XDS'
        outData = {
            "idxref":  XDSIndexing.readIdxrefLp(idxrefPath),
            "xparm":   XDSIndexing.parseXparm(xparmPath),
            "xparmXdsPath": xparmPath
        }
        return outData


    @staticmethod
    def readIdxrefLp(pathToIdxrefLp, resultXDSIndexing=None):
        if resultXDSIndexing is None:
            resultXDSIndexing = {}
        if pathToIdxrefLp.exists():
            with open(str(pathToIdxrefLp)) as f:
                listLines = f.readlines()
            indexLine = 0
            doParseParameters = False
            doParseLattice = False
            while indexLine < len(listLines):
                if "DIFFRACTION PARAMETERS USED AT START OF INTEGRATION" in listLines[indexLine]:
                    doParseParameters = True
                    doParseLattice = False
                elif "DETERMINATION OF LATTICE CHARACTER AND BRAVAIS LATTICE" in listLines[indexLine]:
                    doParseParameters = False
                    doParseLattice = True
                if doParseParameters:
                    if "MOSAICITY" in listLines[indexLine]:
                        resultXDSIndexing['mosaicity'] = float(listLines[indexLine].split()[-1])
                    elif "DETECTOR COORDINATES (PIXELS) OF DIRECT BEAM" in listLines[indexLine]:
                        resultXDSIndexing['xBeam'] = float(listLines[indexLine].split()[-1])
                        resultXDSIndexing['yBeam'] = float(listLines[indexLine].split()[-2])
                    elif "CRYSTAL TO DETECTOR DISTANCE" in listLines[indexLine]:
                        resultXDSIndexing['distance'] = float(listLines[indexLine].split()[-1])
                elif doParseLattice:
                    if listLines[indexLine].startswith(" * ") and not listLines[indexLine + 1].startswith(" * "):
                        listLine = listLines[indexLine].split()
                        latticeCharacter = int(listLine[1])
                        bravaisLattice = listLine[2]
                        spaceGroup = UtilsSymmetry.getMinimumSymmetrySpaceGroupFromBravaisLattice(bravaisLattice)
                        spaceGroupNumber = UtilsSymmetry.getITNumberFromSpaceGroupName(spaceGroup)
                        qualityOfFit = float(listLine[3])
                        resultXDSIndexing.update( {
                            'latticeCharacter': latticeCharacter,
                            'spaceGroupNumber': spaceGroupNumber,
                            'qualityOfFit': qualityOfFit,
                            'a': float(listLine[4]),
                            'b': float(listLine[5]),
                            'c': float(listLine[6]),
                            'alpha': float(listLine[7]),
                            'beta':  float(listLine[8]),
                            'gamma': float(listLine[9])
                        } )
                indexLine += 1
        return resultXDSIndexing

    @staticmethod
    def volum(cell):
        """
        Calculate the cell volum from either:
         - the 6 standard cell parameters (a, b, c, alpha, beta, gamma)
         - or the 3 vectors A, B, C
        Inspired from XOconv written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L758        """
        r2d = 180 / math.pi
        cosd = lambda a: math.cos(a / r2d)
        if len(cell) == 6 and isinstance(cell[0], float):
            # expect a, b, c, alpha, beta, gamma (angles in degree).
            ca, cb, cg = map(cosd, cell[3:6])
            return cell[0] * cell[1] * cell[2] * (1 - ca ** 2 - cb ** 2 - cg ** 2 + 2 * ca * cb * cg) ** 0.5
        elif len(cell) == 3 and isinstance(cell[0], np.array):
            # expect vectors of the 3 cell parameters
            A, B, C = cell
            return A * B.cross(C)
        else:
            return "Can't parse input arguments."

    @staticmethod
    def reciprocal(cell):
        """
        Calculate the 6 reciprocal cell parameters: a*, b*, c*, alpha*, beta*...
        Inspired from XOconv written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L776
        """
        r2d = 180 / math.pi
        cosd = lambda a: math.cos(a / r2d)
        sind = lambda a: math.sin(a / r2d)
        sa, sb, sg = map(sind, cell[3:6])
        ca, cb, cg = map(cosd, cell[3:6])
        v = XDSIndexing.volum(cell)
        rc = (cell[1] * cell[2] * sa / v,
              cell[2] * cell[0] * sb / v,
              cell[0] * cell[1] * sg / v,
              math.acos((cb * cg - ca) / (sb * sg)) * r2d,
              math.acos((ca * cg - cb) / (sa * sg)) * r2d,
              math.acos((ca * cb - cg) / (sa * sb)) * r2d)
        return rc

    @staticmethod
    def BusingLevy(rcell):
        """
        Inspired from XOconv written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L816
        """
        ex = np.array([1,0,0])
        ey = np.array([0,1,0])
        r2d = 180 / math.pi
        cosd = lambda a: math.cos(a / r2d)
        sind = lambda a: math.sin(a / r2d)
        cosr = list(map(cosd, rcell[3:6]))
        sinr = list(map(sind, rcell[3:6]))
        Vr = XDSIndexing.volum(rcell)
        BX = ex * rcell[0]
        BY = rcell[1] * (ex * cosr[2] + ey * sinr[2])
        c = rcell[0] * rcell[1] * sinr[2] / Vr
        cosAlpha = (cosr[1] * cosr[2] - cosr[0]) / (sinr[1] * sinr[2])
        BZ = np.array([rcell[2] * cosr[1],
                   -1 * rcell[2] * sinr[1] * cosAlpha,
                   1 / c])
        return np.array([BX, BY, BZ]).transpose()

    @staticmethod
    def parseXparm(pathToXparmXds):
        """
        Inspired from parse_xparm written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L372
        """
        if pathToXparmXds.exists():
            with open(str(pathToXparmXds)) as f:
                xparm = f.readlines()
            xparamDict = {
                "rot":          list(map(float, xparm[1].split()[3:])),
                "beam":         list(map(float, xparm[2].split()[1:])),
                "distance":     float(xparm[8].split()[2]),
                "originXDS":    list(map(float, xparm[8].split()[:2])),
                "A":            list(map(float, xparm[4].split())),
                "B":            list(map(float, xparm[5].split())),
                "C":            list(map(float, xparm[6].split())),
                "cell":         list(map(float, xparm[3].split()[1:])),
                "pixel_size":   list(map(float, xparm[7].split()[3:])),
                "pixel_numb":   list(map(float, xparm[7].split()[1:])),
                "symmetry":     int(xparm[3].split()[0]),
                "num_init":     list(map(float, xparm[1].split()[:3]))[0],
                "phi_init":     list(map(float, xparm[1].split()[:3]))[1],
                "delta_phi":    list(map(float, xparm[1].split()[:3]))[2],
                "detector_X":   list(map(float, xparm[9].split())),
                "detector_Y":   list(map(float, xparm[10].split()))
            }
        else:
            xparamDict = {}
        return xparamDict


class XDSGenerateBackground(XDSTask):

    def generateXDS_INP(self, inData):
        listXDS_INP = XDSTask.generateXDS_INP(inData)
        listXDS_INP.insert(0, 'JOB= XYCORR INIT COLSPOT')
        dictImageLinks = self.generateImageLinks(
            inData, self.getWorkingDirectory())
        listXDS_INP.append("NAME_TEMPLATE_OF_DATA_FRAMES= {0}".format(
            dictImageLinks["template"] ))
        listXDS_INP.append("DATA_RANGE= {0} {1}".format(
            dictImageLinks["dataRange"][0], dictImageLinks["dataRange"][1]))
        return listXDS_INP

    @staticmethod
    def parseXDSOutput(workingDirectory):
        if (workingDirectory / "BKGINIT.cbf").exists():
            outData = {
                "gainCbf": str(workingDirectory / "GAIN.cbf"),
                "blankCbf": str(workingDirectory / "BLANK.cbf"),
                "bkginitCbf": str(workingDirectory / "BKGINIT.cbf"),
                "xCorrectionsCbf": str(workingDirectory / "X-CORRECTIONS.cbf"),
                "yCorrectionsCbf": str(workingDirectory / "Y-CORRECTIONS.cbf")
            }
        else:
            outData = {}
        return outData


class XDSIntegration(XDSTask):

    def generateXDS_INP(self, inData):
        # Copy XPARM.XDS, GAIN.CBF file
        shutil.copy(inData["xparmXds"], self.getWorkingDirectory())
        shutil.copy(inData["gainCbf"], self.getWorkingDirectory())
        shutil.copy(inData["xCorrectionsCbf"], self.getWorkingDirectory())
        shutil.copy(inData["yCorrectionsCbf"], self.getWorkingDirectory())
        shutil.copy(inData["blankCbf"], self.getWorkingDirectory())
        shutil.copy(inData["bkginitCbf"], self.getWorkingDirectory())
        listXDS_INP = XDSTask.generateXDS_INP(inData)
        listXDS_INP.insert(0, 'JOB= DEFPIX INTEGRATE CORRECT')
        dictImageLinks = self.generateImageLinks(
            inData, self.getWorkingDirectory())
        listXDS_INP.append("NAME_TEMPLATE_OF_DATA_FRAMES= {0}".format(
            dictImageLinks["template"] ))
        listXDS_INP.append("DATA_RANGE= {0} {1}".format(
            dictImageLinks["dataRange"][0], dictImageLinks["dataRange"][1]))
        return listXDS_INP

    @staticmethod
    def parseXDSOutput(workingDirectory):
        outData = {}
        if (workingDirectory / "XDS_ASCII.HKL").exists():
            outData = {
                "xdsAsciiHkl": str(workingDirectory / "XDS_ASCII.HKL"),
                "correctLp": str(workingDirectory / "CORRECT.LP"),
                "bkgpixCbf": str(workingDirectory / "BKGPIX.cbf")
            }
        return outData