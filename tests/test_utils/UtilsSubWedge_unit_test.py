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
__date__ = "29/03/2022"


import json
import pathlib
import unittest

from edna2.utils import UtilsSubWedge
from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


class UtilsSubWegdeUnitTest(unittest.TestCase):

    def getTestExperimentalCondition(self):
        data_path = pathlib.Path(__file__).parent / "data"
        test_file_path = data_path / "experimentalCondition.json"
        exp_cond = json.loads(open(test_file_path).read())
        return exp_cond

    def getTestListSubWedge(self):
        data_path = pathlib.Path(__file__).parent / "data"
        test_file_path = data_path / "listSubWedge.json"
        list_sub_wedge = json.loads(open(test_file_path).read())
        return list_sub_wedge

    def getTestListOf10SubWedges(self):
        data_path = pathlib.Path(__file__).parent / "data"
        test_file_path = data_path / "listOf10SubWedges.json"
        list_sub_wedge = json.loads(open(test_file_path).read())
        return list_sub_wedge

    def testCompareTwoValues(self):
        self.assertTrue(UtilsSubWedge.compareTwoValues(1, 1))
        self.assertFalse(UtilsSubWedge.compareTwoValues(1, 2))
        self.assertTrue(UtilsSubWedge.compareTwoValues(1.0, 1.0))
        self.assertFalse(UtilsSubWedge.compareTwoValues(1.0, 1.01))
        self.assertTrue(UtilsSubWedge.compareTwoValues(1.0, 1.01, 0.1))
        self.assertTrue(UtilsSubWedge.compareTwoValues("EDNA", "EDNA"))
        self.assertFalse(UtilsSubWedge.compareTwoValues("EDNA", "DNA"))
        # Comparison of two different types should raise an exception
        try:
            bTmp = UtilsSubWedge.compareTwoValues("EDNA", 1)
            raise RuntimeError("Problem - exception not raised")
        except:
            self.assertTrue(True)
        # Comparison of anything but double, int or string should raise an exception
        try:
            bTmp = UtilsSubWedge.compareTwoValues([1], [1])
            raise RuntimeError("Problem - exception not raised")
        except:
            self.assertTrue(True)

    def testIsSameExperimentalCondition(self):
        exp_cond_ref = self.getTestExperimentalCondition()
        exp_cond_same_as_ref = self.getTestExperimentalCondition()
        self.assertTrue(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_same_as_ref))
        exp_cond_different_exp_time = self.getTestExperimentalCondition()
        exp_cond_different_exp_time["beam"]["exposureTime"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_exp_time))
        exp_cond_different_wavelength = self.getTestExperimentalCondition()
        exp_cond_different_wavelength["beam"]["wavelength"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_wavelength))
        exp_cond_different_beam_position_x = self.getTestExperimentalCondition()
        exp_cond_different_beam_position_x["detector"]["beamPositionX"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_beam_position_x))
        exp_cond_different_beam_position_y = self.getTestExperimentalCondition()
        exp_cond_different_beam_position_y["detector"]["beamPositionY"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_beam_position_y))
        exp_cond_different_distance = self.getTestExperimentalCondition()
        exp_cond_different_distance["detector"]["distance"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_distance))
        exp_cond_different_name = self.getTestExperimentalCondition()
        exp_cond_different_name["detector"]["name"] = "EDNA"
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_name))
        exp_cond_different_number_pixel_x = self.getTestExperimentalCondition()
        exp_cond_different_number_pixel_x["detector"]["numberPixelX"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_number_pixel_x))
        exp_cond_different_number_pixel_y = self.getTestExperimentalCondition()
        exp_cond_different_number_pixel_y["detector"]["numberPixelY"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_number_pixel_y))
        exp_cond_different_serial_number = self.getTestExperimentalCondition()
        exp_cond_different_serial_number["detector"]["serialNumber"] = "EDNA"
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_serial_number))
        exp_cond_different_two_theta = self.getTestExperimentalCondition()
        exp_cond_different_two_theta["detector"]["twoTheta"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_two_theta))
        exp_cond_different_oscillation_width = self.getTestExperimentalCondition()
        exp_cond_different_oscillation_width["goniostat"]["oscillationWidth"] += 1
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_oscillation_width))
        exp_cond_different_rotation_axis = self.getTestExperimentalCondition()
        exp_cond_different_rotation_axis["goniostat"]["rotationAxis"] = "EDNA"
        self.assertFalse(UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_different_rotation_axis))


    def testSortIdenticalObjects(self):
        listObjects = []
        listSorted = UtilsSubWedge.sortIdenticalObjects(listObjects, UtilsSubWedge.compareTwoValues)
        self.assertEqual(listSorted, [])
        listObjects = [ 1 ]
        listSorted = UtilsSubWedge.sortIdenticalObjects(listObjects, UtilsSubWedge.compareTwoValues)
        self.assertEqual(listSorted, [[1]])
        listObjects = [ 1, 2 ]
        listSorted = UtilsSubWedge.sortIdenticalObjects(listObjects, UtilsSubWedge.compareTwoValues)
        self.assertEqual(listSorted, [[1], [2]])
        listObjects = [ 1, 1 ]
        listSorted = UtilsSubWedge.sortIdenticalObjects(listObjects, UtilsSubWedge.compareTwoValues)
        self.assertEqual(listSorted, [[1, 1]])
        listObjects = [ 1, 2, 1, 3, 4, 1, 5, 2, 2, 9, 3, 2]
        listSorted = UtilsSubWedge.sortIdenticalObjects(listObjects, UtilsSubWedge.compareTwoValues)
        self.assertEqual(listSorted, [[1, 1, 1], [2, 2, 2, 2], [3, 3], [4], [5], [9]])


    def testSortSubWedgesOnExperimentalCondition(self):
        # First check two sub wedges with identical experimental conditions
        list_sub_wedge = self.getTestListSubWedge()
        list_sub_wedge_sorted = UtilsSubWedge.sortSubWedgesOnExperimentalCondition(list_sub_wedge)
        # Check that we got a list with one element
        self.assertEqual(len(list_sub_wedge_sorted), 1)
        # Then modify one sub wedge
        list_sub_wedge_modified = self.getTestListSubWedge()
        list_sub_wedge_modified[1]["experimentalCondition"]["detector"]["distance"] += 100.0
        listSubWedgeSorted = UtilsSubWedge.sortSubWedgesOnExperimentalCondition(list_sub_wedge_modified)
        # Check that we got a list with two elements
        self.assertEqual(len(list_sub_wedge_modified), 2)


    def testMergeTwoSubWedgesAdjascentInRotationAxis(self):
        # First check two sub wedges which shouldn't be merged
        list_sub_wedge = self.getTestListSubWedge()
        sub_wedge_1 = list_sub_wedge[0]
        sub_wedge_2 = list_sub_wedge[1]
        sub_wedge_2["experimentalCondition"]["detector"]["distance"] += 100.0
        sub_wedge_should_not_be_merged = UtilsSubWedge.mergeTwoSubWedgesAdjascentInRotationAxis(sub_wedge_1, sub_wedge_2)
        self.assertIsNone(sub_wedge_should_not_be_merged)
        # Then check two adjascent images
        list_sub_wedge = self.getTestListSubWedge()
        sub_wedge_1 = list_sub_wedge[0]
        sub_wedge_2 = list_sub_wedge[1]
        sub_wedge_merged = UtilsSubWedge.mergeTwoSubWedgesAdjascentInRotationAxis(sub_wedge_1, sub_wedge_2)
        self.assertEqual(len(sub_wedge_merged["image"]), 2)


    def testMergeListOfSubWedgesWithAdjascentRotationAxis(self):
        # Check a list of ten adjascent images
        list_of_10_sub_wedges = self.getTestListOf10SubWedges()
        sub_wedge_merged = UtilsSubWedge.mergeListOfSubWedgesWithAdjascentRotationAxis(list_of_10_sub_wedges)
        self.assertEqual(len(sub_wedge_merged[0]["image"]), 10)
