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
__date__ = "11/01/2021"

import pprint
import unittest

from edna2.utils import UtilsTest
from edna2.utils import UtilsLogging

from edna2.tasks.Raddose import Raddose

logger = UtilsLogging.getLogger()


class RaddoseUnitTest(unittest.TestCase):

    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    def test_createCommandLine(self):
        referenceDataPath = self.dataPath / 'inDataRaddose.json'
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        commandLine, listCommand = Raddose.createCommandLine(inData)
        print(commandLine)
        pprint.pprint(listCommand)
        self.assertTrue("raddose" in commandLine)
        self.assertTrue("BEAM 0.1 0.1" in listCommand)

    def test_parseLogFile(self):
        logFilePath = self.dataPath / 'raddose.log'
        dictResults = Raddose.parseLogFile(logFilePath)
        # pprint.pprint(dictResults)
        self.assertEqual(dictResults["solventContent"], 59.2)

    def test_createOutData(self):
        referenceDataPath = self.dataPath / 'inDataRaddose.json'
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        logFilePath = self.dataPath / 'raddose.log'
        dictResults = Raddose.parseLogFile(logFilePath)
        outData = Raddose.createOutData(inData, dictResults)
        # pprint.pprint(outData)
        self.assertEqual(outData["absorbedDose"], 223000)
        self.assertEqual(outData["timeToReachHendersonLimit"], 89.7)

    def test_mergeAtomicComposition(self):

        atomicComposition1 = [
            {
                "symbol": "S",
                "numberOf": 4
            },
            {
                "symbol": "Se",
                "numberOf": 3
            }
        ]

        atomicComposition2 = [
            {
                "symbol": "S",
                "numberOf": 1
            },
            {
                "symbol": "Fe",
                "numberOf": 5
            }
        ]

        mergedAtomicComposition = Raddose.mergeAtomicComposition(
            atomicComposition1, atomicComposition2
        )

        self.assertEqual(len(mergedAtomicComposition), 3)

        for atom in mergedAtomicComposition:
            if atom["symbol"] == "S":
                self.assertEqual(5, atom["numberOf"])
            if atom["symbol"] == "Se":
                self.assertEqual(3, atom["numberOf"])
            if atom["symbol"] == "Fe":
                self.assertEqual(5, atom["numberOf"])

        mergedAtomicComposition = Raddose.mergeAtomicComposition(
            [], atomicComposition2)
        self.assertEqual(len(mergedAtomicComposition), 2)
        for atom in mergedAtomicComposition:
            if atom["symbol"] == "S":
                self.assertEqual(1, atom["numberOf"])
            if atom["symbol"] == "Fe":
                self.assertEqual(5, atom["numberOf"])
