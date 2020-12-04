#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the 'Software'), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ['O. Svensson']
__license__ = 'MIT'
__date__ = '21/04/2019'

import os
import json
import pprint
import unittest

from edna2.tasks.DozorM import DozorM

from edna2.utils import UtilsTest
from edna2.utils import UtilsConfig


class DozorMUnitTest(unittest.TestCase):

    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    def test_unit_DozorM_parseDozormLogFile(self):
        logPath = self.dataPath / 'opid23eh1_mesh1_dozorm.log'
        listPositions = DozorM.parseDozormLogFile(logPath)
        self.assertEqual(len(listPositions), 2)
        logPath = self.dataPath / 'opid23eh1_mesh3_dozorm.log'
        listPositions = DozorM.parseDozormLogFile(logPath)
        self.assertEqual(len(listPositions), 9)
        pprint.pprint(listPositions)

    def test_unit_DozorM_makePlots(self):
        mapPath = self.dataPath / 'opid23eh1_mesh1_dozorm.map'
        # heatMapPath, crystalMapPath = DozorM.makePlots(mapPath)

    def test_unit_DozorM_parseMap(self):
        mapPath = self.dataPath / 'opid23eh1_mesh1_dozorm.map'
        npArrayScore, npArrayCrystal, npArrayImageNumber = DozorM.parseMap(mapPath)
        print(npArrayScore)
        print(npArrayCrystal)
        print(npArrayImageNumber)

    def test_updateMeshPositions(self):
        meshPositionPath = self.dataPath / 'opid23eh1_mesh1_meshPositions.json'
        with open(str(meshPositionPath)) as fd:
            meshPositions = json.loads(fd.read())
        mapPath = self.dataPath / 'opid23eh1_mesh1_dozorm.map'
        arrayScore, arrayCrystal, arrayImageNumber = DozorM.parseMap(mapPath)
        newMeshPositions = DozorM.updateMeshPositions(
            meshPositions=meshPositions,
            arrayScore=arrayScore
        )
