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
Case Name   : 三权分立打开时验证createrole用户权限的revoke
Description :
    1.设置参数并重启数据库enableSeparationOfDuty=on
    2.创建用户和数据库
    3.新用户连接新数据库查询用户
    4.回收用户连接数据库权限
    5.回收权限后新用户连接新数据库查询用户
    6.回收数据库connect权限
    7.回收权限后新用户连接新数据库查询用户
    8.清理环境
Expect      :
    1.成功
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
        self.constant = Constant()
        self.common = Common()
        self.user_name = 'u_security_rgprivilege_0002'
        self.database_name = 'd_security_rgprivilege_0002'
        self.default_value = self.common.show_param('enableSeparationOfDuty')

    def test_security(self):
        text = '-----step1：设置参数并重启数据库enableSeparationOfDuty=on; ' \
               'expect:成功-----'
        self.logger.info(text)
        mod_msg = \
            self.primary_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'enableSeparationOfDuty=on')
        self.logger.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.logger.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '----step2:创建用户和数据库 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop user if exists {self.user_name};
            drop database if exists {self.database_name};
            create user {self.user_name} createrole password 
            '{macro.PASSWD_REPLACE}';
            create database {self.database_name};''')
        self.logger.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
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
        self.assertIn(self.constant.REVOKE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step5:回收权限后新用户连接新数据库查询用户 ' \
               'expect:成功显示新用户--'
        self.logger.info(text)
        sql_cmd = f'select user;'
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} -W '
            f'{macro.PASSWD_REPLACE}', dbname=f'{self.database_name}')
        self.logger.info(msg)
        self.assertIn(self.user_name, msg, "执行失败:" + text)

        text = '----step6:回收数据库connect权限 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'revoke connect on database '
                                                f'{self.database_name} from '
                                                f'public;')
        self.logger.info(sql_cmd)
        self.assertIn(self.constant.REVOKE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step7:回收权限后新用户连接新数据库查询用户 ' \
               'expect:权限拒绝--'
        self.logger.info(text)
        sql_cmd = f'select user;'
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} -W '
            f'{macro.PASSWD_REPLACE}', dbname=f'{self.database_name}')
        self.logger.info(msg)
        self.assertIn(self.constant.PERMISSION_DENIED, msg, "执行失败:" + text)

    def tearDown(self):
        text = '----step8:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop database {self.database_name};
            drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd)
        self.logger.info('恢复参数默认值')
        mod_msg1 = \
            self.primary_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f'enableSeparationOfDuty='
                                          f'{self.default_value}')
        self.logger.info(mod_msg1)
        self.assertTrue(mod_msg1, '执行失败:' + text)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.logger.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd,
                      "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
