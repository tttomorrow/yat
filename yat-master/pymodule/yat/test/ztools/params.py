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

import re
import stat
from io import StringIO

configure_template = """
TEMP_BUFFER_SIZE = 1G
DATA_BUFFER_SIZE = 2G
SHARED_POOL_SIZE = 1G
LOG_BUFFER_SIZE = 64M 
DBWR_PROCESSES = 8
LOG_BUFFER_COUNT = 8
LSNR_ADDR = 127.0.0.1
LSNR_PORT = 1611
SESSIONS = 1500
_SYS_PASSWORD = bcE3GMt2aJzPLVmiv5KjxLgDQC6YDutUv9uqlfuqXdfhPiGkoG9spOc61elNuG02
"""


class ZParam:
    def __init__(self, config=configure_template):
        self._params = {}
        self.load(config)

    def load(self, config):
        if isinstance(config, (str, )):
            stream = StringIO(config)
        else:
            stream = config
        for line in stream:
            if not re.match(r'^[\r\n \t]*$', line):
                idx = line.index('=')
                key = line[:idx].strip()
                value = line[idx + 1:].strip()
                self.set(key, value)

    def set(self, key, value):
        self._params[key] = value

    def get(self, key, default=None):
        return self._params.get(key, default)

    def save(self, file_path):
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(file_path, flags, mode), 'w') as out:
            for k, v in self._params.items():
                out.write('%s = %s\n' % (k, v))
