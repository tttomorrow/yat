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
Case Name   : 创建普通用户并修改口令,不需要普通用户的旧密码以及旧密码可以不正确
Description :
    1.创建普通用户
    2.管理员第一次修改普通用户密码
    密码修改成功后切换用户验证密码是否修改成功
    3.管理员第二次修改普通用户密码
    密码修改成功后切换用户验证密码是否修改成功
    4.管理员第三次修改普通用户密码
    密码修改成功后切换用户验证密码是否修改成功
    5.清理环境
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
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
        self.user_name = 'u_security_mgt_manamegent_0006'

    def test_security(self):
        text = '----step1:创建用户 expect:创建成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            create user {self.user_name}  password '{macro.PASSWD_REPLACE}';
            ''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step2:管理员第一次修改普通用户密码,旧密码正确' \
               '密码修改成功后切换用户验证密码是否修改成功 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter user {self.user_name} identified by 
            '{macro.PASSWD_REPLACE}_1' replace '{macro.PASSWD_REPLACE}';
            set role {self.user_name} password '{macro.PASSWD_REPLACE}_1';
            select current_user;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG and
                      f'{self.user_name}', sql_cmd, "执行失败:" + text)

        text = '----step3:管理员第二次修改普通用户密码,不需要旧密码' \
               '密码修改成功后切换用户验证密码是否修改成功 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter user {self.user_name} identified by 
            '{macro.PASSWD_REPLACE}_2';
            set role {self.user_name} password '{macro.PASSWD_REPLACE}_2';
            select current_user;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(f'{self.user_name}', sql_cmd, "执行失败:" + text)

        text = '----step4:管理员第三次修改普通用户密码,旧密码不正确' \
               '密码修改成功后切换用户验证密码是否修改成功 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter user {self.user_name} identified by 
            '{macro.PASSWD_REPLACE}_3' replace '{macro.PASSWD_REPLACE}_4';
            set role {self.user_name} password '{macro.PASSWD_REPLACE}_3';
            select current_user;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG and
                      f'{self.user_name}', sql_cmd, "执行失败:" + text)

    def tearDown(self):
        text = '----step5:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
        drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
