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

import autocryst.saveDozor as sd
from autocryst.Image import ImageHandler as Im
from autocryst import run_crystfel

from edna2.tasks.AbstractTask import AbstractTask
from edna2.utils import UtilsLogging
from edna2.utils import UtilsImage

__authors__ = ["S. Basu", "Olof Svensson"]
__license__ = "MIT"
__date__ = "05/07/2019"

logger = UtilsLogging.getLogger()


class ExeCrystFEL(AbstractTask):
    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "listH5FilePath": {"type": "array", "items": {"type": "string"}},
                "doCBFtoH5": {"type": "boolean"},
                "doSubmit": {"type": "boolean"},
                "detectorType": {"type": "string"},
                "batchSize": {"type": "integer"},
                "cbfFileInfo": {
                    "directory": {"type": "string"},
                    "template": {"type": "string"},
                    "startNo": {"type": "integer"},
                    "endNo": {"type": "integer"},
                    "batchSize": {"type": "integer"},
                    "listofImages": {"type": "array", "items": {"type": "string"}},
                },
                "imageQualityIndicators": {
                    "type": "array",
                    "items": {"$ref": self.getSchemaUrl("imageQualityIndicators.json")},
                },
            },
            "oneOf": [{"required": ["listH5FilePath"]}, {"required": ["cbfFileInfo"]}],
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "data_directory": {"type": "string"},
                "streamfile": {"type": "string"},
                "centering": {"type": "string"},
                "num_indexed_frames": {"type": "integer"},
                "lattice": {"type": "string"},
                "unique_axis": {"type": "string"},
                "unit_cell": {
                    "type": "array",
                    "items": {"type": "number"},
                },
                "point_group": {"type": "string"},
                "space_group": {"type": "string"},
                "resolution_limit": {"type": "number"},
                "average_num_spots": {"type": "number"},
            },
        }

    def run(self, inData):
        # Determine data diretcory
        if "listH5FilePath" in inData:
            data_directory = os.path.dirname(inData["listH5FilePath"][0])
        elif "cbfFileInfo" in inData:
            data_directory = inData["cbfFileInfo"]["directory"]
        else:
            raise RuntimeError("No data source found inData")
        doCBFtoH5 = inData.get("doCBFtoH5", False)

        outData = {}
        if doCBFtoH5:
            dd = sd.Dozor(inData)
            dd.extract_olof_json(inData)

            headerfile = self.getWorkingDirectory() / "headers.json"
            if dd.is_success():
                os.chdir(str(self.getWorkingDirectory()))
                if not headerfile.exists():
                    with open(str(headerfile), "w") as jhead:
                        json.dump(dd.cbfheader, jhead, sort_keys=True, indent=2)
                else:
                    pass

                if dd.stacklength <= 100:
                    dd.create_stack()
                else:
                    dd.mp_stack()

                outData = self.exeIndexing(inData)
            else:
                self.setFailure()
                logger.error(
                    "CrystFEL Task failed due to failure of dozor packing into cxi"
                )
        else:
            os.chdir(self.getWorkingDirectory())
            streampath, results = self.exeIndexing(inData)
            if streampath.exists():
                outData = results
                outData["streamfile"] = str(streampath)
                outData["data_directory"] = data_directory

            else:
                self.isFailure()
                logger.error("AutoCryst returned empty stream file")
        return outData

    def exeIndexing(self, inData):
        doCBFtoH5 = inData.get("doCBFtoH5", False)
        in_for_crystfel = dict()

        if "listH5FilePath" in inData.keys():
            tmp = UtilsImage.getPrefix(inData["listH5FilePath"][0])
            in_for_crystfel["prefix"] = tmp
            in_for_crystfel["detectorType"] = inData.get("detectorType", "jungfrau")
            if inData.get("detectorType", "jungfrau") == "eiger":
                in_for_crystfel["prefix"] = tmp.strip("data")
                in_for_crystfel["maxchunksize"] = 10
                FirstImage = tmp.replace("data", "master.h5")
                Image = Im(FirstImage)
                in_for_crystfel["detectorType"] = (
                    Image.imobject.headers["detector_name"][0]
                    + Image.imobject.headers["detector_name"][1]
                )
            else:
                in_for_crystfel["geometry_file"] = inData["geometry_file"]
                in_for_crystfel["threshold"] = inData.get("threshold", "1000")
                in_for_crystfel["peak_radius"] = inData.get("peak_radius", "4,5,10")
                in_for_crystfel["int_radius"] = inData.get("int_radius", "4,5,10")
                in_for_crystfel["min_snr"] = inData.get("min_snr", "5.0")
                in_for_crystfel["min_peaks"] = inData.get("min_peaks", "20")
                in_for_crystfel["max_res"] = inData.get("max_res", "1200")
                in_for_crystfel["partition"] = inData.get("partition", "mx-low")
                in_for_crystfel["unit_cell_file"] = inData.get("unit_cell_file", " ")

            in_for_crystfel["suffix"] = UtilsImage.getSuffix(
                inData["listH5FilePath"][0]
            )
            in_for_crystfel["image_directory"] = str(
                pathlib.Path(inData["listH5FilePath"][0]).parent
            )
            in_for_crystfel["maxchunksize"] = inData.get("batchSize", 300)

        elif "cbfFileInfo" in inData.keys():
            in_for_crystfel["maxchunksize"] = inData["cbfFileInfo"].get("batchSize", 10)
            in_for_crystfel["listofImages"] = inData["cbfFileInfo"].get(
                "listofImages", []
            )
            in_for_crystfel["image_directory"] = inData["cbfFileInfo"]["directory"]
            in_for_crystfel["prefix"] = inData["cbfFileInfo"]["template"].strip(
                "####.cbf"
            )
            in_for_crystfel["suffix"] = UtilsImage.getSuffix(
                inData["cbfFileInfo"]["template"]
            )
            if len(in_for_crystfel["listofImages"]) == 0:
                in_for_crystfel["ImageRange"] = (
                    inData["cbfFileInfo"]["startNo"],
                    inData["cbfFileInfo"]["endNo"],
                )
                FirstImage = os.path.join(
                    inData["cbfFileInfo"]["directory"],
                    inData["cbfFileInfo"]["template"].replace("####", "0001"),
                )
            else:
                FirstImage = in_for_crystfel["listofImages"][0]

            Image = Im(FirstImage)
            in_for_crystfel["detectorType"] = (
                Image.imobject.headers["detector_name"][0]
                + Image.imobject.headers["detector_name"][1]
            )
        else:
            logger.error("input json must have either listH5FilePath or cbfFileInfo")

        if doCBFtoH5:
            cxi_all = list(self.getWorkingDirectory().glob("dozor*cxi"))
            current = len(cxi_all) - 1
            in_for_crystfel["image_directory"] = self.getWorkingDirectory()
            in_for_crystfel["prefix"] = "dozor_%d." % current
            in_for_crystfel["suffix"] = "cxi"
            in_for_crystfel["peak_search"] = "cxi"
            in_for_crystfel["peak_info"] = "/data/peakinfo"
            in_for_crystfel["maxchunksize"] = 10

        in_for_crystfel["doSubmit"] = inData.get("doSubmit", True)

        crysttask = run_crystfel.AutoCrystFEL(in_for_crystfel)
        outstream = None
        results = dict()
        try:
            jsonschema.validate(
                instance=crysttask.jshandle, schema=crysttask.getInDataSchema()
            )
            crysttask.run_indexing()
            if crysttask.is_executable("sbatch"):
                crysttask.combine_streams()
            else:
                pass

            outstream = crysttask.getOutputDirectory() / "alltogether.stream"
            results["QualityMetrics"] = crysttask.report_stats(str(outstream))
            print(results)
            crysttask.writeOutputData(results)
            '''
            crysttask.datafinder()
            crysttask.makeOutputDirectory()
            kk = {}
            if crysttask.jshandle['suffix'] == 'cxi':
                kk['cxi'] = """dim0 = %\ndim1 = ss\ndim2 = fs\ndata = /data/data\n"""
                geomfile = crysttask.make_geometry_file(**kk)
            else:
                geomfile = crysttask.make_geometry_file(**kk)
            print(geomfile)
            crysttask.make_list_events(str(geomfile))
            infile = str(crysttask.getOutputDirectory() / 'input.lst')
            outname = datetime.now().strftime('%H-%M-%S.stream')
            outstream = str(crysttask.getOutputDirectory() / outname)

            ofh = open(infile, 'w')
            for fname in crysttask.filelist:
                ofh.write(fname)
                ofh.write('\n')
            ofh.close()
            crystfel_cmd = crysttask.indexamajig_cmd(infile, outstream, geomfile)
            self.runCommandLine(crystfel_cmd, doSubmit=inData.get('doSubmit', True))
            '''
        except Exception as err:
            self.setFailure()
            logger.error(err)

        return outstream, results


