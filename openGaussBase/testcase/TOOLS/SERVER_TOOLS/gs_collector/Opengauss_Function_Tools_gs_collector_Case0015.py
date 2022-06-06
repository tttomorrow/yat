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
Case Type   : 服务端工具
Case Name   : 收集日志信息时指定主机名称列表文件
Description :
    1.收集日志信息时指定主机名称列表文件
    2.清理环境
Expect      :
    1.收集日志信息成功
    2.清理环境
History     :
"""

import unittest
import time
import os
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.primary_dbuser = Node('PrimaryDbUser')
        self.primary_root = Node('PrimaryRoot')
        self.constant = Constant()
        self.logpath = os.path.join(os.path.dirname(macro.PG_LOG_PATH))

    def test_server_tools1(self):
        self.log.info(f'-----{os.path.basename(__file__)}start-----')

        self.log.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname)

        self.log.info('-----将主机名写入列表文件-----')
        echo_cmd = f'echo \'{hostname}\' ' \
            f'> /home/{self.primary_dbuser.ssh_user}/hostfile.txt'
        self.log.info(echo_cmd)
        echo_msg = self.primary_dbuser.sh(echo_cmd).result()
        self.log.info(echo_msg)

        self.log.info('----收集日志信息时指定主机名称--------')
        current_date = time.strftime("%Y%m%d", time.localtime())
        self.log.info(current_date)
        current_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(current_time)
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector --begin-time="{current_date} 00:00" ' \
            f' --end-time="{current_time}" ' \
            f'-f /home/{self.primary_dbuser.ssh_user}/hostfile.txt'
        self.log.info(collector_cmd)
        collector_msg = self.primary_dbuser.sh(collector_cmd).result()
        self.log.info(collector_msg)
        self.assertIn(self.constant.GS_COLLECTOR_SUCCESS_MSG, collector_msg)

        self.log.info('----查看日志是否生成--------')
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cd {self.logpath};' \
            f'tar -zxvf collector*.tar.gz;'
        self.log.info(collector_cmd)
        collector_msg = self.primary_dbuser.sh(collector_cmd).result()
        self.log.info(collector_msg)
        self.assertIn('Summary.log', collector_msg)
        self.assertIn('Detail.log', collector_msg)
        self.assertIn(f'{hostname}.tar.gz', collector_msg)

    def tearDown(self):
        self.log.info('------清理环境，删除生成的collector日志文件------')
        rm_cmd = f'cd {self.logpath};' \
            f'rm -rf collector_*;' \
            f'rm -rf /home/{self.primary_dbuser.ssh_user}/hostfile.txt'
        self.log.info(rm_cmd)
        rm_msg = self.primary_root.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info(f'-----{os.path.basename(__file__)}finish-----')
