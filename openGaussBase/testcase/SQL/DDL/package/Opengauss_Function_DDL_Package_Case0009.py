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
    2.定义package body
    3.外部建存储过程
    4.使用参数var1,var2调用存储过程并查询表数据
    5.清理环境
Expect      :
    1.成功
    2.成功
    3.成功
    4.调用成功,返回package中存储过程执行后的表数据
    5.成功
History     :
"""

import os
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class PACKAGE(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.table = 't_package_0009'
        self.package = 'p_test_0009'
        self.procedure = 'p_package_0009'

    def test_package(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:声明package expect:成功'
        self.logger.info(step)
        spec_package = self.primary_sh.execut_db_sql(
            f'''create or replace package {self.package} is
            var1 text:= 'test_var1';
            var2 varchar(10):= 'test_var2';
            end {self.package};''')
        self.logger.info(spec_package)
        self.assertIn(self.Con.create_package_success_msg, spec_package,
                      '执行失败' + step)

        step = 'step2:定义package body expect:成功'
        self.logger.info(step)
        def_package = self.primary_sh.execut_db_sql(
            f'''create or replace package body {self.package} is
            var3 int:= 2;
            end {self.package};''')
        self.logger.info(def_package)
        self.assertIn(self.Con.create_package_body_success_msg, def_package,
                      '执行失败' + step)

        step = 'step3:外部建存储过程 expect:成功'
        self.logger.info(step)
        create_procedure = self.primary_sh.execut_db_sql(f'''
            create or replace procedure {self.procedure}() is
            begin
            drop table if exists {self.table};
            create table {self.table}(col_text text,col1_text varchar(10));
            insert into {self.table} values({self.package}.var1,
            {self.package}.var2);
            end;''')
        self.logger.info(create_procedure)
        self.assertIn(self.Con.CREATE_PROCEDURE_SUCCESS_MSG, create_procedure,
                      "执行失败" + step)

        step = 'step4:使用参数var1,var2调用存储过程并查询表数据 expect:成功'
        self.logger.info(step)
        call_procedure = self.primary_sh.execut_db_sql(
            f'''call {self.procedure}();
            select * from {self.table};''')
        self.logger.info(call_procedure)
        self.assertIn('test_var1', call_procedure, "执行失败" + step)
        self.assertIn('test_var2', call_procedure, "执行失败" + step)

    def tearDown(self):
        step = 'step5:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(
            f'''drop package {self.package};
            drop table {self.table};
            drop procedure {self.procedure};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.DROP_PROCEDURE_SUCCESS_MSG, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      '执行失败' + step)
        self.assertIn(self.Con.drop_package_success_msg, clean_environment,
                      '执行失败' + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
