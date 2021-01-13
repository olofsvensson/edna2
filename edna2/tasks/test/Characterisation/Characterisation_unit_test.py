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

import pprint
import unittest

from edna2.tasks.Characterisation import Characterisation

from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


class ControlIndexingUnitTest(unittest.TestCase):

    def test_getDefaultChemicalComposition(self):
        cell = {
            "a": 78.9, "b": 95.162, "c": 104.087,
            "alpha": 90, "beta": 90, "gamma": 90
        }
        numOperators = 4
        chemicalCompositionMM = Characterisation.getDefaultChemicalComposition(cell, numOperators)
        # pprint.pprint(chemicalCompositionMM)
        self.assertEqual(chemicalCompositionMM["solvent"]["atom"][0]["concentration"], 314)
        self.assertEqual(chemicalCompositionMM["structure"]["chain"][0]["numberOfMonomers"], 764)
        self.assertEqual(chemicalCompositionMM["structure"]["chain"][0]["type"], "protein")

    def test_checkEstimateRadiationDamage(self):
        inData = {}
        listSubWedge = []
        self.assertFalse(Characterisation.checkEstimateRadiationDamage(inData))
        inData = {"diffractionPlan": {"estimateRadiationDamage": False}}
        self.assertFalse(Characterisation.checkEstimateRadiationDamage(inData))
        inData = {"diffractionPlan": {"estimateRadiationDamage": True}}
        self.assertTrue(Characterisation.checkEstimateRadiationDamage(inData))
        inData = {"diffractionPlan": {"strategyOption": "bla bla bla bla"}}
        self.assertFalse(Characterisation.checkEstimateRadiationDamage(inData))
        inData = {"diffractionPlan": {"strategyOption": "bla bla -DamPar bla bla"}}
        self.assertTrue(Characterisation.checkEstimateRadiationDamage(inData))
        inData = {"experimentalCondition": {"beam": {"flux": 1e12}}}
        self.assertTrue(Characterisation.checkEstimateRadiationDamage(inData))
