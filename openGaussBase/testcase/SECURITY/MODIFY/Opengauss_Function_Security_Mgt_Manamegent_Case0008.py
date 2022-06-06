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
Case Name   : 用户修改自身口令检查
Description :
    1.创建用户
    2.以用户2登录并修改用户1的密码
    3.用户2登录,修改自己密码且不输入旧密码
    4.以用户2登录并修改自己的密码,密码修改成功后切换用户2验证密码是否修改成功
    5.清理环境
Expect      :
    1.成功
    2.失败
    3.失败
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


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.user_name1 = 'u_security_mgt_manamegent_0008_01'
        self.user_name2 = 'u_security_mgt_manamegent_0008_02'

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

        text = '----step2:用户2登录,并修改用户1的密码 expect:失败----'
        self.logger.info(text)
        sql_cmd = f'''alter user {self.user_name1} identified by 
            '{macro.PASSWD_REPLACE}_1' replace '{macro.PASSWD_REPLACE}';'''
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name2} '
            f'-W {macro.PASSWD_REPLACE}')
        self.logger.info(msg)
        self.assertIn(self.Constant.PERMISSION_DENY_MSG, msg,
                      "执行失败:" + text)

        text = '----step3:用户2登录,修改自己密码且不输入旧密码 expect:失败----'
        self.logger.info(text)
        sql_cmd = f'''
            alter user {self.user_name2} identified by  
            '{macro.PASSWD_REPLACE}_1';'''
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name2} '
            f'-W {macro.PASSWD_REPLACE}')
        self.logger.info(msg)
        self.assertIn('The old password can not be NULL', msg,
                      "执行失败:" + text)

        text = '----step4:用户2登录,并修改自己的密码' \
               '密码修改成功后切换用户验证密码是否修改成功 expect:成功----'
        self.logger.info(text)
        sql_cmd = f'''alter user {self.user_name2} identified by 
            '{macro.PASSWD_REPLACE}_1' replace '{macro.PASSWD_REPLACE}';
            set role {self.user_name2} password '{macro.PASSWD_REPLACE}_1';
            select current_user;'''
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name2} '
            f'-W {macro.PASSWD_REPLACE}')
        self.logger.info(msg)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG and
                      f'{self.user_name2}', msg, "执行失败:" + text)

    def tearDown(self):
        text = '----step5:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop user {self.user_name1} cascade;
            drop user {self.user_name2} cascade;''')
        self.logger.info(sql_cmd)
        self.assertTrue(
            sql_cmd.count(self.Constant.DROP_ROLE_SUCCESS_MSG) == 2,
            "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
