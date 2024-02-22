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

from edna2.tasks.AutoProcessingWrappers import AutoProcessingWrappers

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
    AutoProcessingWrappers.copy_data_to_icat_dir(
        ispyb_xml=ispyb_xml,
        icat_dir=tmp_path
    )



def test_create_icat_metadata_from_ispyb_xml():
    ispyb_xml = get_ispyb_xml()
    icat_metadata = AutoProcessingWrappers.create_icat_metadata_from_ispyb_xml(
        ispyb_xml
    )
    assert icat_metadata is not None
    pprint.pprint(icat_metadata)

def test_upload_autoPROC_to_icat():
    # tmp_path = pathlib.Path(tmpdir)
    # ispyb_xml = get_ispyb_xml()
    # working_dir = tmp_path / "nobackup"
    os.environ["EDNA2_SITE"] = "ESRF_ID30A1"
    processed_data_dir = pathlib.Path("/data/visitor/mx2532/id30a1/20240220/PROCESSED_DATA/INS/INS-Helical_test1/run_01_MXPressA/autoprocessing_combined/autoPROC")
    list_raw_dir = [
        "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_07_datacollection",
        "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_09_datacollection",
        "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_11_datacollection",
        "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_13_datacollection"
    ]
    AutoProcessingWrappers.upload_autoPROC_to_icat(
        beamline="id30a1",
        proposal="mx2532",
        processName="autoPROC",
        list_raw_dir=list_raw_dir,
        processed_data_dir=processed_data_dir,
    )