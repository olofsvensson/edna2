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

# Corresponding EDNA code:
# https://github.com/olofsvensson/edna-mx
# kernel/src/EDUtilsImage.py

import re
import pathlib


def __compileAndMatchRegexpTemplate(pathToImage):
    listResult = []
    if not isinstance(pathToImage, pathlib.Path):
        pathToImage = pathlib.Path(str(pathToImage))
    baseImageName = pathToImage.name
    regexp = re.compile(r'(.*)([^0^1^2^3^4^5^6^7^8^9])([0-9]*)\.(.*)')
    match = regexp.match(baseImageName)
    if match is not None:
        listResult = [
            match.group(0),
            match.group(1),
            match.group(2),
            match.group(3),
            match.group(4)
        ]
    return listResult


def getImageNumber(pathToImage):
    iImageNumber = None
    listResult = __compileAndMatchRegexpTemplate(pathToImage)
    if listResult is not None:
        iImageNumber = int(listResult[3])
    return iImageNumber


def getTemplate(pathToImage, symbol="#"):
    template = None
    listResult = __compileAndMatchRegexpTemplate(pathToImage)
    if listResult is not None:
        prefix = listResult[1]
        separator = listResult[2]
        imageNumber = listResult[3]
        suffix = listResult[4]
        hashes = ""
        for i in range(len(imageNumber)):
            hashes += symbol
        template = prefix + separator + hashes + "." + suffix
    return template


def getPrefix(pathToImage):
    prefix = None
    listResult = __compileAndMatchRegexpTemplate(pathToImage)
    if listResult is not None:
        prefix = listResult[1]
    return prefix


def getSuffix(pathToImage):
    suffix = None
    listResult = __compileAndMatchRegexpTemplate(pathToImage)
    if listResult is not None:
        suffix = listResult[4]
    return suffix


def getPrefixNumber(pathToImage):
    prefix = getPrefix(pathToImage)
    number = getImageNumber(pathToImage)
    prefixNumber = '{0}_{1:04d}'.format(prefix, number)
    return prefixNumber

def getH5FilePath(filePath, batchSize=100, hasOverlap= False, isFastMesh=False):
    if type(filePath) == str:
        filePath = pathlib.Path(filePath)
    imageNumber = getImageNumber(filePath)
    prefix = getPrefix(filePath)
    if hasOverlap:
        h5ImageNumber = 1
        h5FileNumber = imageNumber
    elif isFastMesh or filePath.name.startswith("mesh-"):
        h5ImageNumber = int((imageNumber - 1) / 100) + 1
        h5FileNumber = 1
    else:
        h5ImageNumber = 1
        h5FileNumber = int((imageNumber - 1) / batchSize) * batchSize + 1
    h5MasterFileName = "{prefix}_{h5FileNumber}_master.h5".format(
        prefix=prefix, h5FileNumber=h5FileNumber)
    h5MasterFilePath = filePath.parent / h5MasterFileName
    h5DataFileName = \
        "{prefix}_{h5FileNumber}_data_{h5ImageNumber:06d}.h5".format(
            prefix=prefix, h5FileNumber=h5FileNumber, h5ImageNumber=h5ImageNumber)
    h5DataFilePath = filePath.parent / h5DataFileName
    return h5MasterFilePath, h5DataFilePath, h5FileNumber
