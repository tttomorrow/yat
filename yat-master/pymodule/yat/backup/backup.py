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

import datetime
import os
import shutil
import sys

from yat.common.utils import scan_path
from yat.errors import YatError
from yat.suite import is_test_suite


def now_str():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')


def mode_to_list(mode):
    if mode == 'full':
        return ['log', 'result', 'temp']
    elif mode == 'quick':
        return ['log', 'result']
    elif mode == 'log':
        return ['log']
    else:
        raise YatError('error: unknown backup mode found: %s' % mode)


def exclude_common_path(suite_paths):
    split_paths = [path.split(os.path.sep) for path in suite_paths]

    pos = -1

    same = True

    while same:
        pos += 1
        name_set = set()
        same = True
        for split_path in split_paths:
            if pos < len(split_path) - 1:
                name_set.add(split_path[pos])
            else:
                same = False
                break
        same = same and len(name_set) == 1

    return [(val, os.path.join(*split_paths[index][pos:])) for index, val in enumerate(suite_paths)]


class SuiteScannHandler:
    def __init__(self):
        self.suites = []

    def __call__(self, path, is_dir, base):
        if is_dir and is_test_suite(path):
            self.suites.append(path)


def do_backup(**opts):
    backup_path = opts.get('backup_dir')
    if backup_path is None:
        raise YatError('-b/--backup-dir is required')

    backup_list = mode_to_list(opts['mode'])
    scanner = SuiteScannHandler()
    scan_path(opts['dir'], scanner, True)
    path_info = exclude_common_path(scanner.suites)
    real_backup_path = os.path.join(backup_path, now_str())
    if os.path.exists(real_backup_path):
        raise YatError('error: backup set %s is exists' % real_backup_path)

    for from_path, to_path in path_info:
        sys.stdout.write('Backup Suite %s ... ' % from_path)
        sys.stdout.flush()
        to_path = os.path.join(real_backup_path, to_path)
        if len([0 for target in backup_list if os.path.exists(os.path.join(from_path, target))]) <= 0:
            sys.stdout.write('empty\n')
            continue

        if not os.path.exists(to_path):
            os.makedirs(to_path)

        broken = False
        for target in backup_list:
            sub_from_path = os.path.join(from_path, target)
            if os.path.exists(sub_from_path):
                shutil.copytree(sub_from_path, os.path.join(to_path, target))
            else:
                broken = True
        if broken:
            sys.stdout.write('broken\n')
        else:
            sys.stdout.write('ok\n')


def do_init(**opts):
    pass


def do_config(**opts):
    pass

