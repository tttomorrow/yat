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
"""
Case Type   : 系统内部使用工具
Case Name   : 指定-s为非2的倍数，启动trace
Description :
    1.查看gaussdb进程号
    2.启动trace
Expect      :
    1.查看gaussdb进程号成功
    2.启动trace成功，显示[GAUSS-TRACE] start Success!
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('---Opengauss_Function_Tools_Gs_Trace0024开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('-----------------查看数据库进程号---------------')
        pid_cmd = f"ps -ef | grep {self.PrimaryNode.ssh_user} | " \
            f"grep gaussdb | grep {macro.DB_INSTANCE_PATH} | tr -s ' '" \
            f"| grep -v grep | cut -d ' ' -f 2"
        LOG.info(pid_cmd)
        self.pid_msg = self.PrimaryNode.sh(pid_cmd).result()
        LOG.info('数据库进程为：' + self.pid_msg)

        LOG.info('--------------启动trace------------------')
        start_cmd = f'''source {macro.DB_ENV_PATH};
            gstrace start -p {self.pid_msg} -s 3;
            '''
        LOG.info(start_cmd)
        start_msg = self.PrimaryNode.sh(start_cmd).result()
        self.assertIn(self.constant.trace_start_success, start_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        stop_cmd = f'''source {macro.DB_ENV_PATH};
            gstrace stop -p {self.pid_msg};
            '''
        LOG.info(stop_cmd)
        stop_msg = self.PrimaryNode.sh(stop_cmd).result()
        LOG.info(stop_msg)
        LOG.info('---Opengauss_Function_Tools_Gs_Trace0024执行完成---')
