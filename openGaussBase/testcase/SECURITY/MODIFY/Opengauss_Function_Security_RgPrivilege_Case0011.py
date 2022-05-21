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
Case Name   : 三权分立关闭时验证auditadmin用户权限的revoke
Description :
    1.查询三权分立参数enableSeparationOfDuty值
    2.创建用户和数据库
    3.新用户连接新数据库查询用户
    4.回收用户连接数据库权限
    5.回收权限后新用户连接新数据库查询用户
    6.回收数据库connect权限
    7.回收权限后新用户连接新数据库查询用户
    8.清理环境
Expect      :
    1.显示默认值off
    2.成功
    3.显示新用户名
    4.成功
    5.显示新用户名
    6.成功
    7.权限拒绝
    8.成功
History     :
"""


import os
import unittest
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()
        self.user_name = 'u_security_rgprivilege_0011'
        self.database_name = 'd_security_rgprivilege_0011'
        self.default_value = self.common.show_param('enableSeparationOfDuty')

    def test_security(self):
        text = '----step1:查询三权分立参数enableSeparationOfDuty值  ' \
               'expect:默认值off----'
        self.logger.info(text)
        show_para = self.default_value
        self.logger.info(show_para)
        self.assertEqual("off", show_para, "执行失败:" + text)

        text = '----step2:创建用户和数据库 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop user if exists {self.user_name};
            drop database if exists {self.database_name};
            create user {self.user_name} auditadmin password 
            '{macro.PASSWD_REPLACE}';
            create database {self.database_name};''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      "执行失败:" + text)

        text = '----step3:新用户连接新数据库查询用户 expect:成功显示新用户--'
        self.logger.info(text)
        sql_cmd = f'select user;'
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} -W '
            f'{macro.PASSWD_REPLACE}', dbname=f'{self.database_name}')
        self.logger.info(msg)
        self.assertIn(self.user_name, msg, "执行失败:" + text)

        text = '----step4:回收用户连接数据库权限 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'revoke connect on database '
                                                f'{self.database_name} from '
                                                f'{self.user_name};')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.REVOKE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step5:回收用户权限后新用户连接新数据库查询用户 ' \
               'expect:成功显示新用户--'
        self.logger.info(text)
        sql_cmd = f'select user;'
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} -W '
            f'{macro.PASSWD_REPLACE}', dbname=f'{self.database_name}')
        self.logger.info(msg)
        self.assertIn(self.user_name, msg, "执行失败:" + text)

        text = '----step6:回收用户连接数据库权限 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'revoke connect on database '
                                                f'{self.database_name} from '
                                                f'public;')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.REVOKE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step7:回收public权限后新用户连接新数据库查询用户 ' \
               'expect:权限拒绝--'
        self.logger.info(text)
        sql_cmd = f'select user;'
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} -W '
            f'{macro.PASSWD_REPLACE}', dbname=f'{self.database_name}')
        self.logger.info(msg)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg, "执行失败:" + text)

    def tearDown(self):
        text = '----step8:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop database {self.database_name};
            drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.Constant.DROP_DATABASE_SUCCESS, sql_cmd,
                      "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
