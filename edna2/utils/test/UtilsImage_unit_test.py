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



import unittest

from edna2.utils import UtilsImage


class UtilsImageUnitTest(unittest.TestCase):

    def setUp(self):
        self.imageFileName = "ref-testscale_1_0001.img"
        self.imageFileNameH5 = "mesh-local-user_0_1_000001.h5"

    def test_getPrefix(self):
        prefix = UtilsImage.getPrefix(self.imageFileName)
        self.assertEqual(prefix, "ref-testscale_1")

    def test_getPrefixH5(self):
        prefix = UtilsImage.getPrefix(self.imageFileNameH5)
        self.assertEqual(prefix, "mesh-local-user_0_1")

    def test_getImageNumber(self):
        imageNumber = UtilsImage.getImageNumber(self.imageFileName)
        self.assertEqual(imageNumber, 1)

    def test_getTemplateHash(self):
        template = UtilsImage.getTemplate(self.imageFileName)
        templateReference = "ref-testscale_1_####.img"
        self.assertEqual(templateReference, template)

    def test_getTemplateQuestionMark(self):
        template = UtilsImage.getTemplate(self.imageFileName, symbol="?")
        templateReference = "ref-testscale_1_????.img"
        self.assertEqual(templateReference, template)

    def test_getH5FilePath_ref(self):
        refH5Master1 = "ref-UPF2-UPF2__4_1_1_master.h5"
        refH5Data1 = "ref-UPF2-UPF2__4_1_1_data_000001.h5"
        file1 = "ref-UPF2-UPF2__4_1_0001.h5"
        h5MasterFilePath, h5DataFilePath, h5FileNumber = \
            UtilsImage.getH5FilePath(file1, hasOverlap=True)
        self.assertEqual(refH5Master1, str(h5MasterFilePath))
        self.assertEqual(refH5Data1, str(h5DataFilePath))

        refH5Master2 = "ref-UPF2-UPF2__4_1_2_master.h5"
        refH5Data2 = "ref-UPF2-UPF2__4_1_2_data_000001.h5"
        file2 = "ref-UPF2-UPF2__4_1_0002.h5"
        h5MasterFilePath, h5DataFilePath, h5FileNumber = \
            UtilsImage.getH5FilePath(file2, hasOverlap=True)
        self.assertEqual(refH5Master2, str(h5MasterFilePath))
        self.assertEqual(refH5Data2, str(h5DataFilePath))