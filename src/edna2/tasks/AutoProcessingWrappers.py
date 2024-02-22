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

import os
import json
import shutil
import pprint
import pathlib
import socket

import xmltodict

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsImage
from edna2.utils import UtilsPath
from edna2.utils import UtilsICAT
from edna2.utils import UtilsLogging
from edna2.utils import UtilsConfig

from pyicat_plus.client.main import IcatClient

logger = UtilsLogging.getLogger()


class AutoPROCWrapper(AbstractTask):

    def getInDataSchema(self):
        # 	dataCollectionId : XSDataInteger optional
        # 	icatProcessDataDir : XSDataFile optional
        # 	dirN : XSDataFile optional
        # 	templateN : XSDataString optional
        # 	fromN : XSDataInteger optional
        # 	toN : XSDataInteger optional
        # 	processDirectory : XSDataFile optional
        # 	doAnom : XSDataBoolean optional
        # 	doAnomAndNonanom : XSDataBoolean optional
        # 	symm : XSDataString optional
        # 	cell : XSDataString optional
        # 	reprocess : XSDataBoolean optional
        # 	lowResolutionLimit : XSDataDouble optional
        # 	highResolutionLimit : XSDataDouble optional
        # 	exclude_range : XSDataRange [] optional
        return {
            "type": "object",
            "properties": {
                "start_image_number": {"type": "number"},
                "end_image_number": {"type": "number"},
                "dataCollectionId": {"type": "number"},
                "icatProcessDataDir": {"type": "string"},
                "processDirectory": {"type": "string"},
                "doAnom": {"type": "boolean"},
                "doAnomAndNonanom": {"type": "boolean"},
                "symm": {"type": "string"},
                "cell": {"type": "string"},
                "reprocess": {"type": "boolean"},
                "lowResolutionLimit": {"type": "number"},
                "highResolutionLimit": {"type": "number"},
                "exclude_range": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "number",
                        },
                    },
                },
                "raw_data": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
        }

    def run(self, in_data):
        out_data = {}
        logger = UtilsLogging.getLogger()
        logger.info("Starting auto-processing with autoPROC")
        AutoPROCWrapper.host_info()
        # Wait for data files
        is_success = AutoPROCWrapper.wait_for_data(in_data)
        if not is_success:
            logger.error("One or several data files are missing")
            self.setFailure()
        else:
            logger.info("Setting ISPyB status to RUNNING")
            command_line = self.get_command_line(in_data)
            logger.info(command_line)
            # self.set_ispyb_status(status="RUNNING")
            self.runCommandLine(command_line)
            # if len(in_data["raw_data"]) == 1:
            #     logger.info("Processing single sweep")
            #     out_data = self.process_single_sweep(in_data)
            # else:
            #     logger.info("Processing multiple sweeps")
            #     out_data = self.process_multiple_sweeps(in_data)
            logger.info("Setting ISPyB status to FINISHED")
            # self.set_ispyb_status(status="FINISHED")
        return out_data

    def process_single_sweep(self, in_data, command_line):
        out_data = {}
        return out_data

    def process_multiple_sweeps(self, in_data):
        out_data = {}
        return out_data

    def get_command_line(self, in_data):
        rotation_axis = None
        scale_with_xscale = True
        nthreads = 20
        command_line = "process -B -xml"
        command_line += f" -nthreads {nthreads}"
        command_line += ' -M ReportingInlined autoPROC_HIGHLIGHT="no"'
        if scale_with_xscale:
            command_line += " autoPROC_ScaleWithXscale='yes'"
        if rotation_axis is not None:
            command_line += f' XdsFormatSpecificJiffyRun=no autoPROC_XdsKeyword_ROTATION_AXIS="{rotation_axis}"'
        # Make sure we only store PDF files in summary html file
        command_line += ' autoPROC_Summary2Base64_ConvertExtensions="pdf"'
        command_line += ' autoPROC_Summary2Base64_ModalExtensions="LP html log mrfana pdb stats table1 xml sca"'
        for raw_data in in_data["raw_data"]:
            metadata = AutoPROCWrapper.get_metadata(raw_data)
            template = metadata["MX_template"]
            start_image_number = in_data.get(
                "start_image_number", metadata["MX_startImageNumber"]
            )
            end_image_number = in_data.get(
                "end_image_number",
                metadata["MX_startImageNumber"] + metadata["MX_numberOfImages"] - 1,
            )
            if template.endswith(".h5"):
                autoPROC_template = template.replace("%04d", "1_master")
                prefix = "_".join(template.split("_")[:-2])
            else:
                autoPROC_template = template.replace("%04d", "####")
                prefix = "_".join(template.split("_")[:-1])
            command_line += f" -Id {prefix},{raw_data},{autoPROC_template},{start_image_number},{end_image_number}"
        # Resolution
        low_resolution_limit = in_data.get("lowResolutionLimit", None)
        high_resolution_limit = in_data.get("highResolutionLimit", None)
        if low_resolution_limit is not None or high_resolution_limit is not None:
            # See https://www.globalphasing.com/autoproc/manual/autoPROC4.html#processcli
            if low_resolution_limit is None:
                low_resolution_limit = 1000.0  # autoPROC default value
            if high_resolution_limit is None:
                high_resolution_limit = 0.1  # autoPROC default value
            command_line += " -R {0} {1}".format(
                low_resolution_limit, high_resolution_limit
            )
        # Anomalous
        anomalous = in_data.get("doAnom", True)
        if anomalous:
            command_line += " -ANO"
        # Reference MTZ file
        # refMTZ = in_data.get
        # if refMTZ is not None:
        #     command_line += " -ref {0}".format(refMTZ.path.value)
        # Forced space group
        symm = in_data.get("symm", None)
        if symm is not None:
            command_line += f" symm='{symm}'"
        # Forced cell
        cell = in_data.get("cell", None)
        if cell is not None:
            command_line += f" cell='{cell}'"
        return command_line

    @staticmethod
    def get_metadata(raw_data_path):
        if type(raw_data_path) == str:
            raw_data_path = pathlib.Path(raw_data_path)
        metadata_path = raw_data_path / "metadata.json"
        metadata = json.loads(open(metadata_path).read())
        # Start and end image number taking into account exclude ranges
        # start_image_number = metadata["MX_startImageNumber"]
        # end_image_number = start_image_number + metadata["MX_numberOfImages"] - 1
        # if "exclude_range" in in_data:
        #     for range in in_data["exclude_range"]:
        #         if range[0] <= start_image_number and range[0] >= end_image_number:
        #             pass
        return metadata

    @staticmethod
    def wait_for_data(in_data):
        logger = UtilsLogging.getLogger()
        list_raw_data = in_data["raw_data"]
        is_success = True
        for raw_data in list_raw_data:
            raw_data_path = pathlib.Path(raw_data)
            metadata = AutoPROCWrapper.get_metadata(raw_data_path)
            if metadata["MX_numberOfImages"] < 8:
                logger.error("There are fewer than 8 images, aborting")
                is_success = False
                break
            else:
                template = metadata["MX_template"]
                start_image_number = metadata["MX_startImageNumber"]
                end_image_number = (
                    start_image_number + metadata["MX_numberOfImages"] - 1
                )
                list_path = []
                if template.endswith(".h5"):
                    # Wait for master, first data and last data file
                    master_file_name = AutoPROCWrapper.eiger_template_to_master(
                        template
                    )
                    list_path.append(raw_data_path / master_file_name)
                    first_data_file_name = AutoPROCWrapper.eiger_template_to_data(
                        template, start_image_number
                    )
                    list_path.append(raw_data_path / first_data_file_name)
                    last_data_file_name = AutoPROCWrapper.eiger_template_to_data(
                        template, end_image_number
                    )
                    list_path.append(raw_data_path / last_data_file_name)
                elif template.endswith(".cbf"):
                    format_string = template.replace("####", "%04d")
                    first_file_name = format_string % start_image_number
                    list_path.append(raw_data_path / first_file_name)
                    last_file_name = format_string % end_image_number
                    list_path.append(raw_data_path / last_file_name)
                else:
                    raise RuntimeError(f"Unknown file type: {template}")
                for data_file in list_path:
                    has_timed_out, final_size = UtilsPath.waitForFile(data_file)
                    if has_timed_out:
                        is_success = False
        return is_success

    @staticmethod
    def eiger_template_to_data(template, image_number):
        file_number = int((image_number - 1) / 100) + 1
        format_string = template.replace("%04d", f"1_data_{file_number:06d}")
        return format_string.format(image_number)

    @staticmethod
    def eiger_template_to_master(template):
        format_string = template.replace("%04d", "1_master")
        return format_string

    @staticmethod
    def host_info():
        logger = UtilsLogging.getLogger()
        try:
            host_name = socket.gethostname()
            logger.info(f"Running on {host_name}")
            load_avg = os.getloadavg()
            logger.info("System load avg: {0}".format(load_avg))
        except OSError:
            pass

    @staticmethod
    def upload_autoPROC_to_icat(
        beamline, proposal, processName, list_raw_dir, processed_data_dir
    ):
        dataset_name = processName
        icat_dir = processed_data_dir / processName
        if not icat_dir.exists():
            icat_dir.mkdir(mode=0o755)
        working_dir = processed_data_dir / "nobackup"
        ispyb_xml_path = working_dir / f"{processName}.xml"
        if ispyb_xml_path.exists():
            with open(ispyb_xml_path) as f:
                ispyb_xml = f.read()
            AutoPROCWrapper.copy_data_to_icat_dir(
                ispyb_xml=ispyb_xml, icat_dir=icat_dir
            )
            metadata = AutoPROCWrapper.create_icat_metadata_from_ispyb_xml(
                ispyb_xml=ispyb_xml
            )
            icat_beamline = UtilsICAT.getIcatBeamline(beamline)
            logger.debug(f"ICAT beamline name: {icat_beamline}")
            if icat_beamline is not None:
                dict_config = UtilsConfig.getTaskConfig("ICAT")
                metadata_urls = json.loads(dict_config.get("metadata_urls", "[]"))
                logger.debug(metadata_urls)
                if len(metadata_urls) > 0:
                    client = IcatClient(metadata_urls=metadata_urls)
                    # Get the sample name
                    first_raw_dir = pathlib.Path(list_raw_dir[0])
                    raw_metadata_path = first_raw_dir / "metadata.json"
                    sample_name = UtilsICAT.get_sample_name(raw_metadata_path)
                    metadata["Sample_name"] = sample_name
                    metadata["scanType"] = "integration"
                    metadata["Process_program"] = processName
                    logger.debug("Before store")
                    logger.debug(f"icat_beamline {icat_beamline}")
                    logger.debug(f"proposal {proposal}")
                    logger.debug(f"dataset_name {dataset_name}")
                    logger.debug(f"icat_dir {icat_dir}")
                    logger.debug(f"metadata {pprint.pformat(metadata)}")
                    logger.debug(f"raw {list_raw_dir}")
                    reply = client.store_processed_data(
                        beamline=icat_beamline,
                        proposal=proposal,
                        dataset=dataset_name,
                        path=str(icat_dir),
                        metadata=metadata,
                        raw=list_raw_dir,
                    )
                    logger.debug(reply)
                    logger.debug("After store")

    @staticmethod
    def copy_data_to_icat_dir(ispyb_xml, icat_dir):
        dict_ispyb = xmltodict.parse(ispyb_xml)
        autoProcContainer = dict_ispyb["AutoProcContainer"]
        autoProcProgramContainer = autoProcContainer["AutoProcProgramContainer"]
        list_program_attachment = autoProcProgramContainer["AutoProcProgramAttachment"]
        for program_attachment in list_program_attachment:
            file_name = program_attachment["fileName"]
            file_path = program_attachment["filePath"]
            shutil.copy(os.path.join(file_path, file_name), icat_dir)

    @staticmethod
    def create_icat_metadata_from_ispyb_xml(ispyb_xml):
        dict_ispyb = xmltodict.parse(ispyb_xml)
        # Meta-data
        metadata = {}
        autoProcContainer = dict_ispyb["AutoProcContainer"]
        autoProc = autoProcContainer["AutoProc"][0]
        autoProcScalingContainer = autoProcContainer["AutoProcScalingContainer"][0]
        if "autoProcIntegrationContainer" in autoProcScalingContainer:
            autoProcIntegrationContainer = autoProcScalingContainer[
                "autoProcIntegrationContainer"
            ]
            autoProcIntegration = autoProcIntegrationContainer["AutoProcIntegration"]
            if autoProcIntegration["anomalous"]:
                metadata["MXAutoprocIntegration_anomalous"] = 1
            else:
                metadata["MXAutoprocIntegration_anomalous"] = 0
        else:
            autoProcIntegrationContainer = None
            autoProcIntegration = None
        metadata["MXAutoprocIntegration_space_group"] = autoProc["spaceGroup"]
        if "refinedCell_a" in autoProc and autoProc["refinedCell_a"] is not None:
            metadata["MXAutoprocIntegration_cell_a"] = autoProc["refinedCell_a"]
            metadata["MXAutoprocIntegration_cell_b"] = autoProc["refinedCell_b"]
            metadata["MXAutoprocIntegration_cell_c"] = autoProc["refinedCell_c"]
            metadata["MXAutoprocIntegration_cell_alpha"] = autoProc["refinedCell_alpha"]
            metadata["MXAutoprocIntegration_cell_beta"] = autoProc["refinedCell_beta"]
            metadata["MXAutoprocIntegration_cell_gamma"] = autoProc["refinedCell_gamma"]
        elif autoProcIntegration is not None:
            metadata["MXAutoprocIntegration_cell_a"] = autoProcIntegration["cell_a"]
            metadata["MXAutoprocIntegration_cell_b"] = autoProcIntegration["cell_b"]
            metadata["MXAutoprocIntegration_cell_c"] = autoProcIntegration["cell_c"]
            metadata["MXAutoprocIntegration_cell_alpha"] = autoProcIntegration[
                "cell_alpha"
            ]
            metadata["MXAutoprocIntegration_cell_beta"] = autoProcIntegration[
                "cell_beta"
            ]
            metadata["MXAutoprocIntegration_cell_gamma"] = autoProcIntegration[
                "cell_gamma"
            ]

        for autoProcScalingStatistics in autoProcScalingContainer[
            "AutoProcScalingStatistics"
        ]:
            statistics_type = autoProcScalingStatistics["scalingStatisticsType"]
            icat_stat_name = statistics_type.replace("Shell", "")
            metadata[f"MXAutoprocIntegrationScaling_{icat_stat_name}_completeness"] = (
                autoProcScalingStatistics["completeness"]
            )
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_anomalous_completeness"
            ] = autoProcScalingStatistics["anomalousCompleteness"]
            metadata[f"MXAutoprocIntegrationScaling_{icat_stat_name}_multiplicity"] = (
                autoProcScalingStatistics["multiplicity"]
            )
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_anomalous_multiplicity"
            ] = autoProcScalingStatistics["anomalousMultiplicity"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_resolution_limit_low"
            ] = autoProcScalingStatistics["resolutionLimitLow"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_resolution_limit_high"
            ] = autoProcScalingStatistics["resolutionLimitHigh"]
            metadata[f"MXAutoprocIntegrationScaling_{icat_stat_name}_r_merge"] = (
                autoProcScalingStatistics["rMerge"]
            )
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_r_meas_within_IPlus_IMinus"
            ] = autoProcScalingStatistics["rMeasWithinIPlusIMinus"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_r_meas_all_IPlus_IMinus"
            ] = autoProcScalingStatistics["rMeasAllIPlusIMinus"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_r_pim_within_IPlus_IMinus"
            ] = autoProcScalingStatistics["rPimWithinIPlusIMinus"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_r_pim_all_IPlus_IMinus"
            ] = autoProcScalingStatistics["rPimAllIPlusIMinus"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_mean_I_over_sigI"
            ] = autoProcScalingStatistics["meanIOverSigI"]
            metadata[f"MXAutoprocIntegrationScaling_{icat_stat_name}_cc_half"] = (
                autoProcScalingStatistics["ccHalf"]
            )
            if "ccAno" in autoProcScalingStatistics:
                metadata[f"MXAutoprocIntegrationScaling_{icat_stat_name}_cc_ano"] = (
                    autoProcScalingStatistics["ccAno"]
                )
        return metadata
