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

import grp
import os
import pwd
import shutil
import sys
import tarfile
from subprocess import Popen, PIPE

from .errors import ZenithToolsError

PY2 = sys.version_info[0] == 2


def run_cmd(cmds, *args):
    for cmd in cmds:
        pop = Popen(cmd).wait()
    return pop


def run_cmd_output(cmd, *args):
    if len(args) > 0:
        cmd %= args

    opt = {
        'shell': True,
        'stdout': PIPE,
        'stderr': PIPE
    }

    if not PY2:
        opt['encoding'] = 'utf-8'

    proc = Popen(cmd, **opt)
    out, err = proc.communicate()

    return proc.returncode, out, err


def is_data_path(data):
    """
    is a path a zenith-data path
    :param data:
    :return:
    """
    data_path = os.path.join(data, 'data')
    cfg_path = os.path.join(data, 'cfg')
    return os.path.exists(data_path) and os.path.exists(cfg_path)


def assert_data_path(data):
    """
    Assert when data path is not exists or illegal
    :param data:
    :return:
    """
    if not os.path.exists(data):
        raise ZenithToolsError('given zenith data path %s is not exists' % data)
    if not is_data_path(data):
        raise ZenithToolsError('given path %s is not a zenith data path' % data)


def get_current_user():
    """
    get *nix system current username and group name
    """
    user = pwd.getpwuid(os.getuid()).pw_name
    group = grp.getgrgid(os.getgid()).gr_name

    return user, group


def set_env():
    """
    set the basic env values
    """
    ret, gsdb_home, _ = run_cmd_output('. ~/.bashrc; echo $GSDB_HOME')
    if ret == 0:
        gsdb_home = gsdb_home.strip('\n').strip('\r').strip(' ')
        os.environ['GSDB_HOME'] = gsdb_home
        os.environ['PATH'] = '%s/bin:%s' % (gsdb_home, os.environ['PATH'])
        if 'LD_LIBRARY_PATH' in os.environ:
            os.environ['LD_LIBRARY_PATH'] = '{0}/lib:{0}/add-ons:{1}'.format(gsdb_home, os.environ['LD_LIBRARY_PATH'])
        else:
            os.environ['LD_LIBRARY_PATH'] = '{0}/lib:{0}/add-ons'.format(gsdb_home)
    else:
        raise ZenithToolsError('env key $GSDB_HOME is not set')


class ZSQLClient:
    def __init__(self, **opts):
        if 'data' in opts:
            data_arg = ['-D', opts['data']]
        else:
            data_arg = []

        if 'user' in opts:
            if 'password' in opts:
                conn_arg = ['%s/%s@%s:%d' % (opts['user'], opts['password'], opts['host'], opts['port'])]
            else:
                conn_arg = ['%s@%s:%d' % (opts['user'], opts['host'], opts['port'])]
        elif 'host' in opts:
            conn_arg = ['/', 'as', 'sysdba', '%s:%d' % (opts['host'], opts['port'])]
        else:
            conn_arg = ['/', 'as', 'sysdba']

        self.cmd = ['zsql']
        self.cmd.extend(conn_arg)
        self.cmd.append('-q')
        self.cmd.extend(data_arg)

    def execute(self, sql):
        cmd = self.cmd + ['-c', "'%s'" % sql]
        ret, output, err = run_cmd_output(' '.join(cmd))
        if ret == 0:
            return output
        else:
            raise ZenithToolsError('execute sql %s failed: %s' % (sql, output + err))


def tar_copy(tars, dest):
    tar_info = [i for i in tars.split(':') if len(i) > 0]

    if len(tar_info) < 1:
        return

    for tar_path in tar_info[:-1]:
        dir_path = os.path.dirname(tar_path)
        tar_path = os.path.basename(tar_path)
        if dir_path != '':
            os.chdir(dir_path)

        tar = tarfile.open(tar_path)
        tar.extractall()

    shutil.copytree(tar_info[-1], dest)
