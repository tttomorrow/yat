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
Case Type   : 服务端工具
Case Name   : 日志收集（root用户）
Description : root用户进行日志收集
Expect      : 收集失败
History     :
"""

import time
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Tools_gs_collector_Case0040start-----')
        self.pri_root = Node('PrimaryRoot')
        self.result = "Cannot run this script as a " \
                      "user with the root permission"

    def test_server_tools1(self):
        self.log.info('---------获取收集日志的时间---------')
        current_date = time.strftime("%Y%m%d", time.localtime())
        self.log.info(current_date)
        current_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(current_time)
        self.log.info('--------------root用户进行日志收集---------------')
        check_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector ' \
            f'--begin-time="{current_date} 00:00" ' \
            f'--end-time="{current_time}" ;'
        self.log.info(check_cmd1)
        msg1 = self.pri_root.sh(check_cmd1).result()
        self.log.info(msg1)
        self.assertIn(self.result, msg1)

    def tearDown(self):
        self.log.info('--------------无需清理环境-------------------')
        self.log.info('Opengauss_Function_Tools_gs_collector_Case0040finish')
