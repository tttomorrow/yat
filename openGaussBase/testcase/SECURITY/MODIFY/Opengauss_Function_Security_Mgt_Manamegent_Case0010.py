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
Case Name   : 对管理面所有的用户活动都必须有相应的日志记录
Description :
    1.创建普通用户
    2.修改用户密码
    3.锁定用户
    4.解锁用户
    5.赋予权限
    6.收回权限
    7.普通用户登录并修改自己密码
    8.删除普通用户
    9.查看日志
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.成功
    7.成功
    8.成功
    9.成功
History     : 
"""



import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()
        self.user_name = 'u_security_mgt_manamegent_0010'

    def test_security(self):
        text = '----查询当前时间----'
        self.logger.info(text)
        current_time = self.dbuserNode.sh(f'date "+%Y-%m-%d %H:%M"').result()
        self.logger.info(current_time)
        text = '----step1:创建用户 expect:创建成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            create user {self.user_name}  password 
            '{macro.PASSWD_REPLACE}';''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step2:修改用户密码 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter user {self.user_name} identified by 
            '{macro.PASSWD_REPLACE}_1';''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step3:锁定用户 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter user {self.user_name} account lock;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step4:解锁用户 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter user {self.user_name} account unlock;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step5:赋予权限 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            grant select on table pg_user to {self.user_name};''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step6:回收权限 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
                    revoke select on table pg_user from {self.user_name};''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.REVOKE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step7:普通用户登录并修改自己的密码 expect:成功----'
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

        text = '----step8:删除普通用户 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
                    drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd)
        self.assertTrue(
            sql_cmd.count(self.Constant.DROP_ROLE_SUCCESS_MSG) == 1,
            "执行失败:" + text)

        text = '----step9:查看日志 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            select time,type,result,username,database from pg_query_audit
            ('{current_time}','now()') where 
            username = '{self.user_name}'; ''')
        self.logger.info(sql_cmd)
        self.assertIn('login_success' and 'set_parameter' and 'ddl_user' and
                      'user_logout', sql_cmd, "执行失败:" + text)

    def tearDown(self):
        self.logger.info(f'-----无需清理环境-----')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
