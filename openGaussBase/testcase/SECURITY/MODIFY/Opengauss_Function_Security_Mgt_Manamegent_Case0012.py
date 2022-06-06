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
Case Name   : 对管理面所有的用户活动都必须有相应的审计日志记录
Description :
    1.查询failed_login_attempts值
    2.创建普通用户
    3.设置登录失败锁定次数为3次
    4.用错误密码第一次登录
    5.用错误密码第二次登录
    6.用错误密码第三次登录
    7.用正确密码第一次登录
    8.查看日志
    9.清理环境
Expect      :
    1.显示默认值10
    2.成功
    3.成功
    4.失败
    5.失败
    6.失败
    7.失败
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
        self.user_name = 'u_security_mgt_manamegent_0012'
        self.default_value = self.common.show_param('failed_login_attempts')

    def test_security(self):
        text = '----查询当前时间----'
        self.logger.info(text)
        current_time = self.dbuserNode.sh(f'date "+%Y-%m-%d %H:%M"').result()
        self.logger.info(current_time)
        text = '----step1:查询failed_login_attempts值; expect:默认值10----'
        self.logger.info(text)
        show_para = self.default_value
        self.logger.info(show_para)
        self.assertEqual("10", show_para, "执行失败:" + text)

        text = '----step2:创建用户 expect:创建成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
        create user {self.user_name}  password '{macro.PASSWD_REPLACE}';''')
        self.logger.info(sql_cmd)
        self.assertTrue(
            sql_cmd.count(self.Constant.CREATE_ROLE_SUCCESS_MSG) == 1,
            "执行失败:" + text)

        text = '----step3:设置登录失败锁定次数为3次;  expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
                    alter system set failed_login_attempts to 3;
                    select pg_sleep(2);
                    show failed_login_attempts;''')
        self.logger.info(sql_cmd)
        self.assertEqual("3", sql_cmd.split("\n")[-2].strip(),
                         "执行失败:" + text)

        text = '----step4:用错误密码第一次登录 expect:失败----'
        self.logger.info(text)
        msg = self.primary_sh.execut_db_sql(
        sql_cmd, sql_type=f' -U {self.user_name} -W {macro.PASSWD_REPLACE}_1')
        self.logger.info(msg)
        self.assertIn(self.Constant.INVALID_USERNAME_OR_PASSWD_TYPE, msg,
                      "执行失败:" + text)

        text = '----step5:用错误密码第二次登录 expect:失败----'
        self.logger.info(text)
        msg = self.primary_sh.execut_db_sql(
        sql_cmd, sql_type=f' -U {self.user_name} -W {macro.PASSWD_REPLACE}_2')
        self.logger.info(msg)
        self.assertIn(self.Constant.INVALID_USERNAME_OR_PASSWD_TYPE, msg,
                      "执行失败:" + text)

        text = '----step6:用错误密码第三次登录 expect:失败----'
        self.logger.info(text)
        msg = self.primary_sh.execut_db_sql(
        sql_cmd, sql_type=f' -U {self.user_name} -W {macro.PASSWD_REPLACE}_3')
        self.logger.info(msg)
        self.assertIn(self.Constant.INVALID_USERNAME_OR_PASSWD_TYPE, msg,
                      "执行失败:" + text)

        text = '----step7:用正确密码第一次登录 expect:失败----'
        self.logger.info(text)
        msg = self.primary_sh.execut_db_sql(
        sql_cmd, sql_type=f' -U {self.user_name} -W {macro.PASSWD_REPLACE}')
        self.logger.info(msg)
        self.assertIn(self.Constant.ACCOUNT_LOCKED_TYPE, msg,
                      "执行失败:" + text)

        text = '----step8:查看日志 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
                select time,type,result,username,database from pg_query_audit
                ('{current_time}','now()') where 
                username = '{self.user_name}'; ''')
        self.logger.info(sql_cmd)
        self.assertIn('login_failed' and 'lock_user', sql_cmd,
                      "执行失败:" + text)

    def tearDown(self):
        text = '----step9:清理环境 expect:成功----'
        self.logger.info(text)
        self.logger.info('删除用户')
        sql_cmd1 = self.primary_sh.execut_db_sql(f'''
            drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd1)
        self.logger.info('恢复默认值')
        sql_cmd2 = self.primary_sh.execut_db_sql(f'''
            alter system set failed_login_attempts to {self.default_value};
            select pg_sleep(2);
            show failed_login_attempts;''')
        self.logger.info(sql_cmd2)
        self.assertEqual("10", sql_cmd2.split("\n")[-2].strip(),
                         "执行失败:" + text)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd1,
                      '执行失败:' + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
