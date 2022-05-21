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
Case Name   : 创建package,指定权限为调用者执行权限
Description :
    1.声明package
    3.定义package body
    3.创建用户
    4.创建表
    5.回收新建用户在表上的insert权限
    6.新建用户进入数据库,切换模式至public,调用package
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
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class PACKAGE(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.user = 'u_package_0008'
        self.table = 't_package_0008'
        self.package = 'p_test_0008'
        self.procedure = 'p_package_0008'

    def test_package(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:声明package expect:成功'
        self.logger.info(step)
        spec_package = self.primary_sh.execut_db_sql(
            f'''create or replace package {self.package} is
            var1 int:=1;
            var2 int:=2;
            procedure {self.procedure}();
            end {self.package};''')
        self.logger.info(spec_package)
        self.assertIn(self.Con.create_package_success_msg, spec_package,
                      '执行失败' + step)

        step = 'step2:定义package body expect:成功'
        self.logger.info(step)
        def_package = self.primary_sh.execut_db_sql(
            f'''create or replace package body {self.package} is
            procedure {self.procedure}()
            is
            begin
                insert into {self.table} values(var1),(var2);
            end;
            end {self.package};''')
        self.logger.info(def_package)
        self.assertIn(self.Con.create_package_body_success_msg, def_package,
                      '执行失败' + step)

        step = 'step3:创建用户 expect:成功'
        self.logger.info(step)
        create_user = self.primary_sh.execut_db_sql(f'''
            drop user if exists {self.user} cascade;
            create user {self.user} with password '{macro.PASSWD_REPLACE}';''')
        self.logger.info(create_user)
        self.assertIn(self.Con.CREATE_ROLE_SUCCESS_MSG, create_user,
                      "执行失败" + step)

        step = 'step4:新建表 expect:成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table};
            create table {self.table}(c_int int);''')
        self.logger.info(create_table)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, create_table, '执行失败'
                      + step)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table, '执行失败'
                      + step)

        step = 'step5:回收新建用户在表上的insert权限 expect:成功'
        self.logger.info(step)
        revoke_pri = self.primary_sh.execut_db_sql(f'''
            revoke insert on table {self.table} from {self.user};''')
        self.logger.info(revoke_pri)
        self.assertIn('REVOKE', revoke_pri, "执行失败" + step)

        step = 'step6:新建用户进入数据库,切换模式至public,调用package ' \
               'expect:合理报错'
        self.logger.info(step)
        invoke_package = self.primary_sh.execut_db_sql(
            f'''set current_schema = public; 
                call {self.package}.{self.procedure}();''',
            sql_type=f" -U {self.user} -W '{macro.PASSWD_REPLACE}'")
        self.logger.info(invoke_package)
        text = f'ERROR:  permission denied for package {self.package}'
        self.assertIn('SET', invoke_package, "执行失败" + step)
        self.assertIn(text, invoke_package, "执行失败" + step)

    def tearDown(self):
        step = 'step7:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(
            f'''drop package {self.package};
            drop table {self.table};
            drop user {self.user};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.drop_package_success_msg, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      '执行失败' + step)
        self.assertIn(self.Con.DROP_ROLE_SUCCESS_MSG, clean_environment,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
