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
from yat.common.utils import rmtree
from yat.const import YAT_LOG_DIR, YAT_RESULT_DIR, YAT_TEMP_DIR
from yat.errors import YatError


def make_yat_output(source_dir, work_dir, force=False):
    if os.path.exists(work_dir) and len(os.listdir(work_dir)):
        if force:
            rmtree(work_dir, include_self=False)
        else:
            raise YatError('specific --output/-o path is not empty, using --force to override output directory')
    else:
        os.makedirs(work_dir)

    for sub in os.listdir(source_dir):
        if sub not in (YAT_LOG_DIR, YAT_RESULT_DIR, YAT_TEMP_DIR):
            real_path = os.path.abspath(os.path.join(source_dir, sub))
            os.symlink(real_path, os.path.join(work_dir, sub))
