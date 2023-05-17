#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the 'Software'), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "21/04/2019"

import datetime
import pprint
import time

import xmltodict

# Corresponding EDNA code:
# https://github.com/olofsvensson/edna-mx
# mxPluginExec/plugins/EDPluginGroupISPyB-v1.4/plugins/
#     EDPluginISPyBRetrieveDataCollectionv1_4.py


from suds.client import Client
from suds.transport.http import HttpAuthenticated

import os
import gzip
import pathlib

from edna2.utils import UtilsPath
from edna2.utils import UtilsConfig
from edna2.utils import UtilsLogging
from edna2.utils import UtilsIspyb

from edna2.tasks.AbstractTask import AbstractTask

logger = UtilsLogging.getLogger()


class ISPyBRetrieveDataCollection(AbstractTask):
    def run(self, inData):
        dictConfig = UtilsConfig.getTaskConfig("ISPyB")
        username = dictConfig["username"]
        password = dictConfig["password"]
        httpAuthenticated = HttpAuthenticated(username=username, password=password)
        wdsl = dictConfig["ispyb_ws_url"] + "/ispybWS/ToolsForCollectionWebService?wsdl"
        client = Client(wdsl, transport=httpAuthenticated, cache=None)
        if "image" in inData:
            path = pathlib.Path(inData["image"])
            indir = path.parent.as_posix()
            infilename = path.name
            dataCollection = (
                client.service.findDataCollectionFromFileLocationAndFileName(
                    indir, infilename
                )
            )
        elif "dataCollectionId" in inData:
            dataCollectionId = inData["dataCollectionId"]
            dataCollection = client.service.findDataCollection(dataCollectionId)
        else:
            errorMessage = "Neither image nor data collection id given as input!"
            logger.error(errorMessage)
            raise BaseException(errorMessage)
        if dataCollection is not None:
            outData = Client.dict(dataCollection)
        else:
            outData = {}
        return outData


class GetListAutoprocIntegration(AbstractTask):
    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "token": {"type": "string"},
                "proposal": {"type": "string"},
                "dataCollectionId": {"type": "integer"},
            },
        }

    # def getOutDataSchema(self):
    #     return {
    #         "type": "array",
    #         "items": {
    #             "type": "object",
    #             "properties": {
    #                 "AutoProcIntegration_autoProcIntegrationId": {"type": "integer"}
    #             }
    #         }
    #     }

    def run(self, inData):
        # urlExtISPyB, token, proposal, dataCollectionId
        token = inData["token"]
        proposal = inData["proposal"]
        dataCollectionId = inData["dataCollectionId"]
        dictConfig = UtilsConfig.getTaskConfig("ISPyB")
        restUrl = dictConfig["ispyb_ws_url"] + "/rest"
        ispybWebServiceURL = os.path.join(
            restUrl,
            token,
            "proposal",
            str(proposal),
            "mx",
            "autoprocintegration",
            "datacollection",
            str(dataCollectionId),
            "view",
        )
        dataFromUrl = UtilsIspyb.getDataFromURL(ispybWebServiceURL)
        outData = {}
        if dataFromUrl["statusCode"] == 200:
            outData["autoprocIntegration"] = dataFromUrl["data"]
        else:
            outData["error"] = dataFromUrl
        return outData


class GetListAutoprocAttachment(AbstractTask):
    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "token": {"type": "string"},
                "proposal": {"type": "string"},
                "autoProcProgramId": {"type": "integer"},
            },
        }

    # def getOutDataSchema(self):
    #     return {
    #         "type": "array",
    #         "items": {
    #             "type": "object",
    #             "properties": {
    #                 "AutoProcIntegration_autoProcIntegrationId": {"type": "integer"}
    #             }
    #         }
    #     }

    def run(self, inData):
        # urlExtISPyB, token, proposal, autoProcProgramId
        token = inData["token"]
        proposal = inData["proposal"]
        autoProcProgramId = inData["autoProcProgramId"]
        dictConfig = UtilsConfig.getTaskConfig("ISPyB")
        restUrl = dictConfig["ispyb_ws_url"] + "/rest"
        ispybWebServiceURL = os.path.join(
            restUrl,
            token,
            "proposal",
            str(proposal),
            "mx",
            "autoprocintegration",
            "attachment",
            "autoprocprogramid",
            str(autoProcProgramId),
            "list",
        )
        dataFromUrl = UtilsIspyb.getDataFromURL(ispybWebServiceURL)
        outData = {}
        if dataFromUrl["statusCode"] == 200:
            outData["autoprocAttachment"] = dataFromUrl["data"]
        else:
            outData["error"] = dataFromUrl
        return outData


