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
__date__ = "21/04/2019"

import gzip
import os
import shutil
import time
import graypy
import logging
import logging.handlers

from edna2.utils import UtilsConfig


def addGrayLogHandler(logger):
    server = UtilsConfig.get("Logging", "graylog_server")
    port = UtilsConfig.get("Logging", "graylog_port")
    if server is not None and port is not None:
        graylogHandler = graypy.GELFUDPHandler(server, int(port))
        logger.addHandler(graylogHandler)


def addStreamHandler(logger):
    streamHandler = logging.StreamHandler()
    logFileFormat = "%(asctime)s %(levelname)-8s %(message)s"
    formatter = logging.Formatter(logFileFormat)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)


def rotator(source, dest):
    with open(source, "rb") as f_in:
        with gzip.open(dest + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(source)


def addConfigFileHandler(logger):
    logPath = UtilsConfig.get("Logging", "log_file_path")
    do_add_rotating_fileHandler = True
    if do_add_rotating_fileHandler and (logPath is not None):
        is_ok = False
        if os.path.exists(logPath):
            if os.access(logPath, os.W_OK):
                is_ok = True
        else:
            logDir = os.path.dirname(logPath)
            if os.path.exists(logDir):
                if os.access(logDir, os.W_OK):
                    is_ok = True
            else:
                logDirParent = os.path.dirname(logDir)
                if os.access(logDirParent, os.W_OK):
                    os.makedirs(logDir)
                    is_ok = True
        if is_ok:
            # if "DATE" in logPath:
            #     logPath = logPath.replace(
            #         "DATE", time.strftime("%Y-%m-%d", time.localtime(time.time()))
            #     )
            if "USER" in logPath:
                logPath = logPath.replace("USER", os.environ["USER"])
            backup_count = int(UtilsConfig.get("Logging", "log_file_backupCount", 30))
            when = UtilsConfig.get("Logging", "when", "midnight")
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=logPath, when=when, backupCount=backup_count
            )
            file_handler.rotator = rotator
            log_file_format = UtilsConfig.get("Logging", "log_file_format")
            if log_file_format is None:
                log_file_format = "%(asctime)s %(module)-20s %(funcName)-15s %(levelname)-8s %(message)s"
            formatter = logging.Formatter(log_file_format)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)


def addFileHandler(logger, log_path):
    do_add_rotating_fileHandler = False
    if len(logger.handlers) > 0:
        # making sure we do not add duplicate handlers
        for handler in logger.handlers:
            if isinstance(handler, logging.handlers.TimedRotatingFileHandler):
                do_add_rotating_fileHandler = False
    if do_add_rotating_fileHandler:
        if "DATETIME" in log_path:
            log_path = log_path.replace(
                "DATETIME", time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
            )
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        maxBytes = int(UtilsConfig.get("Logging", "log_file_maxbytes", 1e7))
        backupCount = int(UtilsConfig.get("Logging", "log_file_backupCount", 0))
        fileHandler = logging.handlers.TimedRotatingFileHandler(
            log_path, maxBytes=maxBytes, backupCount=backupCount
        )
        logFileFormat = UtilsConfig.get("Logging", "log_file_format")
        if logFileFormat is None:
            logFileFormat = (
                "%(asctime)s %(module)-20s %(funcName)-15s %(levelname)-8s %(message)s"
            )
        formatter = logging.Formatter(logFileFormat)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)


def setLoggingLevel(logger, level):
    if level is None:
        level = UtilsConfig.get("Logging", "level")
    if level is None:
        level = "INFO"
    if level == "DEBUG":
        loggingLevel = logging.DEBUG
    elif level == "INFO":
        loggingLevel = logging.INFO
    elif level == "WARNING":
        loggingLevel = logging.WARNING
    elif level == "ERROR":
        loggingLevel = logging.ERROR
    elif level == "CRITICAL":
        loggingLevel = logging.CRITICAL
    elif level == "FATAL":
        loggingLevel = logging.FATAL
    else:
        raise RuntimeError('Unknown logging level: "{0}"'.format(level))
    logger.setLevel(loggingLevel)


def getLogger(level=None):
    logger = logging.getLogger("edna2")
    # Check if handlers already added:
    hasGraylogHandler = False
    hasStreamHandler = False
    hasFileHandler = False
    for handler in logger.handlers:
        if isinstance(handler, graypy.GELFUDPHandler):
            hasGraylogHandler = True
        elif isinstance(handler, logging.handlers.TimedRotatingFileHandler):
            hasFileHandler = True
        elif isinstance(handler, logging.StreamHandler):
            hasStreamHandler = True
    if not hasGraylogHandler:
        addGrayLogHandler(logger)
    if not hasStreamHandler:
        addStreamHandler(logger)
    if not hasFileHandler:
        addConfigFileHandler(logger)
    # Set level
    setLoggingLevel(logger, level)
    return logger
