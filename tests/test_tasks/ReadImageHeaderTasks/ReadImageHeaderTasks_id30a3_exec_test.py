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

import unittest

from edna2.utils import UtilsTest
from edna2.utils import UtilsConfig

from edna2.tasks.ReadImageHeader import ReadImageHeader


class ReadImageHeaderTasksExecTest_id30a3(unittest.TestCase):
    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    @unittest.skipIf(
        UtilsConfig.getSite() == "Default",
        "Cannot run test with default config",
    )
    def test_executeReadImageHeaderTask_id30a3(self):
        referenceDataPath = self.dataPath / "id30a3.json"
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        readImageHeader = ReadImageHeader(inData=inData)
        readImageHeader.execute()
        self.assertTrue(readImageHeader.isSuccess())
