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
__date__ = '2021/07/20'

import pprint
import pathlib
import tempfile
import unittest

from edna2.tasks.DozorM2 import DozorM2

from edna2.utils import UtilsTest


class DozorM2UnitTest(unittest.TestCase):

    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    def test_generateCommands(self):
        workingDir = pathlib.Path(tempfile.mkdtemp(prefix="DozorM2_"))
        referenceDataPath = self.dataPath / 'inDataDozorM2.json'
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        command = DozorM2.generateCommands(inData, workingDir)
        print(command)

    def test_unit_parseDozorm2LogFile_1(self):
        logPath = self.dataPath / 'dozorm2.log'
        dictCoord = DozorM2.parseDozorm2LogFile(logPath)
        # pprint.pprint(scan1)
        # pprint.pprint(scan2)
        # pprint.pprint(coord)
        self.assertEqual(len(dictCoord["scan1"]), 8)
        self.assertEqual(len(dictCoord["scan2"]), 8)
        self.assertEqual(len(dictCoord["coord"]), 7)
