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
Case Name   : 三权分立关闭时验证普通用户public的权限
Description :
    1.查询三权分立参数enableSeparationOfDuty值
    2.创建用户
    3.创建函数
    4.新用户连接新数据库创建表并调用函数
    5.清理环境
Expect      :
    1.显示默认值off
    2.成功
    3.成功
    4.表创建失败，函数调用成功
    5.成功
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
        self.user_name = 'u_security_rgprivilege_0016'
        self.table_name = 't_security_rgprivilege_0016'
        self.function_name = 'f_security_rgprivilege_0016'
        self.default_value = self.common.show_param('enableSeparationOfDuty')

    def test_security(self):
        text = '----step1:查询三权分立参数enableSeparationOfDuty值  ' \
               'expect:默认值off----'
        self.logger.info(text)
        show_para = self.default_value
        self.logger.info(show_para)
        self.assertEqual("off", show_para, "执行失败:" + text)

        text = '----step2:创建用户 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop user if exists {self.user_name};
            create user {self.user_name} password '{macro.PASSWD_REPLACE}';''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step3:创建函数 expect:成功--'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop function if exists public.{self.function_name};
            create or replace function public.{self.function_name}() 
            return integer AS BEGIN RETURN 1;END;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step4:新用户连接新数据库创建表并调用函数 ' \
               'expect:表创建失败，函数调用成功--'
        self.logger.info(text)
        sql_cmd = f'drop table if exists public.{self.table_name};' \
            f'create table public.{self.table_name}(a int);' \
            f'call public.{self.function_name}();'
        self.logger.info(sql_cmd)
        msg = self.primary_sh.execut_db_sql(
            sql_cmd, sql_type=f' -U {self.user_name} -W '
            f'{macro.PASSWD_REPLACE}')
        self.logger.info(msg)
        self.assertIn('1 row', msg, "执行失败:" + text)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg, "执行失败:" + text)

    def tearDown(self):
        text = '----step5:清理环境 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            drop function public.{self.function_name};
            drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.Constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
