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
from yat.common.shell import shell_assert
from yat.const import YAT_HOME_TEMPLATE, YAT_CONF_DIR
from yat.errors import YatError

_ignore_list = [
    '~*',
    '*~',
    '*.swap',
    '*.swp',
    '*.swo',
    '*.log',
    "*.diff",
    "*.diffs",
    "*.timing",
    "*.out",
    '/log',
    '/temp',
    '/result',
    '__pycache__',
    '*.pyc'
]


def _make_suite_template(suite_dir, configs):
    """
    Make a test suite template directory
    """
    shell_assert("mkdir -p %s" % suite_dir)
    shell_assert("cp -r %s/conf %s" % (YAT_HOME_TEMPLATE, suite_dir))
    for path in ('expect', 'testcase', 'script', 'python', 'schedule'):
        os.makedirs(os.path.join(suite_dir, path), exist_ok = True)
    if len(configs) > 0:
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(os.path.join(suite_dir , YAT_CONF_DIR , 'configure.yml') , flags , mode) , 'w') as config:
            for k, v in configs.items():
                config.write("%s: %s\n" % (k, v))
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    with os.fdopen(os.open(os.path.join(suite_dir, '.gitignore'), flags, mode), 'w') as ignore:
        for item in _ignore_list:
            ignore.write('{}\n'.format(item))


def make_template(test_dir, config, force=False):
    test_dir = os.path.abspath(test_dir)
    if len(test_dir) <= 0:
        raise YatError("test-dir value is illegal")

    test_dir_exists = os.path.exists(test_dir)

    if test_dir_exists and len(os.listdir(test_dir)) > 0 and not force:
        raise YatError("Directory %s is not empty. Initialize stop" % test_dir)

    if test_dir_exists:
        shell_assert("rm -rf '%s'" % test_dir)

    _make_suite_template(test_dir, config)
