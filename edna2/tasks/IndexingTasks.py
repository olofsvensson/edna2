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
__date__ = "14/04/2020"

import numpy as np


from edna2.tasks.AbstractTask import AbstractTask
from edna2.tasks.ReadImageHeader import ReadImageHeader
from edna2.tasks.DozorTasks import ControlDozor
from edna2.tasks.XDSTasks import XDSIndexingTask

from edna2.utils import UtilsImage

class ControlIndexingTask(AbstractTask):
    """
    This task receives a list of images or data collection ids and
    returns result of indexing
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "dataCollectionId": {
                    "type": "array",
                    "items": {
                        "type": "integer",
                    }
                },
                "imagePath": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    }
                }
            }
        }

    def run(self, inData):
        outData = {}
        # First get the list of subWedges
        listSubWedge = self.getListSubWedge(inData)
        # Get list of spots from Dozor
        imageDict = listSubWedge[0]
        imageDict["dozorSpotFile"] = self.getDozorSpotFiles(listSubWedge)
        # Run XDS indexing
        resultIndexing = self.runXdsIndexing(imageDict)
        outData = {
            "resultIndexing": resultIndexing
        }
        return outData

    @staticmethod
    def getListSubWedge(inData):
        listSubWedge = None
        # First check if we have data collection ids or image list
        if "dataCollectionId" in inData:
            # TODO: get list of data collections from ISPyB
            raise RuntimeError("Not implemented!")
        elif "imagePath" in inData:
            listSubWedge = ControlIndexingTask.readImageHeaders(inData["imagePath"])
        else:
            raise RuntimeError("No dataCollectionId or imagePath in inData")
        return listSubWedge

    @staticmethod
    def readImageHeaders(listImagePath):
        # Read the header(s)
        inDataReadImageHeader = {
            "imagePath": listImagePath
        }
        readImageHeader = ReadImageHeader(
            inData=inDataReadImageHeader,
            workingDirectorySuffix=UtilsImage.getPrefix(listImagePath[0])
        )
        readImageHeader.execute()
        listSubWedge = readImageHeader.outData["subWedge"]
        return listSubWedge

    @staticmethod
    def getDozorSpotFiles(listSubWedge):
        listDozorSpotFile = []
        for subWedge in listSubWedge:
            listSubWedgeImage = subWedge['image']
            for image in listSubWedgeImage:
                # listImage.append(image['path'])
                inDataControlDozor = {
                    'image': [image['path']]
                }
                controlDozor = ControlDozor(
                    inData=inDataControlDozor,
                    workingDirectorySuffix=UtilsImage.getPrefixNumber(image['path'])
                )
                controlDozor.execute()
                if controlDozor.isSuccess():
                    dozorSpotFile = controlDozor.outData["imageQualityIndicators"][0]["dozorSpotFile"]
                    listDozorSpotFile.append(dozorSpotFile)
        return listDozorSpotFile

    @staticmethod
    def getResultIndexingFromXds(xdsIndexingOutData):
        idxref = xdsIndexingOutData["idxref"]
        xparamDict = xdsIndexingOutData["xparm"]
        # Calculate MOSFLM UB matrix
        A = np.array(xparamDict["A"])
        B = np.array(xparamDict["B"])
        C = np.array(xparamDict["C"])

        volum = np.cross(A, B).dot(C)
        Ar = np.cross(B, C) / volum
        Br = np.cross(C, A) / volum
        Cr = np.cross(A, B) / volum
        UBxds = np.array([Ar, Br, Cr]).transpose()

        BEAM = np.array(xparamDict["beam"])
        ROT = np.array(xparamDict["rot"])
        wavelength = 1 / np.linalg.norm(BEAM)

        xparamDict["cell_volum"] = volum
        xparamDict["wavelength"] = wavelength
        xparamDict["Ar"] = Ar.tolist()
        xparamDict["Br"] = Br.tolist()
        xparamDict["Cr"] = Cr.tolist()
        xparamDict["UB"] = UBxds.tolist()

        normROT = float(np.linalg.norm(ROT))
        CAMERA_z = np.true_divide(ROT, normROT)
        CAMERA_y = np.cross(CAMERA_z, BEAM)
        normCAMERA_y = float(np.linalg.norm(CAMERA_y))
        CAMERA_y = np.true_divide(CAMERA_y, normCAMERA_y)
        CAMERA_x = np.cross(CAMERA_y, CAMERA_z)
        CAMERA = np.transpose(np.array([CAMERA_x, CAMERA_y, CAMERA_z]))

        mosflmUB = CAMERA.dot(UBxds) * xparamDict["wavelength"]
        # mosflmUB = UBxds*xparamDict["wavelength"]
        # xparamDict["mosflmUB"] = mosflmUB.tolist()

        reciprocCell = XDSIndexingTask.reciprocal(xparamDict["cell"])
        B = XDSIndexingTask.BusingLevy(reciprocCell)
        mosflmU = np.dot(mosflmUB, np.linalg.inv(B)) / xparamDict["wavelength"]
        # xparamDict[

        resultIndexing = {
            "spaceGroupNumber": idxref["spaceGroupNumber"],
            "cell": {
                "a": idxref["a"],
                "b": idxref["b"],
                "c": idxref["c"],
                "alpha": idxref["alpha"],
                "beta": idxref["beta"],
                "gamma": idxref["gamma"],
            },
            "xBeam": idxref["xBeam"],
            "yBeam": idxref["yBeam"],
            "distance": idxref["distance"],
            "qualityOfFit": idxref["qualityOfFit"],
            "mosaicity": idxref["mosaicity"],
            "XDS_xparm": xparamDict,
            "mosflmB": mosflmU.tolist(),
            "mosflmU": mosflmU.tolist()
        }
        return resultIndexing

    @staticmethod
    def runXdsIndexing(imageDict):
        xdsIndexinInData = {
            "image": [imageDict]
        }
        xdsIndexingTask = XDSIndexingTask(
            inData=xdsIndexinInData,
            workingDirectorySuffix=UtilsImage.getPrefix(imageDict["image"][0]["path"])
        )
        xdsIndexingTask.execute()
        resultIndexing = {}
        if xdsIndexingTask.isSuccess():
            xdsIndexingOutData = xdsIndexingTask.outData
            resultIndexing = ControlIndexingTask.getResultIndexingFromXds(xdsIndexingOutData)
        return resultIndexing
