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
Case Name   : 指定的日志文件以及存放路径
Description :
    1.创建指定文件夹
    2.指定的日志文件以及存放路径
    3.清理环境
Expect      :
    1.创建指定文件夹成功
    2.收集日志信息成功
    3.清理环境
History     :
"""

import unittest
import time
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

    def test_server_tools1(self):
        self.log.info('-Opengauss_Function_Tools_gs_collector_Case0021开始-')

        self.log.info("---创建指定文件夹---")
        mkdir_cmd = f"mkdir /home/test_collector/ ;" \
            f"chmod -R 777 /home/test_collector/"
        self.log.info(mkdir_cmd)
        mkdir_msg = self.primary_root.sh(mkdir_cmd).result()
        self.log.info(mkdir_msg)

        self.log.info('----指定的日志文件以及存放路径--------')
        current_date = time.strftime("%Y%m%d", time.localtime())
        self.log.info(current_date)
        current_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(current_time)
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector --begin-time="{current_date} 00:00"  ' \
            f'--end-time="{current_time}" -o ' \
            f'/home/test_collector/test_collector.log'
        self.log.info(collector_cmd)
        collector_msg = self.primary_dbuser.sh(collector_cmd).result()
        self.log.info(collector_msg)
        self.assertIn(self.constant.GS_COLLECTOR_SUCCESS_MSG, collector_msg)

        self.log.info('----查看日志是否生成--------')
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cd /home/test_collector/;' \
            f'ls'
        self.log.info(collector_cmd)
        collector_msg = self.primary_dbuser.sh(collector_cmd).result()
        self.log.info(collector_msg)
        self.assertIn('test_collector.log', collector_msg)

    def tearDown(self):
        self.log.info('------清理环境，删除生成的collector日志文件------')
        rm_cmd = f'rm -rf /home/test_collector'
        self.log.info(rm_cmd)
        rm_msg = self.primary_root.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_collector_Case0021结束-')
