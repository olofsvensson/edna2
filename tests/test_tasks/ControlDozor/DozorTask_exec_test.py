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
__date__ = "21/04/2019"

import os
import shutil
import tempfile
import unittest

from edna2.tasks.ControlDozor import ExecDozor

from edna2.utils import UtilsTest
from edna2.utils import UtilsConfig


class ExecDozorTest(unittest.TestCase):
    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    @unittest.skipIf(
        UtilsConfig.getSite() == "Default", "Cannot run dozor test with default config"
    )
    def test_execute_Dozor(self):
        referenceDataPath = self.dataPath / "inDataDozor.json"
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        # 'Manually' load the 10 test images
        for imageNo in range(1, 11):
            fileName = "x_1_{0:04d}.cbf".format(imageNo)
            UtilsTest.loadTestImage(fileName)
        dozor = ExecDozor(inData=inData)
        dozor.execute()
        self.assertTrue(dozor.isSuccess())
        outData = dozor.outData
        self.assertEqual(len(outData["imageDozor"]), 10)

    @unittest.skipIf(
        UtilsConfig.getSite() == "Default", "Cannot run dozor test with default config"
    )
    def test_execute_Dozor_slurm(self):
        referenceDataPath = self.dataPath / "inDataDozor.json"
        in_data = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        # Use SLURM - use /tmp_14_days as working dir
        username = os.environ["USER"]
        working_dir = tempfile.mkdtemp(dir=f"/tmp_14_days/{username}", prefix="edna2_dozor_slurm_")
        in_data["doSubmit"] = True
        in_data["workingDirectory"] = working_dir
        # 'Manually' load the 10 test images
        for image_no in range(1, 11):
            file_name = "x_1_{0:04d}.cbf".format(image_no)
            UtilsTest.loadTestImage(file_name)
        dozor = ExecDozor(inData=in_data)
        dozor.execute()
        shutil.rmtree(working_dir)
        self.assertTrue(dozor.isSuccess())
        out_data = dozor.outData
        self.assertEqual(len(out_data["imageDozor"]), 10)

    @unittest.skipIf(
        UtilsConfig.getSite() == "Default",
        "Cannot run control dozor test with default config",
    )
    @unittest.skipIf(
        not os.path.exists(
            "/data/visitor/mx415/id30a3/20171127/"
            + "RAW_DATA/mx415/1-2-2/MXPressF_01/"
            + "mesh-mx415_1_1_master.h5"
        ),
        "Image /data/visitor/mx415/id30a3/20171127/RAW_DATA/mx415/"
        + "1-2-2/MXPressF_01/mesh-mx415_1_1_master.h5 doesn't exist",
    )
    def test_execute_ExecDozor_eiger4m(self):
        # UtilsConfig.setSite('esrf_ispyb_valid')
        referenceDataPath = self.dataPath / "ExecDozor_eiger4m.json"
        self.inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        dozor = ExecDozor(inData=self.inData)
        dozor.execute()
        self.assertTrue(dozor.isSuccess())
        outData = dozor.outData
        self.assertEqual(len(outData["imageDozor"]), 51)
