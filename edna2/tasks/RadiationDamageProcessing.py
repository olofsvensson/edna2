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
from edna2.tasks.SubWedgeAssembly import SubWedgeAssembly
from edna2.tasks.XDSTasks import XDSIndexAndIntegration


class RadiationDamageProcessing(AbstractTask):
    """
    This task receives a list of images or data collection ids and
    returns result of indexing
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "dataCollectionId": {"type": "integer"},
                "imagePath": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
        }

    def run(self, inData):
        outData = {}
        # First get the list of subWedges
        if "subWedge" in inData:
            list_sub_wedge = inData["subWedge"]
        else:
            list_sub_wedge = self.getListSubWedge(inData)
        indata_xds_integration = {
            "subWedge": list_sub_wedge
        }
        xds_integration = XDSIndexAndIntegration(inData=indata_xds_integration)
        xds_integration.execute()




    def getListSubWedge(self, inData):
        list_sub_wedges = None
        sub_wedge_assembly = SubWedgeAssembly(inData=inData)
        sub_wedge_assembly.execute()
        if sub_wedge_assembly.isSuccess():
            list_sub_wedges = sub_wedge_assembly.outData
        return list_sub_wedges