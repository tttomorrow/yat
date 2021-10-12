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

yat_home = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
os.environ['YAT_HOME'] = yat_home


YAT_HOME = yat_home
YAT_HOME_LIB = os.path.join(YAT_HOME, 'lib')
YAT_HOME_APP = os.path.join(YAT_HOME, 'app')
YAT_HOME_DRIVER = os.path.join(YAT_HOME, 'driver')
YAT_HOME_PYTHON = os.path.join(YAT_HOME, 'python')
YAT_HOME_TEMPLATE = os.path.join(YAT_HOME, 'template')
YAT_HOME_SCRIPT = os.path.join(YAT_HOME, 'script')
YAT_RESULT_DIR = 'result'
YAT_LOG_DIR = 'log'
YAT_OUTPUT_DIR = 'output'
YAT_TEMP_DIR = 'temp'
YAT_TEST_CASE_DIR = 'testcase'
YAT_REPORT_DIR = 'report'
YAT_CONF_DIR = 'conf'
YAT_SCHEDULE_DIR = 'schedule'
YAT_PYTHON_DIR = 'python'
YAT_SCRIPT_DIR = 'script'
YAT_ENV_FILE_NAME = 'env.sh'
YAT_DIFF = 'yat.diff'
YAT_SCHEDULE_FILE = 'schedule.schd'
YAT_CONFIGURE_FILE = 'configure.yml'
YAT_JSON_LOG = 'yat.json'
YAT_TEXT_LOG = 'yat.log'
YAT_REDO_LOG = 'yat.redo'
YAT_SYSTEM_LOG = 'error.log'
YAT_CONF_UPLOAD = 'upload.yml'
YAT_LIB_DIR = 'lib'
