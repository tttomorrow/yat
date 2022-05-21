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
Case Name   : 创建普通用户并查看日志权限
Description :
    1.创建普通用户
    2.普通用户登录,并查看日志权限
    3.清理环境
Expect      :
    1.成功
    2.失败
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


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.user_name = 'u_security_mgt_manamegent_0011'

    def test_security(self):
        text = '----step1:创建普通用户 expect:创建成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
        create user {self.user_name}  password '{macro.PASSWD_REPLACE}';''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step2:普通用户登录,并查看日志权限 expect:失败----'
        self.logger.info(text)
        sql_cmd = f'''
            select type,result,username,database from pg_query_audit
            ('2001-01-01 00:00:00','now()') where 
            username = '{self.user_name}';'''
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} '
            f'-W {macro.PASSWD_REPLACE}')
        self.logger.info(msg)
        self.assertIn('permission denied to query audit', msg,
                      "执行失败:" + text)

    def tearDown(self):
        text = '----step3:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                        "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
