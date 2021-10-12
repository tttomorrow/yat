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
from os.path import expanduser

from .util import get_current_user
from .util import run_cmd

env_template = """
export GSDB_HOME={0}
export PATH=$GSDB_HOME/bin:$PATH
export LD_LIBRARY_PATH=$GSDB_HOME/lib:$GSDB_HOME/add-ons:$LD_LIBRARY_PATH
"""


def install(package, app):
    package = os.path.abspath(package)
    app = os.path.abspath(app)

    pkg_dir = os.path.dirname(package)
    pkg_name = os.path.basename(package)
    cmd_arry = []
    cmd_arry.append(["cd" , pkg_dir])
    cmd_arry.append(["tar" , "xf" , pkg_name])
    cmd_arry.append(["cd" , "$(ls --color=none -d */ | awk '/Gauss100/{{ print $0; }}')"])
    cmd_arry.append(["tar" , "xf" , "$(ls --color=none | awk '/Gauss100.*RUN.*\\.tar\\.gz/{{ print $0; }}')"])
    cmd_arry.append(["mkdir" , "-p" , app])
    cmd_arry.append(["cp" , "-r" , "$(ls --color=none -d */ | awk '/Gauss100.*RUN.*/{{ print $0; }}')" , app])

    run_cmd(cmd_arry)

    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    with os.fdopen(os.open(os.path.join(expanduser('~'), '.bashrc'), flags, mode), 'a') as out:
        out.write(env_template.format(app))


def origin_install(**kwargs):
    package = os.path.abspath(kwargs['package'])
    app = os.path.abspath(kwargs['app'])
    data = os.path.abspath(kwargs['data'])
    config = ' '.join(['-C %s' % c for c in kwargs['config']])
    config += ' -C LSNR_PORT=%d' % kwargs['port']
    pkg_dir = os.path.dirname(package)
    pkg_name = os.path.basename(package)
    user, group = get_current_user()
    cmd_arry = []
    cmd_arry.append(["cd" , pkg_dir])
    cmd_arry.append(["tar" , "xf" , pkg_name])
    cmd_arry.append(["cd" , "$(ls --color=none -d */ | awk '/Gauss100/{{ print $0; }}')"])
    cmd_arry.append(["python" , "install.py" , "-U" , user+":"group , "-R" , app , "-D" , data , config , "-g" , "withoutroot"])
    run_cmd(cmd_arry)
