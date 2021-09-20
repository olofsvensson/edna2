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

import pathlib
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

    def test_splitPrefixRunNumber(self):
        path = pathlib.Path("/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0001.cbf")
        pre_prefix, run_number = UtilsImage.splitPrefixRunNumber(path)
        self.assertEqual(pre_prefix, 'PsPL7C-252')
        self.assertEqual(run_number, 1)
        path = pathlib.Path("/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/Ps_PL_7C-2_52_1_0001.cbf")
        pre_prefix, run_number = UtilsImage.splitPrefixRunNumber(path)
        self.assertEqual(pre_prefix, 'Ps_PL_7C-2_52')
        self.assertEqual(run_number, 1)


    def tes_mergeCbfInDirectory(self):
        for number in range(8, 9):
            cbfDirectory = "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX{0}".format(number)
            UtilsImage.mergeCbfInDirectory(cbfDirectory)


    def tes_mergeCbf(self):
        listPath = [
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0001.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0002.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0003.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0004.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0005.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0006.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0007.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0008.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0009.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0010.cbf"
        ]
        outputPath = "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_3_0001.cbf"
        UtilsImage.mergeCbf(listPath, outputPath)
        listPath = [
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0450.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0451.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0452.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0453.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0454.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0455.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0456.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0457.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0458.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0459.cbf"
        ]
        outputPath = "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_3_0002.cbf"
        UtilsImage.mergeCbf(listPath, outputPath)
        listPath = [
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0900.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0901.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0902.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0903.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0904.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0905.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0906.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0907.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0908.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0909.cbf"
        ]
        outputPath = "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_3_0003.cbf"
        UtilsImage.mergeCbf(listPath, outputPath)
        listPath = [
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1350.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1351.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1352.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1353.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1354.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1355.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1356.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1357.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1358.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1359.cbf"
        ]
        outputPath = "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_3_0004.cbf"
        UtilsImage.mergeCbf(listPath, outputPath)
        listPath = [
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1800.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1801.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1802.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1803.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1804.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1805.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1806.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1807.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1808.cbf",
            "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_1809.cbf"
        ]
        outputPath = "/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_3_0005.cbf"
        UtilsImage.mergeCbf(listPath, outputPath)
