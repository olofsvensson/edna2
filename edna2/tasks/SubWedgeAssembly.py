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

from edna2.tasks.AbstractTask import AbstractTask
from edna2.tasks.ReadImageHeader import ReadImageHeader

from edna2.utils import UtilsLogging
from edna2.utils import UtilsSubWedge

logger = UtilsLogging.getLogger()


class SubWedgeAssembly(AbstractTask):

    def run(self, inData):
        sub_wedge_merge = []
        list_image_path = inData["imagePath"]
        if "fastCharacterisation" in inData:
            is_fast_characterisation = True
            list_subwedge_angles = inData["fastCharacterisation"]["listSubWedgeAngles"]
            no_images_in_subwedge = inData["fastCharacterisation"]["noImagesInSubWedge"]
        else:
            is_fast_characterisation = False
            list_subwedge_angles = None
            no_images_in_subwedge = None
        sub_wedge_number = 1
        input_read_image_header = {
            "imagePath": list_image_path
        }
        read_image_header = ReadImageHeader(inData=input_read_image_header)
        read_image_header.execute()
        if read_image_header.isSuccess():
            list_subwedge = read_image_header.outData["subWedge"]
            for index_subwedge, subwedge in enumerate(list_subwedge):
                if is_fast_characterisation:
                    # Modify the start angle
                    index_angle = int(index_subwedge / no_images_in_subwedge)
                    angle_subwedge = list_subwedge_angles[index_angle]
                    goniostat = subwedge["experimentalCondition"]["goniostat"]
                    goniostat["rotationAxisStart"] = (goniostat["rotationAxisStart"] + angle_subwedge) % 360
                    goniostat["rotationAxisEnd"] = (goniostat["rotationAxisEnd"] + angle_subwedge) % 360
                else:
                    subwedge["subWedgeNumber"] = index_subwedge + 1
            sub_wedge_merge = UtilsSubWedge.subWedgeMerge(list_subwedge)
        return sub_wedge_merge