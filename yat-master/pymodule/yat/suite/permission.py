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

from yat.common.utils import scan_path, chmod
from yat.const import YAT_SCRIPT_DIR

# TODO read case suffix list from configure
_test_case_list = (
    '.sql', '.py', '.sh', '.groovy', '.go'
)


def suite_permission(test_dir, readonly=False, onerror=None):
    if onerror is None:
        def onerror(_path, _exc_info):
            print("set permission of file %s with error: %s" % (_path, _exc_info))

    def _permission_normal_handler(path, is_dir, base):
        """ for normal file mode set handler """
        if is_dir:
            the_mode = 0o500 if readonly else 0o700
        else:
            the_mode = 0o400 if readonly else 0o600
        chmod(path, the_mode, onerror=onerror)

    def _permission_test_case_handler(path, is_dir, base):
        """
            for test case file and directory mode set handler

            for directory:
                1. __pycache__ dir is ignore

            for files:
                1. .sql
                2. .sh
                3. .py
                4. .go
                5. .groovy

                is set to mode
            other is ignore
        """
        the_mode = None
        if is_dir:
            if base == '__pycache__':
                the_mode = 0o700
            else:
                the_mode = 0o500 if readonly else 0o700
        else:
            if os.path.splitext(path)[1] in _test_case_list:
                the_mode = 0o400 if readonly else 0o600

        if the_mode:
            chmod(path, the_mode, onerror=onerror)

    # sub file and directory permission
    for sub_file in os.listdir(test_dir):
        real_path = os.path.join(test_dir, sub_file)
        if sub_file in ('log', 'result', 'temp'):
            chmod(real_path, 0o700, onerror=onerror)
        elif sub_file == 'testcase':
            scan_path(real_path, _permission_test_case_handler, True)
        else:
            scan_path(real_path, _permission_normal_handler, True)

    # script's sub files permission
    script_path = os.path.join(test_dir, YAT_SCRIPT_DIR)
    if os.path.exists(script_path):
        for sub_file in os.listdir(script_path):
            mode = 0o500 if readonly else 0o700
            chmod(os.path.join(script_path, sub_file), mode, onerror=onerror)

    # test suite directory permission
    chmod(test_dir, 0o500 if readonly else 0o700, onerror=onerror)
