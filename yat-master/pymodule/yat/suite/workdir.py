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
from yat.const import YAT_TEMP_DIR, YAT_RESULT_DIR, YAT_LOG_DIR, YAT_TEXT_LOG, YAT_JSON_LOG, YAT_REDO_LOG, YAT_CONF_DIR, YAT_ENV_FILE_NAME, YAT_SCRIPT_DIR, YAT_TEST_CASE_DIR, YAT_CONF_UPLOAD, YAT_SCHEDULE_DIR, YAT_PYTHON_DIR, YAT_LIB_DIR


class OutputDir:
    def __init__(self, root):
        self.root = root

    def get_temp_dir(self):
        return os.path.join(self.root, YAT_TEMP_DIR)

    def get_result_dir(self):
        return os.path.join(self.root, YAT_RESULT_DIR)

    def get_log_dir(self):
        return os.path.join(self.root, YAT_LOG_DIR)

    def get_yat_text_log(self):
        return os.path.join(self.get_log_dir(), YAT_TEXT_LOG)

    def get_yat_json_log(self):
        return os.path.join(self.get_log_dir(), YAT_JSON_LOG)

    def get_yat_redo_log(self):
        return os.path.join(self.get_log_dir(), YAT_REDO_LOG)


class WorkDir:
    def __init__(self, root):
        self.root = os.path.realpath(root)
        self.output = OutputDir(self.root)

    def get_work_dir(self):
        return self.root

    def get_yat_env(self):
        return os.path.join(self.root, YAT_CONF_DIR, YAT_ENV_FILE_NAME)

    def get_script_dir(self):
        return os.path.join(self.root, YAT_SCRIPT_DIR)

    def get_test_case_dir(self):
        return os.path.join(self.root, YAT_TEST_CASE_DIR)

    def get_conf_dir(self):
        return os.path.join(self.root, YAT_CONF_DIR)

    def get_conf_upload(self):
        return os.path.join(self.root, YAT_CONF_DIR, YAT_CONF_UPLOAD)

    def get_schedule_dir(self):
        return os.path.join(self.root, YAT_SCHEDULE_DIR)

    def get_python_dir(self):
        return os.path.join(self.root, YAT_PYTHON_DIR)

    def get_lib_dir(self):
        return os.path.join(self.root, YAT_LIB_DIR)
