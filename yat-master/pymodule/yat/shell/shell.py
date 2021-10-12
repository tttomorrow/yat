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


class Shell:
    def sh(self, cmd: str, *params, **kwargs) -> (int, str):
        proc = Popen(cmd.format(*params, **kwargs), stderr=STDOUT, stdout=PIPE, encoding='utf-8')
        out = proc.stdout.read()
        proc.stdout.close()
        proc.wait()
        return proc.returncode, out

    def close(self):
        pass
