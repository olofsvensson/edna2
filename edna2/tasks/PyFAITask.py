

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

from __future__ import division, print_function
import os
import sys
import json
import logging
import pathlib
import jsonschema
from datetime import datetime


from edna2.tasks.AbstractTask import AbstractTask
from edna2.utils import UtilsLogging
from edna2.utils import UtilsImage

__author__ = ['G. Santoni']
__license__ = 'MIT'
__date__ = '07/01/2022'

logger = UtilsLogging.getLogger()


class ExeCrystFEL(AbstractTask):

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "listH5FilePath": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "doCBFtoH5": {"type": "boolean"},
                "doSubmit": {"type": "boolean"},
                "cbfFileInfo": {
                    "directory": {"type": "string"},
                    "template": {"type": "string"},
                    "startNo": {"type": "integer"},
                    "endNo": {"type": "integer"},
                    "batchSize": {"type": "integer"},
                    "listofImages": {"type": "array",
                                     "items": {
                                         "type": "string"
                                          }
                                     },
                },
                "imageQualityIndicators": {
                    "type": "array",
                    "items": {
                        "$ref": self.getSchemaUrl("imageQualityIndicators.json")
                    }
                }
            },
            "oneOf": [
                {"required": ["listH5FilePath"]},
                {"required": ['cbfFileInfo']}
            ]
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "processedFile": {"type": "string"},
                "centering": {"type": "string"},
                "num_hit_frames": {"type": "integer"},
                "resolution_limit": {"type": "number"},
                "average_num_spots": {"type": "number"}
            }
        }