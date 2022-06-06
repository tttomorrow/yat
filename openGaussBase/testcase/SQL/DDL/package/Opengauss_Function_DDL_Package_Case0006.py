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
Case Type   : PACKAGE
Case Name   : 创建package,指定权限为定义者执行权限
Description :
    1.修改guc参数behavior_compat_options
    2.创建用户
    3.新建用户身份声明package
    4.新建用户身份定义package body
    5.回收新建用户在用户模式上的create权限
    6.切换至新建用户模式,调用package
    7.清理环境
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.合理报错
    7.成功
History     :
"""

import os
import unittest
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class PACKAGE(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.common = Common()
        self.user = 'u_package_0006'
        self.table = 't_package_0006'
        self.package = 'p_test_0006'
        self.procedure = 'p_package_0006'

    def test_package(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:修改guc参数behavior_compat_options expect:成功'
        self.logger.info(step)
        self.param = self.common.show_param(
            'behavior_compat_options')
        if 'plsql_security_definer' not in self.param:
            modify_param = self.primary_sh.execute_gsguc("reload",
                                                         f'''{self.Con.
                                                         GSGUC_SUCCESS_MSG}'''
                                                         , f"behavior_compat_"
                                                         f"options="
                                                         f"'plsql_security_"
                                                         f"definer'",
                                                         single=False)
            self.logger.info(modify_param)
            self.assertTrue(modify_param, "执行失败" + step)

        step = 'step2:创建用户 expect:成功'
        self.logger.info(step)
        create_user = self.primary_sh.execut_db_sql(f'''
            drop user if exists {self.user} cascade;
            create user {self.user} with password '{macro.PASSWD_REPLACE}';''')
        self.logger.info(create_user)
        self.assertIn(self.Con.CREATE_ROLE_SUCCESS_MSG, create_user,
                      "执行失败" + step)

        step = 'step3:新建用户身份声明package expect:成功'
        self.logger.info(step)
        spec_package = self.primary_sh.execut_db_sql(
            f'''create or replace package {self.package} authid definer is
            var1 int:=1;
            var2 int:=2;
            procedure {self.procedure}();
            end {self.package};''',
            sql_type=f" -U {self.user} -W '{macro.PASSWD_REPLACE}'")
        self.logger.info(spec_package)
        self.assertIn(self.Con.create_package_success_msg, spec_package,
                      '执行失败' + step)

        step = 'step4:新建用户身份定义package body expect:成功'
        self.logger.info(step)
        def_package = self.primary_sh.execut_db_sql(
            f'''create or replace package body {self.package} is
            procedure {self.procedure}()
            is
            begin
                drop table if exists {self.user}.{self.table};
                create table {self.user}.{self.table}(c_int int);
                insert into {self.user}.{self.table} values(var1),(var2);
            end;
            end {self.package};''',
            sql_type=f" -U {self.user} -W '{macro.PASSWD_REPLACE}'")
        self.logger.info(def_package)
        self.assertIn(self.Con.create_package_body_success_msg, def_package,
                      '执行失败' + step)

        step = 'step5:回收新建用户在用户模式上的create权限 expect:成功'
        self.logger.info(step)
        revoke_pri = self.primary_sh.execut_db_sql(f'''
            revoke create on schema {self.user} from {self.user};''')
        self.logger.info(revoke_pri)
        self.assertIn('REVOKE', revoke_pri, "执行失败" + step)

        step = 'step6:切换至新建用户模式,调用package expect:合理报错'
        self.logger.info(step)
        invoke_package = self.primary_sh.execut_db_sql(
            f'''set current_schema = {self.user}; 
                call {self.package}.{self.procedure}();''')
        self.logger.info(invoke_package)
        text = f'ERROR:  permission denied for schema {self.user}'
        self.assertIn('SET', invoke_package, "执行失败" + step)
        self.assertIn(text, invoke_package, "执行失败" + step)

    def tearDown(self):
        step = 'step7:清理环境 expect:清理环境成功'
        self.logger.info(step)
        self.param = self.common.show_param(
            'behavior_compat_options')
        clean_environment = self.primary_sh.execut_db_sql(
            f'''drop package {self.package};''',
            sql_type=f" -U {self.user} -W '{macro.PASSWD_REPLACE}'")
        self.logger.info(clean_environment)
        clean_environment1 = self.primary_sh.execut_db_sql(
            f'''drop user {self.user};''')
        self.logger.info(clean_environment1)
        if len(self.param):
            modify_param = self.primary_sh.execute_gsguc("reload",
                                                         f'''{self.Con.
                                                         GSGUC_SUCCESS_MSG}'''
                                                         , f"behavior_compat_"
                                                         f"options=''"
                                                         , single=False)
            self.logger.info(modify_param)
            self.assertTrue(modify_param, "执行失败" + step)
        self.assertIn(self.Con.drop_package_success_msg, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.Con.DROP_ROLE_SUCCESS_MSG, clean_environment1,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
