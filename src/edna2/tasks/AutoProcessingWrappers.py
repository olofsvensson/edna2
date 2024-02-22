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
import xmltodict

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsICAT
from edna2.utils import UtilsLogging
from edna2.utils import UtilsConfig

from pyicat_plus.client.main import IcatClient

logger = UtilsLogging.getLogger()


class AutoProcessingWrappers(AbstractTask):

    @staticmethod
    def upload_autoPROC_to_icat(beamline, proposal, processName, list_raw_dir, processed_data_dir):
        dataset_name = processName
        icat_dir = processed_data_dir / processName
        if not icat_dir.exists():
            icat_dir.mkdir(mode=0o755)
        working_dir = processed_data_dir / "nobackup"
        ispyb_xml_path = working_dir / f"{processName}.xml"
        if ispyb_xml_path.exists():
            with open(ispyb_xml_path) as f:
                ispyb_xml = f.read()
            AutoProcessingWrappers.copy_data_to_icat_dir(
                ispyb_xml=ispyb_xml,
                icat_dir=icat_dir
            )
            metadata = AutoProcessingWrappers.create_icat_metadata_from_ispyb_xml(
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
            file_type = program_attachment["fileType"]
            file_name = program_attachment["fileName"]
            file_path = program_attachment["filePath"]
            shutil.copy(os.path.join(file_path, file_name), icat_dir)
            pass


    @staticmethod
    def create_icat_metadata_from_ispyb_xml(ispyb_xml):
        dict_ispyb = xmltodict.parse(ispyb_xml)
        # Meta-data
        metadata = {}
        autoProcContainer = dict_ispyb["AutoProcContainer"]
        autoProc = autoProcContainer["AutoProc"][0]
        autoProcScalingContainer = autoProcContainer["AutoProcScalingContainer"][0]
        if "autoProcIntegrationContainer" in autoProcScalingContainer:
            autoProcIntegrationContainer = autoProcScalingContainer["autoProcIntegrationContainer"]
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
            metadata["MXAutoprocIntegration_cell_alpha"] = autoProcIntegration["cell_alpha"]
            metadata["MXAutoprocIntegration_cell_beta"] = autoProcIntegration["cell_beta"]
            metadata["MXAutoprocIntegration_cell_gamma"] = autoProcIntegration["cell_gamma"]

        for (
            autoProcScalingStatistics
        ) in autoProcScalingContainer["AutoProcScalingStatistics"]:
            statistics_type = autoProcScalingStatistics["scalingStatisticsType"]
            icat_stat_name = statistics_type.replace("Shell", "")
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_completeness"
            ] = autoProcScalingStatistics["completeness"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_anomalous_completeness"
            ] = autoProcScalingStatistics["anomalousCompleteness"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_multiplicity"
            ] = autoProcScalingStatistics["multiplicity"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_anomalous_multiplicity"
            ] = autoProcScalingStatistics["anomalousMultiplicity"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_resolution_limit_low"
            ] = autoProcScalingStatistics["resolutionLimitLow"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_resolution_limit_high"
            ] = autoProcScalingStatistics["resolutionLimitHigh"]
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_r_merge"
            ] = autoProcScalingStatistics["rMerge"]
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
            metadata[
                f"MXAutoprocIntegrationScaling_{icat_stat_name}_cc_half"
            ] = autoProcScalingStatistics["ccHalf"]
            if "ccAno" in autoProcScalingStatistics:
                metadata[
                    f"MXAutoprocIntegrationScaling_{icat_stat_name}_cc_ano"
                ] = autoProcScalingStatistics["ccAno"]
        return metadata
