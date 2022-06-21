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
from yat.const import YAT_SCHEDULE_FILE, YAT_TEST_CASE_DIR, YAT_SCHEDULE_DIR
from yat.errors import YatError
from .yat_commander import is_test_suite


def make_schedule(test_dir, force=False):
    """
    Make schedule file from test case directory
    """
    if not is_test_suite(test_dir):
        raise YatError("given test suite path: %s seems not a legal test suite directory" % test_dir)

    schedule_file = os.path.join(test_dir, YAT_SCHEDULE_DIR, YAT_SCHEDULE_FILE)
    if os.path.exists(schedule_file) and not force:
        raise YatError("Default schedule file %s is exists. Using --force to override" % schedule_file)

    test_case_dir = os.path.join(test_dir, YAT_TEST_CASE_DIR)
    cases = os.listdir(test_case_dir)
    if len(cases) <= 0:
        raise YatError("*** ERROR: EMPTY TEST CASE DIRECTORY")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    with os.fdopen(os.open(schedule_file, flags, mode), 'w') as schedule:
        for current_dir, dirs, test_cases in os.walk(test_case_dir):
            groups = ("%s" % os.path.splitext(os.path.join(current_dir, group_case))[0].replace('./testcase/', '')
                      for group_case in test_cases
                      if os.path.isfile(os.path.join(current_dir, group_case))
                     )
            test_groups = "\n      ".join(groups)
            if len(test_groups.strip()) != 0:
                schedule.write("test: %s\n" % test_groups)
