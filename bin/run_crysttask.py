#!/usr/bin/env python3
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

__authors__ = ["S. Basu"]
__license__ = "MIT"
__date__ = "26/04/2023"

import os
import sys
import json
import pathlib
import argparse
from edna2.tasks.CrystfelTasks import ExeCrystFEL 

def optparser():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_directory", type=str, required=True,
                        help="provide path MeshScan, containing images in cbf or h5 formats")
    parser.add_argument("--detectorType", type=str, required=True,
                        help="provide detector type, either pilatus or eiger")
    parser.add_argument("--prefix", type=str, required=True,
                        help="filename prefix, a wildcard to look for files")
    parser.add_argument("--suffix", type=str, required=True,
                        help="image fileformat, either cbf, h5, or cxi")
    parser.add_argument("--batchSize", type=int, required=True,
                        help="max number of images per batch")
    parser.add_argument("--num_processors", type=str, default='20')
    parser.add_argument("--beamline", type=str,
                        help="optional key, not needed")
    parser.add_argument("--processing_directory", type=str,
                        help="optional key, if you want to dump at a different folder")
    parser.add_argument("--doMerging", type=bool, default=False)
    parser.add_argument("--doSubmit", type=bool, default=True)
    parser.add_argument("--partition", type=str, default="low")
    parser.add_argument("--GeneratePeaklist", type=bool, default=False)
    parser.add_argument("--indexing_method", type=str, default="xgandalf,mosflm",
                        help="change to asdf,or dirax or xds if needed")
    parser.add_argument("--peak_search", type=str, default="peakfinder8",
                        help="alternatively, peakfinder9 can be tried")
    parser.add_argument("--peak_info", type=str, default="/data/peakinfo")
    parser.add_argument("--int_method", type=str, default='rings-grad')
    parser.add_argument("--int_radius", type=str, default='3,4,6')
    parser.add_argument("--min_peaks", type=str, default='30')
    parser.add_argument("--peak_radius", type=str, default='3,4,6')
    parser.add_argument("--min_snr", type=str, default='4.0')
    parser.add_argument("--threshold", type=str, default='10')
    parser.add_argument("--local_bg_radius", type=str, default='10')
    parser.add_argument("--min_res", type=str, default='80',
                        help="Applied to avoid regions near beamstop in peak search")
    parser.add_argument("--max_res", type=str, default='1200',
                        help="Applied to avoid regions near beamstop in peak search")
    parser.add_argument("--highres", type=str, default='0.0')
    parser.add_argument("--unit_cell_file", type=str,
                        help="optional key, if you want to index with a given unit-cell")
    parser.add_argument("--geometry_file", type=str,
                        help="optional key, only if you have a better detector geometry file")

    args = parser.parse_args()
    return args

def inData_generate():
    op = optparser()
    input_Dict = dict()
    inData = dict()
    for k, v in op.__dict__.items():
        if v is not None:
            input_Dict[k] = v
        else:
            pass
    for k, v in input_Dict.items():
        if k != "image_directory":
             inData[k] = v
        else:
            pass
    
    
    datadir = pathlib.Path(input_Dict["image_directory"])
    listofimagefiles = list(datadir.glob(input_Dict['prefix'] + '*' + input_Dict['suffix']))
    inData["listH5FilePath"] = []

    for fname in listofimagefiles:
        inData["listH5FilePath"].append(fname.as_posix())

    jh = open("input.json", "w")
    jh.write(json.dumps(inData, default=str, indent=4))
    jh.close()
    return inData


if __name__ == '__main__':
   
   inData = inData_generate()
   crystfel = ExeCrystFEL(inData)

   crystfel.executeRun()
   if crystfel.isFailure():
       logger.error("Error when executing {0}!".format("crystfel task"))
   else:
       print(crystfel.outData)
        
