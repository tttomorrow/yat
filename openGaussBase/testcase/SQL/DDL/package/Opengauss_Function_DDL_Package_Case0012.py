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
Case Name   : 外部调用package声明的公有存储过程
Description :
    1.声明package
    2.定义package body
    3.定义存储过程调用包中定义的存储过程
    4.调用新建存储过程
    5.清理环境
Expect      :
    1.成功
    2.成功
    3.成功
    4.返回存储过程执行结果
    5.成功
History     :
"""

import os
import re
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class PACKAGE(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.package = 'p_test_0012'
        self.procedure = 'p_package_0012_01'
        self.procedure1 = 'p_package_0012_02'

    def test_package(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:声明package expect:成功'
        self.logger.info(step)
        spec_package = self.primary_sh.execut_db_sql(
            f'''create or replace package {self.package} is
            procedure {self.procedure}();
            end {self.package};''')
        self.logger.info(spec_package)
        self.assertIn(self.Con.create_package_success_msg, spec_package,
                      '执行失败' + step)

        step = 'step2:定义package body expect:成功'
        self.logger.info(step)
        def_package = self.primary_sh.execut_db_sql(
            f'''create or replace package body {self.package} is
            procedure {self.procedure}() is
            col_text text;
            begin
                col_text := (select timeofday());
                raise info 'col_text :%',col_text ;
            end;
            end {self.package};''')
        self.logger.info(def_package)
        self.assertIn(self.Con.create_package_body_success_msg, def_package,
                      '执行失败' + step)

        step = 'step3:定义存储过程调用包中定义的存储过程 expect:成功'
        self.logger.info(step)
        create_procedure = self.primary_sh.execut_db_sql(f'''
            create or replace procedure {self.procedure1}(out var1 text)
            is
            begin
               var1 := {self.package}.{self.procedure}();
            end;''')
        self.logger.info(create_procedure)
        self.assertIn(self.Con.CREATE_PROCEDURE_SUCCESS_MSG, create_procedure,
                      "执行失败" + step)

        step = 'step4:调用新建存储过程 expect:返回存储过程执行结果'
        self.logger.info(step)
        call_procedure = self.primary_sh.execut_db_sql(
            f'''call {self.procedure1}(null);''')
        self.logger.info(call_procedure)
        assert1 = re.search(r"col_text :.*", call_procedure, re.S)
        self.assertTrue(assert1, '执行失败:' + step)

    def tearDown(self):
        step = 'step5:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(
            f'''drop package {self.package};
            drop procedure {self.procedure1};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.DROP_PROCEDURE_SUCCESS_MSG, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.Con.drop_package_success_msg, clean_environment,
                      '执行失败' + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
