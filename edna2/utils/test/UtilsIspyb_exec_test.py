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
__date__ = "21/04/2019"


import os
import string
import random
import unittest

from edna2.utils import UtilsIspyb
from edna2.utils import UtilsConfig


class UtilsIspybExecTest(unittest.TestCase):

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run control dozor test with default config')
    def test_findDataCollectionFromFileLocationAndFileName(self):
        firstImagePath = "/data/id30a2/inhouse/opid30a2/20200907/RAW_DATA/MeshScan_10/mesh-opid30a2_1_0001.cbf"
        dataCollection = UtilsIspyb.findDataCollectionFromFileLocationAndFileName(firstImagePath)
        self.assertEqual(2483117, dataCollection.dataCollectionId)

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run control dozor test with default config')
    def test_setImageQualityIndicatorsPlot(self):
        dataCollectionId = 2483117
        letters = string.ascii_lowercase
        filePlot = ''.join(random.choice(letters) for i in range(10))
        fileCsv = ''.join(random.choice(letters) for i in range(10))
        dataCollectionId2 = UtilsIspyb.setImageQualityIndicatorsPlot(dataCollectionId, filePlot, fileCsv)
        self.assertEqual(dataCollectionId, dataCollectionId2)
        # dataCollection = UtilsIspyb.findDataCollection(dataCollectionId)
        # print(dataCollection)
        # self.assertEqual(filePlot, dataCollection.imageQualityIndicatorsPlotPath)
        # self.assertEqual(fileCsv, dataCollection.imageQualityIndicatorsCSVPath)
