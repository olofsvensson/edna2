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
from edna2.tasks.Best import Best
from edna2.tasks.ControlIndexing import ControlIndexing
from edna2.tasks.XDSTasks import XDSGenerateBackground
from edna2.tasks.XDSTasks import XDSIntegration
from edna2.tasks.ReadImageHeader import ReadImageHeader

from edna2.utils import UtilsImage

class Characterisation(AbstractTask):
    """
    This task receives a list of images or data collection ids and
    returns result of indexing
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "dataCollectionId": { "type": "integer" },
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
        listImagePath = inData["imagePath"]
        prefix = UtilsImage.getPrefix(listImagePath[0])
        listSubWedge = self.getListSubWedge(inData)
        # Start indexing
        inDataIndexing = {
            "subWedge": listSubWedge,
        }
        indexingTask = ControlIndexing(
            inData=inDataIndexing,
            workingDirectorySuffix=prefix
        )
        indexingTask.start()
        # Start background esitmation
        inDataGenerateBackground = {
            "subWedge": listSubWedge,
        }
        generateBackground = XDSGenerateBackground(
            inData=inDataGenerateBackground,
            workingDirectorySuffix = prefix
        )
        generateBackground.start()
        generateBackground.join()
        # Check indexing
        indexingTask.join()
        if indexingTask.isSuccess():
            outDataIndexing = indexingTask.outData
            outDataGB = generateBackground.outData
            xparmXdsPath = outDataIndexing["xparmXdsPath"]
            if xparmXdsPath is not None:
                listTasks = []
                listXdsAsciiHkl = []
                correctLp = None
                bkgpixCbf = None
                for subWedge in listSubWedge:
                    inDataIntergation = {
                        "subWedge": [subWedge],
                        "xparmXds": xparmXdsPath,
                        "gainCbf": outDataGB["gainCbf"],
                        "blankCbf": outDataGB["blankCbf"],
                        "bkginitCbf": outDataGB["bkginitCbf"],
                        "xCorrectionsCbf": outDataGB["xCorrectionsCbf"],
                        "yCorrectionsCbf": outDataGB["yCorrectionsCbf"]
                    }
                    imageNo = subWedge["image"][0]["number"]
                    integrationTask = XDSIntegration(
                        inData=inDataIntergation,
                        workingDirectorySuffix=prefix + "_{0:04d}".format(imageNo)
                    )
                    integrationTask.start()
                    listTasks.append(integrationTask)
                for task in listTasks:
                    task.join()
                    if "xdsAsciiHkl" in task.outData:
                        listXdsAsciiHkl.append(task.outData["xdsAsciiHkl"])
                    if correctLp is None:
                        correctLp = task.outData["correctLp"]
                        bkgpixCbf = task.outData["bkgpixCbf"]
                inDataBest = {
                    "subWedge": listSubWedge,
                    "xdsAsciiHkl": listXdsAsciiHkl,
                    "bkgpixCbf": bkgpixCbf,
                    "correctLp": correctLp
                }
                bestTask = Best(inData=inDataBest)
                bestTask.execute()




    @staticmethod
    def getListSubWedge(inData):
        listSubWedge = None
        # First check if we have data collection ids or image list
        # if "dataCollectionId" in inData:
        #     # TODO: get list of data collections from ISPyB
        #         logger.warning("Not implemented!")
        # el
        if "imagePath" in inData:
            listSubWedge = Characterisation.readImageHeaders(inData["imagePath"])
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

