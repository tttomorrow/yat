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
Case Type   : 防篡改
Case Name   : 验证口令与用户名关联加密
Description :
    1.创建用户
    2.查看用户的口令字段值
    3.清理环境
Expect      :
    1.成功
    2.加密显示
    3.成功
History     :
"""


import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import macro


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.user_name1 = 'u_security_mgt_manamegent_0003_1'
        self.user_name2 = 'u_security_mgt_manamegent_0003_2'

    def test_security(self):
        text = '----step1:创建用户 expect:创建成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
        create user {self.user_name1}  password '{macro.PASSWD_REPLACE}';
        create user {self.user_name2}  password '{macro.PASSWD_REPLACE}';''')
        self.logger.info(sql_cmd)
        self.assertTrue(
            sql_cmd.count(self.Constant.CREATE_ROLE_SUCCESS_MSG) == 2,
            "执行失败:" + text)

        text = '----step2:查看用户的口令字段值 expect:加密显示----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            select rolpassword from pg_authid where 
            rolname='{self.user_name1}' 
            minus(select rolpassword from pg_authid where 
            rolname='{self.user_name2}');''')
        self.logger.info(sql_cmd)
        self.assertIn('sha256', sql_cmd, "执行失败:" + text)

    def tearDown(self):
        text = '----step3:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
        drop user {self.user_name1} cascade;
        drop user {self.user_name2} cascade;''')
        self.logger.info(sql_cmd)
        self.assertTrue(
            sql_cmd.count(self.Constant.DROP_ROLE_SUCCESS_MSG) == 2,
            "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
