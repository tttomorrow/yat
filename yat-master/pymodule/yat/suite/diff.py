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

import os
import stat
from yat.common.utils import scan_path
from yat.const import YAT_RESULT_DIR, YAT_LOG_DIR, YAT_DIFF


class _DiffCollectHandler:
    """
    do real work to collect diff files
    """
    DIFF_SEPARATOR = '\n%s\n' % ("=" * 100)

    def __init__(self, output):
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        self.output = os.fdopen(os.open(output, flags, mode), 'w')

    def __call__(self, file, is_dir, base):
        if is_dir:
            return
        if file.endswith(".diff") and os.path.getsize(file) > 0:
            with open(file) as diff:
                content = diff.read()
            self.output.write(self.DIFF_SEPARATOR)
            self.output.write(content)
            self.output.flush()
    
    def close(self):
        self.output.close()


def collect_diff_file(suite_dir):
    """
    collect all the diff file to one yat.diff
    :param suite_dir: the test suite root dir
    """
    result_dir = os.path.join(suite_dir, YAT_RESULT_DIR)
    log_dir = os.path.join(suite_dir, YAT_LOG_DIR)

    if os.path.exists(result_dir):
        handler = _DiffCollectHandler(os.path.join(log_dir, YAT_DIFF))
        try:
            scan_path(result_dir, handler)
        finally:
            handler.close()
