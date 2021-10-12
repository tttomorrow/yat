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
Case Type   : 功能测试
Case Name   : 对外表进行analyse
Description :
    1. 置参数enable_incremental_checkpoint为off并重启检查生效
    2. 创建外表并对其进行analyse
    3. 恢复参数enable_incremental_checkpoint为on并重启检查生效
Expect      : 
    1.默认值是off,设置成功
    2.外表创建成功，analyse执行成功
    3.设置成功，恢复为on
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.user_node = Node('dbuser')
        self.log = Logger()

    def test_test_directory(self):
        self.log.info("-----Opengauss_Function_DML_Set_Case0138开始-----")

        def set_para(value):  # 修改参数值并重启检查生效
            res = self.commonsh.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'enable_incremental_checkpoint={value}')
            self.assertTrue(res)
            self.commonsh.restart_db_cluster()
            status = self.commonsh.get_db_cluster_status()
            self.assertTrue("Normal" in status or 'Degraded' in status)
            res = self.commonsh.execute_gsguc(
                'check', f'{value}', 'enable_incremental_checkpoint')
            self.assertTrue(res)

        set_para('off')
        cmd = """drop foreign table if exists test;
                 create foreign table test(x int);
                 analyze verbose test;"""
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue('INFO:  analyzing "public.test"' in msg)

    def tearDown(self):
        cmd = """drop foreign table if exists test;"""
        self.commonsh.execut_db_sql(cmd)
        self.log.info("-----Opengauss_Function_DML_Set_Case0138结束-----")