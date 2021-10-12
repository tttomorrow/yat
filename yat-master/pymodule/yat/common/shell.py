#!/usr/bin/env python
# encoding=utf-8
"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""

from subprocess import Popen, PIPE, STDOUT


def run_shell(cmd, pipe=True, shell=True):
    """
    run sub commands
    :param cmd:
    :param pipe:
    :param shell:
    :return:
    """
    opt = {'shell': shell, 'encoding': 'utf-8'}
    if pipe:
        opt['stdout'] = PIPE
        opt['stderr'] = STDOUT

    proc = Popen(cmd, **opt)

    if pipe:
        stdout, _ = proc.communicate()
        return proc.returncode, stdout
    else:
        return proc.wait(), None


def shell_output(cmd, shell=True):
    return run_shell(cmd, shell=shell)


def shell_status(cmd, shell=True):
    ret, _ = run_shell(cmd, shell=shell)
    return ret


def shell_assert(cmd, pipe=True, shell=True):
    """
    run sub commands and if ret != 0, raise exception
    :param cmd:
    :param pipe:
    :param shell:
    :return:
    """
    ret, out = run_shell(cmd, pipe=pipe, shell=shell)
    if ret != 0:
        raise RuntimeError("run command: %s with error: %s" % (cmd, out))
    return ret, out
