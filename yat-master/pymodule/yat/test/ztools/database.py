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
import stat
from . import archive_log
from . import instance
from .util import assert_data_path
from .util import run_cmd

create_db_template = """
create database gauss character set ${charset}
CONTROLFILE
(
    '${data}/data/cntl1', 
    '${data}/data/cntl2', 
    '${data}/data/cntl3'
)
LOGFILE
(
    '${data}/data/log1' size 500M, 
    '${data}/data/log2' size 500M, 
    '${data}/data/log3' size 500M, 
    '${data}/data/log4' size 500M
)
system tablespace DATAFILE 
    '${data}/data/system' size 1G autoextend on next 32M
undo tablespace DATAFILE 
    '${data}/data/undo' size 1G
default tablespace DATAFILE 
    '${data}/data/user1' size 200M autoextend on next 32M,
    '${data}/data/user2' size 200M autoextend on next 32M,
    '${data}/data/user3' size 200M autoextend on next 32M,
    '${data}/data/user4' size 200M autoextend on next 32M
temporary tablespace TEMPFILE
    '${data}/data/temp1_01' size 160M autoextend on next 32M, 
    '${data}/data/temp1_02' size 160M autoextend on next 32M
nologging tablespace TEMPFILE 
    '${data}/data/temp2_01' size 160M autoextend on next 32M,
    '${data}/data/temp2_02' size 160M autoextend on next 32M 
nologging undo tablespace TEMPFILE 
    '${data}/data/temp2_undo' size 1G ARCHIVELOG;
"""


def template_gen(template, **opts):
    for k, v in opts.items():
        template = template.replace("${%s}" % k, v)

    return template


def create_db(data, **kwargs):
    """
    Create database on zenith instance
    :param data:
    :return:
    """
    init_script = kwargs.get("init_script")
    init_template = kwargs.get('init_template')
    charset = kwargs.get('db_charset', 'utf8')

    data = os.path.abspath(data)
    assert_data_path(data)
    if init_script:
        create_db_file = os.path.abspath(init_script)
    else:
        if init_template:
            with open(init_template) as template:
                create_template = template.read()
        else:
            create_template = create_db_template
        create_db_file = os.path.join(data, 'create_database.sql')
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(create_db_file, flags, mode), 'w') as out:
            out.write(template_gen(create_template, data=data, charset=charset))

    cmd = "zsql / as sysdba -D {0} -q -f {1} > {0}/log/create_database.log 2>&1".format(data, create_db_file)
    cmd_arry = []
    cmd_arry.append(["zsql" , "/" , "as" , "sysdba" , "-D" , data , "-q" , "-f" , create_db_file , ">" , data , "/log/create_database.log 2>&1"])

    run_cmd(cmd_arry)


def delete_db(data, clean_archive=True):
    """
    Kill instance and delete database files
    :param data:
    :param clean_archive:
    :return:
    """
    assert_data_path(data)
    instance.kill_instance(data)
    if clean_archive:
        archive_log.clean_archive_log(data)

    data_dir = os.path.join(data, 'data')
    shutil.rmtree(data_dir)
    os.makedirs(data_dir, 0o700)

