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

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "2021/07/20"

import os
import shutil
import pathlib
import tempfile
import unittest

from edna2.tasks.DozorRD import DozorRD

from edna2.utils import UtilsTest


class DozorRDUnitTest(unittest.TestCase):
    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    def test_generateCommands(self):
        referenceDataPath = self.dataPath / "inDataDozorRD.json"
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        command = DozorRD.generateCommands(inData)
        print(command)

    def test_unit_parseDozorRDLogFile(self):
        logPath = self.dataPath / "dozorrd.log"
        dictResult = DozorRD.parseDozorRDLogFile(logPath)
        dictRef = {
            "noSpotDecrease": 1.751,
            "mainScore": 10.719,
            "spotIntensity": 67.269,
            "sumIntensity": 2.218,
            "average": 26.735,
        }
        for key, value in dictRef.items():
            assert dictResult[key] == value
