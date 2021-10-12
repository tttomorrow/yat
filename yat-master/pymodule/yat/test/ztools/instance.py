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
import shutil
import time
import stat
from .errors import ZenithToolsError, ArgumentsError
from .params import ZParam
from .util import assert_data_path, ZSQLClient, is_data_path
from .util import run_cmd, run_cmd_output


def get_instance_pids(data):
    """
    get instance running pids with given data path
    """
    assert_data_path(data)
    ret, pid_txt, _ = run_cmd_output('lsof +d {0} | grep zengine | awk \'{{ print $2; }}\' | sort | uniq'.format(
        os.path.join(data, 'data')
    ))
    lsof_pids = [int(pid.strip()) for pid in pid_txt.split('\n') if len(pid.strip()) > 0]

    ret, pid_txt, _ = run_cmd_output("ps -ef | grep zengine | grep -v grep | grep '{0}' | awk '{{ print $2; }}'".format(
        os.path.abspath(data)
    ))
    ps_pids = [int(pid.strip()) for pid in pid_txt.split('\n') if len(pid.strip()) > 0]
    # remove the same pid
    return list(set(lsof_pids) | set(ps_pids))


def kill_instance(data):
    """
    kill the instance with given data path
    """
    assert_data_path(data)
    data = os.path.abspath(data)
    pids = get_instance_pids(data)
    count = 0
    # make sure all instance process is dead
    while len(pids) > 0:
        count += 1
        if count > 300:
            raise ZenithToolsError("kill instance failed after many times kill")
        for pid in pids:
            cmd_arry = []
            cmd_arry.append(["kill" , "-9" , pid])
            run_cmd(cmd_arry)
        pids = get_instance_pids(data)


def create_instance(data, port, config=None):
    """ create zenith instance directories"""
    if config is None:
        config = []
    data = os.path.abspath(data)
    data_path = os.path.join(data, 'data')
    config_path = os.path.join(data, 'cfg')

    if os.path.exists(data) and len(os.listdir(data)):
        raise ZenithToolsError('not empty data directory, reject to create instance')

    settings = []
    for c in config:
        settings.append(c)

    if not os.path.exists(data_path):
        os.makedirs(data_path, 0o700)
    if not os.path.exists(config_path):
        os.makedirs(config_path, 0o700)

    param = ZParam()
    param.load('\n'.join(config) + '\nLSNR_PORT=%d' % port)
    param.save(os.path.join(config_path, 'zengine.ini'))
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    with os.fdopen(os.open(os.path.join(config_path, 'zhba.conf'), flags, mode), 'w') as zhba:
        zhba.writelines(['host * 127.0.0.1,::1'])


def start_instance(data, mode='open'):
    """ start zenith instance background with given mode """
    assert_data_path(data)
    if mode not in ('open', 'nomount', 'mount'):
        raise ArgumentsError('given start mode %s is not illegal' % mode)

    data = os.path.abspath(data)
    cmd = '(setsid zengine -D {0} {1} > /dev/null 2>&1 &);'.format(data, mode)
    cmd_arry = []
    cmd_arry.append(["setsid" , "zengine" , "-D" , data , mode , ">" , "/dev/null" , "2>&1" , "&"])
    run_cmd(cmd_arry)
    time.sleep(5)
    return len(get_instance_pids(data)) > 0


def delete_instance(data):
    """ delete instance process and remove directories """
    if os.path.exists(data):
        if is_data_path(data):
            kill_instance(data)
        shutil.rmtree(data, True)


def status_instance(data):
    """ get the instance process status """
    assert_data_path(data)
    if len(get_instance_pids(data)) > 0:
        output = ZSQLClient(data=data).execute('select status from dv_instance')
        if 'OPEN' in output:
            return 'open'
        elif 'NOMOUNT' in output:
            return 'nomount'
        elif 'MOUNT' in output:
            return 'mount'
        else:
            return 'unknown'
    else:
        return 'close'


def get_run_log(data):
    """ get the instance's run log text """
    assert_data_path(data)
    log_file = os.path.join(data, 'log', 'run', 'zengine.rlog')
    if not os.path.exists(log_file):
        raise ZenithToolsError('zenith run log file is not exists')

    with open(log_file) as log:
        return log.read()
