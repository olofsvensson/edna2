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
__date__ = "21/02/2024"

import json
import pathlib

from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


def get_sample_name(directory):
    path_directory = pathlib.Path(str(directory))
    metadata_path = path_directory / "metadata.json"
    sample_name = None
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.loads(f.read())
        if "Sample_name" in metadata:
            sample_name = metadata["Sample_name"]
    if sample_name is None:
        dir1 = path_directory.parent
        if dir1.name.startswith("run"):
            dir2 = dir1.parent
            if dir2.name.startswith("run"):
                sample_name = dir2.parent.name
            else:
                sample_name = dir2.name
        else:
            sample_name = dir1.name
    return sample_name


def getIcatBeamline(beamline):
    dict_beamline = {
        "id23eh1": "ID23-1",
        "id23eh2": "ID23-2",
        "id30a1": "ID30A-1",
        "id30a2": "ID30A-2",
        "id30a3": "ID30A-3",
        "id30b": "ID30b",
        "bm07": "BM07",
    }
    icat_beamline = dict_beamline.get(beamline, None)
    return icat_beamline
