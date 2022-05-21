"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
Case Type   : 系统内部使用工具
Case Name   : 主机指定SIGNALNAME PID为USR2，执行gs_ctl kill是否成功
Description :
    1.查看数据库用户PID
    2.对USR2执行gs_ctl kill
    3.查看数据库进程(可能需要稍等一会)
    4.重启数据库
Expect      :
    1.查看数据库用户的PID成功
    2.对USR2执行gs_ctl kill成功，gs_ctl kill ,datadir is (null)
    3.数据库进程被kill掉
    4.重启数据库成功
History     :
"""

import unittest
import time

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0105开始执行-----')
        self.constant = Constant()
        self.common = Common()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('-----------------查看数据库进程号---------------')
        pid_cmd = f"ps -u {self.PrimaryNode.ssh_user} | grep 'gaussdb' |" \
            f" tr -s ' '| cut -d ' ' -f 2"
        LOG.info(pid_cmd)
        pid_msg = self.PrimaryNode.sh(pid_cmd).result()
        LOG.info('数据库进程为：' + pid_msg)
        kill_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl kill USR2 {pid_msg};
            '''
        LOG.info(kill_cmd)
        kill_msg = self.PrimaryNode.sh(kill_cmd).result()
        self.assertIn('gs_ctl kill', kill_msg)

        time.sleep(20)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        LOG.info('--------------进行重启------------------')
        restart_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary \
            -m immediate;
            '''
        LOG.info(restart_cmd)
        restart_msg = self.PrimaryNode.sh(restart_cmd).result()
        LOG.info(restart_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0105执行完成---')
