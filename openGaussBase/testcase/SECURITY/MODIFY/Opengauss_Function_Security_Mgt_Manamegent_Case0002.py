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
Case Name   : 创建普通用户并修改口令
Description :
    1.创建普通用户
    2.普通用户登录数据库第一次修改口令
    3.普通用户登录数据库第二次修改口令
    4.普通用户登录数据库第三次修改口令
    5.清理环境
Expect      :
    1.成功
    2.成功
    3.成功
    4.失败
    5.成功
History     : 
"""


import os
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from yat.test import macro


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()
        self.user_name = 'u_security_mgt_manamegent_0002'

    def test_security(self):
        text = '----step1:创建用户 expect:创建成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            create user {self.user_name}  password '{macro.PASSWD_REPLACE}';
            ''')
        self.logger.info(sql_cmd)
        self.assertTrue(
            sql_cmd.count(self.Constant.CREATE_ROLE_SUCCESS_MSG) == 1,
            "执行失败:" + text)

        text = '----step2:普通用户登录数据库第一次修改口令 expect:成功----'
        self.logger.info(text)
        sql_cmd = f'''alter user {self.user_name} identified by 
            '{macro.PASSWD_REPLACE}_1' replace '{macro.PASSWD_REPLACE}';'''
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} '
            f'-W {macro.PASSWD_REPLACE}')
        self.logger.info(msg)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, msg,
                      "执行失败:" + text)

        text = '----step3:普通用户登录数据库第二次修改口令 expect:成功----'
        self.logger.info(text)
        sql_cmd = f'''alter user {self.user_name} identified by 
            '{macro.PASSWD_REPLACE}_2' replace '{macro.PASSWD_REPLACE}_1';'''
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} '
            f'-W {macro.PASSWD_REPLACE}_1')
        self.logger.info(msg)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, msg,
                      "执行失败:" + text)

        text = '----step4:普通用户登录数据库第三次修改口令 expect:失败----'
        self.logger.info(text)
        sql_cmd = f'''alter user {self.user_name} identified by 
            '{macro.PASSWD_REPLACE}' replace '{macro.PASSWD_REPLACE}_2';'''
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} '
            f'-W {macro.PASSWD_REPLACE}_2')
        self.logger.info(msg)
        self.assertIn('The password cannot be reused.', msg,
                      "执行失败:" + text)

    def tearDown(self):
        text = '----step5:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
        drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
