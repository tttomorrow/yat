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
Case Type   : 功能测试
Case Name   : 指定verbose模式（异常）
Description : 指定verbose模式.合理报错
Expect      : 执行失败
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Log = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Log.info("---Opengauss_Function_Tools_gs_restore_Case0005开始执行---")
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')

    def test_server_tools1(self):
        Log.info("----指定verbose模式,合理报错----")
        check_cmd = f'''source {macro.DB_ENV_PATH}
                        gs_restore -v
                         '''
        Log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        Log.info(msg)
        self.assertIn("Mandatory to specify dump \
filename/path for gs_restore", msg)

    def tearDown(self):
        Log.info('---------重启数据库---------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail;' \
            f'gs_om -t restart;'
        Log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        Log.info(msg)
        Log.info('----Opengauss_Function_Tools_gs_restore_Case0005执行结束----')