class CrystFEL2ISPyB(AbstractTask):
    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "streamfile": {"type": "string"},
                "centering": {"type": "string"},
                "num_indexed_frames": {"type": "integer"},
                "lattice": {"type": "string"},
                "unique_axis": {"type": "string"},
                "unit_cell": {
                    "type": "array",
                    "items": {"type": "number"},
                },
                "point_group": {"type": "string"},
                "space_group": {"type": "string"},
                "resolution_limit": {"type": "number"},
                "average_num_spots": {"type": "number"},
            },
        }

    def getOutDataSchema(self):
        return {"type": "object", "properties": {"status": {"type": "string"}}}

    def run(self, inData):
        qm = inData["QualityMetrics"]
        # Create ssx_cells.json
        ssx_cells = {"unit_cells": qm["unit_cell_array"]}
        working_dir = self.getWorkingDirectory()
        ssx_cells_path = working_dir / "ssx_cells.json"
        with open(ssx_cells_path, "w") as f:
            f.write(json.dumps(ssx_cells, indent=4))
        # Create ssx_stats.json
        ssx_stats = {
            "nbHits": qm["number_hits"],
            "nbIndexed": qm["num_indexed_frames"],
            "laticeType": qm["lattice"],
            "estimatedResolution": qm["resolution_limit"],
        }
        ssx_stats_path = working_dir / "ssx_stats.json"
        with open(ssx_stats_path, "w") as f:
            f.write(json.dumps(ssx_stats, indent=4))
        # Create pyarch directory

        out_data = {
            "status": "ok"
        }
        return out_data


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s%(message)s",
        datefmt="%y-%m-%d %H:%M",
        filename="autocryst.log",
        filemode="a+",
    )
    fh = open(sys.argv[1], "r")
    inData = json.load(fh)
    fh.close()
    crystfel = ExeCrystFEL(inData)

    crystfel.executeRun()
    print(crystfel.outData)
