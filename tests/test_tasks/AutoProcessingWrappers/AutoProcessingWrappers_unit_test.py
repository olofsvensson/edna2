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
import pprint
import unittest

from edna2.utils import UtilsTest
from edna2.utils import UtilsLogging

from edna2.tasks.AutoProcessingWrappers import AutoPROCWrapper

logger = UtilsLogging.getLogger()


def get_ispyb_xml():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    auto_proc_xml_path = data_path / "autoPROC.xml"
    with open(auto_proc_xml_path) as f:
        ispyb_xml = f.read()
    return ispyb_xml


def test_copy_data_to_icat_dir(tmpdir):
    tmp_path = pathlib.Path(tmpdir)
    ispyb_xml = get_ispyb_xml()
    AutoPROCWrapper.copy_data_to_icat_dir(ispyb_xml=ispyb_xml, icat_dir=tmp_path)


def test_create_icat_metadata_from_ispyb_xml():
    ispyb_xml = get_ispyb_xml()
    icat_metadata = AutoPROCWrapper.create_icat_metadata_from_ispyb_xml(ispyb_xml)
    assert icat_metadata is not None
    pprint.pprint(icat_metadata)


def test_get_metadata():
    raw_data_path = "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_07_datacollection"
    metadata = AutoPROCWrapper.get_metadata(raw_data_path)
    pprint.pprint(metadata)

def test_wait_for_data_cbf():
    in_data = {
        "raw_data": [
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_07_datacollection",
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_09_datacollection",
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_11_datacollection",
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_13_datacollection",
        ]
    }
    is_success = AutoPROCWrapper.wait_for_data(in_data)
    assert is_success


# def test_wait_for_data_h5():
#     in_data = {
#         "raw_data": [
#             "/data/visitor/mx2112/id23eh1/20240130/RAW_DATA/Sample-8:2:08/run_01_MXPressF/run_01_04_datacollection",
#         ]
#     }
#     is_success = AutoPROCWrapper.wait_for_data(in_data)
#     assert is_success
