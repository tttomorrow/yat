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
import re
import stat
import pwd
from yat.common.utils import root_gid, root_uid
from yat.common.shell import run_shell


# get the root user id and group id for current user checker and file owner checker



def check_depend():
    """
    check the depend to run yat
    :return: check pass return True, else False
    """
    errors = []
    # checking java version
    ret, out = run_shell('java -version')
    if ret != 0:
        errors.append("java is not install")
        return errors

    if None is re.search(r'version[^0-9]*1\.(8|9|10|11)\.*', out):
        errors.append("java need version >= 1.8")

    return errors


def check_root_user():
    """
    check the current is root or not
    :return: check errors
    """
    errors = []
    if os.getuid() == root_uid or os.getgid() == root_gid:
        errors.append("root user or user with root group is not allow to run yat")


def check_core_dump_setting():
    """
    checking os core dump setting is right
    """
    errors = []

    ret, out = run_shell('ulimit -c')
    limit = out.strip('\n').strip()
    if limit != 'unlimited':
        errors.append(f'core dump file setting limit="{limit}" is incorrect, should set to unlimited')

    with open('/proc/sys/kernel/core_pattern', 'r') as core_pattern_file:
        core_pattern = core_pattern_file.read().strip()

    core_path = os.path.dirname(core_pattern)
    if os.path.isabs(core_path):
        if os.path.exists(core_path):
            core_dir_stat = os.stat(core_path)
            permission = stat.S_IMODE(core_dir_stat.st_mode)
            if permission != 0o777:
                errors.append(f'core dump pattern path {core_path}\'s permission mask {permission} is not right')
        else:
            errors.append(f'core dump pattern path {core_path} is not exists')
    else:
        errors.append(f'core dump pattern path {core_pattern} is not a absolute path')

    return errors


def check_all():
    errors = []
    errors.extend(check_depend())
    return errors
