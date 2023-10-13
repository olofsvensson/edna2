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
__date__ = "13/10/2023"


import shlex
import subprocess
import threading


def run_command_line(command_line, timeout_sec=120):
    proc = subprocess.Popen(
        shlex.split(command_line),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    kill_proc = lambda p: p.kill()
    timer = threading.Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        binaryStdout, binaryStderr = proc.communicate()
        stdout = binaryStdout.decode("utf-8")
        stderr = binaryStderr.decode("utf-8")
    finally:
        timer.cancel()
    return stdout, stderr


def parse_salloc_stderr(stderr):
    job_id = None
    list_lines = stderr.split("\n")
    for line in list_lines:
        if line.startswith("salloc: Granted job allocation"):
            job_id = int(line.split(" ")[-1])
            break
    return job_id


def salloc(partition, exclusive=False):
    timeout_sec = 100
    salloc_command_line = f"salloc --no-shell -p {partition}"
    if exclusive:
        salloc_command_line += " --exclusive"
    stdout, stderr = run_command_line(salloc_command_line, timeout_sec)
    job_id = parse_salloc_stderr(stderr)
    if job_id is None:
        print(stdout)
        print(stderr)
    return job_id


def srun(job_id, command):
    timeout_sec = 10
    srun_command_line = f"srun --jobid {job_id} {command}"
    stdout, stderr = run_command_line(srun_command_line, timeout_sec)
    return stdout, stderr


def scancel(job_id):
    timeout_sec = 10
    scancel_command_line = f"scancel {job_id}"
    stdout, stderr = run_command_line(scancel_command_line, timeout_sec)

