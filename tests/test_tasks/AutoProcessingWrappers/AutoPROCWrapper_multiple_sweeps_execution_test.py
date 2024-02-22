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
__date__ = "21/02/2024"

import os
import pathlib
import unittest

from edna2.utils import UtilsLogging
from edna2.utils import UtilsTest

from edna2.tasks.AutoProcessingWrappers import AutoPROCWrapper

logger = UtilsLogging.getLogger()

class AutoPROCWrapperExecTest_single_sweep(unittest.TestCase):

    def test_execute_multiple_sweeps(self):
        in_data = {
            "fromN"
            "raw_data": [
                "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_07_datacollection",
                "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_09_datacollection",
                "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_11_datacollection",
                "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_13_datacollection",
            ]
        }
        autoProcessingWrappers = AutoPROCWrapper(inData=in_data)
        autoProcessingWrappers.execute()
        out_data = autoProcessingWrappers.outData
        assert out_data is not None

    # def tes_upload_autoPROC_to_icat():
    #     # tmp_path = pathlib.Path(tmpdir)
    #     # ispyb_xml = get_ispyb_xml()
    #     # working_dir = tmp_path / "nobackup"
    #     os.environ["EDNA2_SITE"] = "ESRF_ID30A1"
    #     processed_data_dir = pathlib.Path(
    #         "/data/visitor/mx2532/id30a1/20240220/PROCESSED_DATA/INS/INS-Helical_test1/run_01_MXPressA/autoprocessing_combined/autoPROC"
    #     )
    #     list_raw_dir = [
    #         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_07_datacollection",
    #         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_09_datacollection",
    #         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_11_datacollection",
    #         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_13_datacollection",
    #     ]
    #     AutoPROCWrapper.upload_autoPROC_to_icat(
    #         beamline="id30a1",
    #         proposal="mx2532",
    #         processName="autoPROC",
    #         list_raw_dir=list_raw_dir,
    #         processed_data_dir=processed_data_dir,
    #     )
