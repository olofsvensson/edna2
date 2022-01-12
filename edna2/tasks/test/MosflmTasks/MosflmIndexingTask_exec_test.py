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
__date__ = "14/05/2019"

import unittest

from edna2.utils import UtilsTest
from edna2.utils import UtilsConfig
from edna2.utils import UtilsLogging

from edna2.tasks.MosflmTasks import MosflmIndexingTask

logger = UtilsLogging.getLogger()


class MosflmTasksExecTest(unittest.TestCase):

    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    # @unittest.skipIf(UtilsConfig.getSite() == 'Default',
    #                  'Cannot run mosflm test with default config')
    # def test_execute_MosflmIndexingTask_2m_RNASE_1(self):
    #     UtilsTest.loadTestImage('ref-2m_RNASE_1_0001.cbf')
    #     UtilsTest.loadTestImage('ref-2m_RNASE_1_0002.cbf')
    #     referenceDataPath = self.dataPath / 'mosflm_indexing_2m_RNASE_1.json'
    #     inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
    #     mosflmIndexingTask = MosflmIndexingTask(inData=inData)
    #     mosflmIndexingTask.execute()
    #     self.assertTrue(mosflmIndexingTask.isSuccess())

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run mosflm test with default config')
    def tes_execute_MosflmIndexingTask_TRYP_X1_4(self):
        UtilsTest.loadTestImage('ref-TRYP-X1_4_0001.cbf')
        UtilsTest.loadTestImage('ref-TRYP-X1_4_0002.cbf')
        UtilsTest.loadTestImage('ref-TRYP-X1_4_0003.cbf')
        UtilsTest.loadTestImage('ref-TRYP-X1_4_0004.cbf')
        referenceDataPath = self.dataPath / 'mosflm_indexing_TRYP-X1_4.json'
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        mosflmIndexingTask = MosflmIndexingTask(inData=inData)
        mosflmIndexingTask.execute()
        self.assertTrue(mosflmIndexingTask.isSuccess())

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run mosflm test with default config')
    def test_execute_MosflmIndexingTask_TRYP_X1_4(self):
        referenceDataPath = self.dataPath / 'TRYP-X1_4.json'
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        mosflmIndexingTask = MosflmIndexingTask(inData=inData)
        mosflmIndexingTask.execute()
        self.assertTrue(mosflmIndexingTask.isSuccess())


    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run mosflm test with default config')
    def test_execute_MosflmIndexingTask_fae_3(self):
        UtilsTest.loadTestImage('ref-fae_3_0001.h5')
        UtilsTest.loadTestImage('ref-fae_3_0002.h5')
        UtilsTest.loadTestImage('ref-fae_3_0003.h5')
        UtilsTest.loadTestImage('ref-fae_3_0004.h5')
        referenceDataPath = self.dataPath / 'mosflm_indexing_fae_3.json'
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        mosflmIndexingTask = MosflmIndexingTask(inData=inData)
        mosflmIndexingTask.execute()
        self.assertTrue(mosflmIndexingTask.isSuccess())

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run mosflm test with default config')
    def tes_aggregate_master(self):
        import h5py
        import pprint
        filePath = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_1_data_000001.h5"
        filePath1 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_1_master.h5"
        filePath2 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_2_master.h5"
        filePath3 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_3_master.h5"
        filePath4 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_4_master.h5"
        f1 = h5py.File(filePath1, 'r')
        f2 = h5py.File(filePath2, 'r')
        f3 = h5py.File(filePath3, 'r')
        f4 = h5py.File(filePath4, 'r')
        data1 = f1['entry']['data']['data_000001'][()]
        data2 = f2['entry']['data']['data_000001'][()]
        data3 = f3['entry']['data']['data_000001'][()]
        data4 = f4['entry']['data']['data_000001'][()]
        # f.create_group('entry')
        # entry = f['entry']
        # entry.create_group('data')
        # data = entry['data']
        f = h5py.File(filePath, 'w')
        data_000001 = f.create_dataset('/entry/data/data', (4, 4362, 4148), dtype="uint32")
        data_000001[0,:,:] = data1[0,:,:]
        data_000001[1,:,:] = data2[0,:,:]
        data_000001[2,:,:] = data3[0,:,:]
        data_000001[3,:,:] = data4[0,:,:]
        # data['data_000001'] = data_000001
        # pprint.pprint(data.keys())
        # pprint.pprint(data.values())
        f.close()

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run mosflm test with default config')
    def tes_modify_master(self):
        import h5py
        import pprint
        filePath1 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_1_master.h5"
        filePath2 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_master.h5"
        f1 = h5py.File(filePath1, "r+")
        # f2 = h5py.File(filePath2, "w")
        entry = f1['entry']
        nimages = entry['instrument']['detector']['detectorSpecific']['nimages']
        print(dir(nimages))
        # nimages = ?4
        # print(nimages[()])
        entry['instrument']['detector']['detectorSpecific']['nimages'] [()]= 4
        # print(entry['instrument']['detector']['detectorSpecific']['nimages'][()])
        # f2['entry'] = entry
        f1.close()

