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
Case Name   : 逻辑复制pg_recvlogical 指定参数-V,输出版本信息，随后立即退出
Description :
        1.指定参数-V,查看版本信息
        pg_recvlogical -V
Expect      :
        1.输出版本信息，随后立即退出
History     :
"""
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Tools_pg_recvlogical_Case0021 start-')
        self.primary_node = Node('PrimaryDbUser')

    def test_standby(self):
        text = 'step1:逻辑复制pg_recvlogical 指定参数-V;expect:输出版本信息--'
        self.log.info(text)
        execute_cmd = f"pg_recvlogical -V "
        self.log.info(execute_cmd)
        exec_msg = self.primary_node.sh(f"source {macro.DB_ENV_PATH};"
                                        f"{execute_cmd}").result()
        self.log.info(exec_msg)
        self.assertIn("pg_recvlogical", exec_msg)
        self.assertIn("openGauss", exec_msg)

    def tearDown(self):
        self.log.info('--无需恢复环境--')
        self.log.info(
            '-Opengauss_Function_Tools_pg_recvlogical_Case0021 finish--')
