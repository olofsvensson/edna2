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


import unittest

from edna2.utils import UtilsSlurm
from edna2.utils import UtilsConfig


class UtilsSlurmExecTest(unittest.TestCase):

    def test_parse_salloc_stderr(self):
        stderr = """salloc: Pending job allocation 9420567
salloc: job 9420567 queued and waiting for resources
salloc: job 9420567 has been allocated resources
salloc: Granted job allocation 9420567
salloc: Nodes mxhpc3-2201 are ready for job
        """
        job_id = UtilsSlurm.parse_salloc_stderr(stderr)
        self.assertEqual(job_id, 9420567)



    @unittest.skipIf(
        UtilsConfig.getSite() == "Default",
        "Cannot run slurm exec test with default config",
    )
    def test_salloc(self):
        partition = "mx"
        job_id = UtilsSlurm.salloc(
            partition=partition
        )
        self.assertIsNotNone(job_id)
        UtilsSlurm.scancel(job_id)


    @unittest.skipIf(
        UtilsConfig.getSite() == "Default",
        "Cannot run slurm exec test with default config",
    )
    def test_srun(self):
        partition = "mx"
        job_id = UtilsSlurm.salloc(
            partition=partition,
            exclusive=True
        )
        self.assertIsNotNone(job_id)
        command = "whoami"
        stdout, stderr = UtilsSlurm.srun(job_id, command)
        print(stdout)
        print(stderr)
        print("*"* 80)
        command = "id"
        stdout, stderr = UtilsSlurm.srun(job_id, command)
        print(stdout)
        print(stderr)
        UtilsSlurm.scancel(job_id)