class GetListAutoprocessingResults(AbstractTask):
    """
    This task receives a list of data collection IDs and returns a list
    of dictionaries with all the auto-processing results and file attachments
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "token": {"type": "string"},
                "proposal": {"type": "string"},
                "dataCollectionId": {
                    "type": "array",
                    "items": {
                        "type": "integer",
                    },
                },
            },
        }

    # def getOutDataSchema(self):
    #     return {
    #         "type": "object",
    #         "required": ["dataForMerge"],
    #         "properties": {
    #             "dataForMerge": {
    #                 "type": "object",
    #                 "items": {
    #                     "type": "object",
    #                     "properties": {
    #                         "spaceGroup": {"type": "string"}
    #                     }
    #                 }
    #             }
    #         }
    #     }

    def run(self, inData):
        urlError = None
        token = inData["token"]
        proposal = inData["proposal"]
        listDataCollectionId = inData["dataCollectionId"]
        dictForMerge = {}
        dictForMerge["dataCollection"] = []
        for dataCollectionId in listDataCollectionId:
            dictDataCollection = {"dataCollectionId": dataCollectionId}
            inDataGetListIntegration = {
                "token": token,
                "proposal": proposal,
                "dataCollectionId": dataCollectionId,
            }
            getListAutoprocIntegration = GetListAutoprocIntegration(
                inData=inDataGetListIntegration
            )
            getListAutoprocIntegration.setPersistInOutData(False)
            getListAutoprocIntegration.execute()
            resultAutoprocIntegration = getListAutoprocIntegration.outData
            if "error" in resultAutoprocIntegration:
                urlError = resultAutoprocIntegration["error"]
                break
            else:
                listAutoprocIntegration = resultAutoprocIntegration[
                    "autoprocIntegration"
                ]
                # Get v_datacollection_summary_phasing_autoProcProgramId
                for autoprocIntegration in listAutoprocIntegration:
                    if (
                        "v_datacollection_summary_phasing_autoProcProgramId"
                        in autoprocIntegration
                    ):
                        autoProcProgramId = autoprocIntegration[
                            "v_datacollection_summary_phasing_autoProcProgramId"
                        ]
                        inDataGetListAttachment = {
                            "token": token,
                            "proposal": proposal,
                            "autoProcProgramId": autoProcProgramId,
                        }
                        getListAutoprocAttachment = GetListAutoprocAttachment(
                            inData=inDataGetListAttachment
                        )
                        getListAutoprocAttachment.setPersistInOutData(False)
                        getListAutoprocAttachment.execute()
                        resultAutoprocAttachment = getListAutoprocAttachment.outData
                        if "error" in resultAutoprocAttachment:
                            urlError = resultAutoprocAttachment["error"]
                        else:
                            autoprocIntegration[
                                "autoprocAttachment"
                            ] = resultAutoprocAttachment["autoprocAttachment"]
                    dictDataCollection["autoprocIntegration"] = listAutoprocIntegration
            dictForMerge["dataCollection"].append(dictDataCollection)
            # dictForMerge[dataCollectionId] = dictDataCollection
        if urlError is None:
            outData = dictForMerge
        else:
            outData = {"error": urlError}
        return outData


class RetrieveAttachmentFiles(AbstractTask):
    """
    This task receives a list of data collection IDs and returns a list
    of dictionaries with all the auto-processing results and file attachments
    """

    # def getInDataSchema(self):
    #     return {
    #         "type": "object",
    #         "properties": {
    #             "token": {"type": "string"},
    #             "proposal": {"type": "string"},
    #             "dataCollectionId": {
    #                 "type": "array",
    #                 "items": {
    #                     "type": "integer",
    #                 }
    #             }
    #         }
    #     }

    # def getOutDataSchema(self):
    #     return {
    #         "type": "object",
    #         "required": ["dataForMerge"],
    #         "properties": {
    #             "dataForMerge": {
    #                 "type": "object",
    #                 "items": {
    #                     "type": "object",
    #                     "properties": {
    #                         "spaceGroup": {"type": "string"}
    #                     }
    #                 }
    #             }
    #         }
    #     }

    def run(self, inData):
        urlError = None
        listPath = []
        token = inData["token"]
        proposal = inData["proposal"]
        listAttachment = inData["attachment"]
        dictConfig = UtilsConfig.getTaskConfig("ISPyB")
        restUrl = dictConfig["ispyb_ws_url"] + "/rest"
        # proposal/MX2112/mx/autoprocintegration/autoprocattachmentid/21494689/get
        for dictAttachment in listAttachment:
            attachmentId = dictAttachment["id"]
            fileName = dictAttachment["fileName"]
            ispybWebServiceURL = os.path.join(
                restUrl,
                token,
                "proposal",
                str(proposal),
                "mx",
                "autoprocintegration",
                "autoprocattachmentid",
                str(attachmentId),
                "get",
            )
            rawDataFromUrl = UtilsIspyb.getRawDataFromURL(ispybWebServiceURL)
            if rawDataFromUrl["statusCode"] == 200:
                rawData = rawDataFromUrl["content"]
                if fileName.endswith(".gz"):
                    rawData = gzip.decompress(rawData)
                    fileName = fileName.split(".gz")[0]
                with open(fileName, "wb") as f:
                    f.write(rawData)
                listPath.append(str(self.getWorkingDirectory() / fileName))
            else:
                urlError = rawDataFromUrl
        if urlError is None:
            outData = {"filePath": listPath}
        else:
            outData = {"error": urlError}
        return outData


class ISPyBFindDetectorByParam(AbstractTask):
    def run(self, inData):
        dictConfig = UtilsConfig.getTaskConfig("ISPyB")
        username = dictConfig["username"]
        password = dictConfig["password"]
        httpAuthenticated = HttpAuthenticated(username=username, password=password)
        wdsl = dictConfig["ispyb_ws_url"] + "/ispybWS/ToolsForCollectionWebService?wsdl"
        client = Client(wdsl, transport=httpAuthenticated, cache=None)
        manufacturer = inData["manufacturer"]
        model = inData["model"]
        mode = inData["mode"]
        detector = client.service.findDetectorByParam("", manufacturer, model, mode)
        if detector is not None:
            outData = Client.dict(detector)
        else:
            outData = {}
        return outData


class UploadGPhLResultsToISPyB(AbstractTask):
    def run(self, in_data):
        list_id = []
        # List of data collection ids
        list_data_collection_id = in_data["dataCollectionId"]
        # Load XML file
        xml_path = in_data["autoPROCXML"]
        with open(xml_path) as f:
            xml_string = f.read()
        auto_proc_dict = xmltodict.parse(xml_string)
        pprint.pprint(auto_proc_dict)
        auto_proc_container = auto_proc_dict["AutoProcContainer"]
        auto_proc = auto_proc_container["AutoProc"]
        if type(auto_proc) == list:
            list_auto_proc = auto_proc
        else:
            list_auto_proc = [auto_proc]
        auto_proc_program_container = auto_proc_container["AutoProcProgramContainer"]
        auto_proc_scaling_container = auto_proc_container["AutoProcScalingContainer"]
        if type(auto_proc_scaling_container) == list:
            list_auto_proc_scaling_container = auto_proc_scaling_container
        else:
            list_auto_proc_scaling_container = [auto_proc_scaling_container]
        for index, auto_proc_scaling_container in enumerate(list_auto_proc_scaling_container):
            auto_proc = list_auto_proc[index]
            data_collection_id = list_data_collection_id[index]
            auto_proc_scaling = auto_proc_scaling_container["AutoProcScaling"]
            auto_proc_scaling_statistics = auto_proc_scaling_container[
                "AutoProcScalingStatistics"
            ]
            auto_proc_integration_container = auto_proc_scaling_container[
                "AutoProcIntegrationContainer"
            ]
            auto_proc_integration = auto_proc_integration_container["AutoProcIntegration"]
            # image =
            # 1. Create AutoProcProgram entry
            auto_proc_program = auto_proc_program_container["AutoProcProgram"]
            auto_proc_program_id = self.createAutoProcProgram(auto_proc_program)
            # 2. Upload all AutoProcProgramAttachments
            list_attachment = auto_proc_program_container["AutoProcProgramAttachment"]
            list_attachment_id = self.uploadAttachments(
                auto_proc_program_id, list_attachment
            )
            # 3. Create AutoProcIntegration entry
            auto_proc_integration_id = self.createAutoProcIntegration(
                auto_proc_program_id=auto_proc_program_id,
                data_collection_id=data_collection_id,
                auto_proc_integration=auto_proc_integration,
            )
            # 4. Create AutoProc entry
            auto_proc_id = self.createAutoProc(
                auto_proc_program_id=auto_proc_program_id, auto_proc=auto_proc
            )
            # 5. Create scaling entry
            auto_proc_scaling_id = self.createAutoProcScaling(
                auto_proc_id=auto_proc_id, auto_proc_scaling=auto_proc_scaling
            )
            # 6. Create scaling has int entry
            auto_proc_scaling_has_int_id = self.createAutoProcScaling_has_int(
                auto_proc_integration_id=auto_proc_integration_id,
                auto_proc_scaling_id=auto_proc_scaling_id
            )
            # 6. Create scaling statistics entries
            list_statistics_id = self.uploadStatistics(
                auto_proc_scaling_id=auto_proc_scaling_id,
                auto_proc_scaling_statistics=auto_proc_scaling_statistics,
            )
            scaling_container_id = {
                "data_collection_id": data_collection_id,
                "auto_proc_id": auto_proc_id,
                "auto_proc_program_id": auto_proc_program_id,
                "auto_proc_integration_id": auto_proc_integration_id,
                "list_attachment_id": list_attachment_id,
                "auto_proc_scaling_id": auto_proc_scaling_id,
                "auto_proc_scaling_has_int_id": auto_proc_scaling_has_int_id,
                "list_statistics_id": list_statistics_id,
            }
            list_id.append(scaling_container_id)
        out_data = {
            "ids": list_id
        }
        pprint.pprint(out_data)
        return out_data

    def createAutoProcProgram(self, auto_proc_program):
        auto_proc_program_id = UtilsIspyb.storeOrUpdateAutoProcProgram(
            programs=self.check_length(auto_proc_program["processingPrograms"]),
            commandline=self.check_length(auto_proc_program["processingCommandLine"]),
            start_time=self.get_time(auto_proc_program["processingStartTime"]),
            end_time=self.get_time(auto_proc_program["processingEndTime"]),
            environment=self.check_length(auto_proc_program["processingEnvironment"]),
            message=self.check_length(auto_proc_program["processingMessage"]),
            status=auto_proc_program["processingStatus"],
        )
        return auto_proc_program_id

    def uploadAttachments(self, auto_proc_program_id, list_attachments):
        list_attachment_id = []
        for dict_attachment in list_attachments:
            file_name = dict_attachment["fileName"]
            file_dir = pathlib.Path(dict_attachment["filePath"])
            file_path = file_dir / file_name
            if file_path.exists():
                file_type = dict_attachment["fileType"]
                pyarch_dir = UtilsPath.createPyarchFilePath(file_dir)
                pyarch_dir.mkdir(mode=0o755, exist_ok=True, parents=True)
                pyarch_path = pyarch_dir / file_name
                UtilsPath.systemCopyFile(file_path, pyarch_path)
                attachment_id = UtilsIspyb.storeOrUpdateAutoProcProgramAttachment(
                    auto_proc_program_id=auto_proc_program_id,
                    file_path=pyarch_path,
                    file_type=file_type,
                )
                list_attachment_id.append(attachment_id)
            else:
                logger.warning(f"File path {file_path} doesn't exists")
        return list_attachment_id

    def createAutoProcIntegration(
        self, auto_proc_program_id, data_collection_id, auto_proc_integration
    ):
        auto_proc_integration_id = UtilsIspyb.storeOrUpdateAutoProcIntegration(
            auto_proc_program_id=auto_proc_program_id,
            dataCollection_id=data_collection_id,
            start_image_number=auto_proc_integration.get("startImageNumber", None),
            end_image_number=auto_proc_integration.get("endImageNumber", None),
            refined_detector_distance=auto_proc_integration.get(
                "refinedDetectorDistance", None
            ),
            refined_x_beam=auto_proc_integration.get("refinedXBeam", None),
            refined_y_beam=auto_proc_integration.get("refinedYBeam", None),
            rotation_axis_x=auto_proc_integration.get("rotationAxisX", None),
            rotation_axis_y=auto_proc_integration.get("rotationAxisY", None),
            rotation_axis_z=auto_proc_integration.get("rotationAxisZ", None),
            beam_vector_x=auto_proc_integration.get("beamVectorX", None),
            beam_vector_y=auto_proc_integration.get("beamVectorY", None),
            beam_vector_z=auto_proc_integration.get("beamVectorZ", None),
            cell_a=auto_proc_integration.get("cell_a", None),
            cell_b=auto_proc_integration.get("cell_b", None),
            cell_c=auto_proc_integration.get("cell_c", None),
            cell_alpha=auto_proc_integration.get("cell_alpha", None),
            cell_beta=auto_proc_integration.get("cell_beta", None),
            cell_gamma=auto_proc_integration.get("cell_gamma", None),
            record_time_stamp=None,
            anomalous=1,
        )
        return auto_proc_integration_id

    def createAutoProc(self, auto_proc_program_id, auto_proc):
        auto_proc_id = UtilsIspyb.storeOrUpdateAutoProc(
            auto_proc_program_id=auto_proc_program_id,
            space_group=auto_proc["spaceGroup"],
            refined_cell_a=auto_proc["refinedCell_a"],
            refined_cell_b=auto_proc["refinedCell_b"],
            refined_cell_c=auto_proc["refinedCell_c"],
            refined_cell_alpha=auto_proc["refinedCell_alpha"],
            refined_cell_beta=auto_proc["refinedCell_beta"],
            refined_cell_gamma=auto_proc["refinedCell_gamma"],
        )
        return auto_proc_id

    def createAutoProcScaling(self, auto_proc_id, auto_proc_scaling):
        auto_proc_scaling_id = UtilsIspyb.storeOrUpdateAutoProcScaling(
            auto_proc_id=auto_proc_id
        )
        return auto_proc_scaling_id

    def createAutoProcScaling_has_int(self, auto_proc_integration_id, auto_proc_scaling_id):
        auto_proc_scaling_has_int_id = UtilsIspyb.storeOrUpdateAutoProcScalingHasInt(
            auto_proc_integration_id=auto_proc_integration_id,
            auto_proc_scaling_id=auto_proc_scaling_id
        )
        return auto_proc_scaling_has_int_id


    def uploadStatistics(self, auto_proc_scaling_id, auto_proc_scaling_statistics):
        list_statistics_id = []
        for statistics in auto_proc_scaling_statistics:
            auto_proc_scaling_statistics_id = (
                UtilsIspyb.storeOrUpdateAutoProcScalingStatistics(
                    scaling_statistics_type=statistics["scalingStatisticsType"],
                    resolution_limit_low=statistics["resolutionLimitLow"],
                    resolution_limit_high=statistics["resolutionLimitHigh"],
                    r_merge=statistics["rMerge"],
                    r_meas_within_i_plus_i_minus=statistics["rMeasWithinIPlusIMinus"],
                    r_meas_all_i_plus_i_minus=statistics["rMeasAllIPlusIMinus"],
                    r_pim_within_i_plus_i_minus=statistics["rPimWithinIPlusIMinus"],
                    r_pim_all_i_plus_i_minus=statistics["rPimAllIPlusIMinus"],
                    ntotal_observations=statistics["nTotalObservations"],
                    ntotal_unique_observations=statistics["nTotalUniqueObservations"],
                    mean_iover_sig_i=statistics["meanIOverSigI"],
                    completeness=statistics["completeness"],
                    multiplicity=statistics["multiplicity"],
                    anomalous_completeness=statistics["anomalousCompleteness"],
                    anomalous_multiplicity=statistics["anomalousMultiplicity"],
                    auto_proc_scaling_id=auto_proc_scaling_id,
                    cc_half=statistics["ccHalf"],
                    cc_ano=statistics["ccAnomalous"],
                )
            )
            list_statistics_id.append(auto_proc_scaling_statistics_id)
        return list_statistics_id

    def check_length(self, parameter, max_string_length=255):
        if type(parameter) == str and len(parameter) > max_string_length:
            old_parameter = parameter
            parameter = parameter[0 : max_string_length - 3] + "..."
            logger.warning(
                "String truncated to %d characters for ISPyB! Original string: %s"
                % (max_string_length, old_parameter)
            )
            logger.warning("Truncated string: %s" % parameter)
        return parameter

    def get_time(self, time_value):
        # Fri May 12 08:31:54 CEST 2023
        return datetime.datetime.strptime(time_value, "%a %b %d %H:%M:%S %Z %Y")
