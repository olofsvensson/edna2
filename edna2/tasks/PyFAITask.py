

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
import pprint
import logging
import pathlib
import jsonschema
from datetime import datetime


from edna2.tasks.AbstractTask import AbstractTask
from edna2.utils import UtilsLogging
from edna2.utils import UtilsImage
from edna2.utils import UtilsDetector


__author__ = ['G. Santoni']
__license__ = 'MIT'
__date__ = '07/01/2022'

logger = UtilsLogging.getLogger()


class PyFAITask(AbstractTask):

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "listH5FilePath": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "doSubmit": {"type": "boolean"},
                'poni_file':{"type": "string"},
                "mask_file":{"type":"string"},
                "detectorType": {"type": "string"},                
                "detector_distance": {"type": "number"},
                "wavelength": {"type": "number"},
                "pixel_size":{"type":"number"},
                "orgx": {"type": "number"}, 
                "orgy": {"type": "number"},
                "isZigZag": {"type": "boolean"},
                "imageQualityIndicators": {
                    "type": "array",
                    "items": {
                        "$ref": self.getSchemaUrl("imageQualityIndicators.json")
                    }
                }
            },
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
    def run(self, inData):
        outdata = {}
        geometry = self.generatePoni(inData)
        with open(str(self.getWorkingDirectory() / 'experiment.poni'), 'w') as f:
            f.write(geometry)
        commandLine = self.generateCommand(inData)
        self.runCommandLine(commandLine)
    
    def generateCommand(self, inData):
        #this function prepares the command line to run peakfinder.
        #gets image, poni name  + other parameters to be determined
        shellCommand = 'peakfinder '
        shellCommand += '-p experiment.poni '
        shellCommand += 'inData["listH5FilePath"[0]]'
        return shellCommand

    def generatePoni(self, inData):
        #for the sake of uniformity, will need to calculate poni1 poni2 from orgx orgy from MXCUBE.
        detectorType = inData['detectorType']
        pixelSize = UtilsDetector.getPixelsize(detectorType)
        poni = '!\n'
        poni += 'PixelSize1: %d\n' %pixelSize
        poni += 'PixelSize2: %d\n' %pixelSize
        poni += 'Distance: {0}\n'.format(inData["detector_distance"])
        poni += 'Poni1: {0}\n'.format(inData['orgy'])
        poni += 'Poni2: {0}\n'.format(inData['orgx'])
        poni += 'Rot1: 0\n'
        poni += 'Rot2: 0\n'
        poni += 'Rot3: 0\n'
        return poni