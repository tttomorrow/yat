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
Case Name   : 创建package,名称含特殊字符
Description :
    1.声明package,名称含特殊字符
    2.定义package body
    3.调用package,查询表数据
    4.清理环境
Expect      :
    1.成功
    2.成功
    3.返回package函数执行结果
    4.成功
History     :
"""

import os
import unittest
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
        self.table = 't_package_0016'
        self.procedure = 'p_package_0016'

    def test_package(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:声明package,名称含特殊字符 expect:成功'
        self.logger.info(step)
        spec_package = self.primary_sh.execut_db_sql(
            f'''create or replace package ￥ is
            var1 text:='text_var1';
            var2 text:='text_var2';
            procedure p_package_0016();
            end ￥;''')
        self.logger.info(spec_package)
        self.assertIn(self.Con.create_package_success_msg, spec_package,
                      '执行失败' + step)

        step = 'step2:定义package body expect:成功'
        self.logger.info(step)
        def_package = self.primary_sh.execut_db_sql(
            f'''create or replace package body ￥ is
            procedure {self.procedure}()
            is
            begin
            drop table if exists {self.table};
            create table {self.table}(c_text text);
            insert into {self.table} values(var1),(var2);
            end;
            end ￥;''')
        self.logger.info(def_package)
        self.assertIn(self.Con.create_package_body_success_msg, def_package,
                      '执行失败' + step)

        step = 'step3:调用package,查询表数据 expect:返回package函数执行结果'
        self.logger.info(step)
        invoke_package = self.primary_sh.execut_db_sql(
            f'''call ￥.{self.procedure}();
            select * from {self.table};''')
        self.logger.info(invoke_package)
        self.assertIn('text_var1', invoke_package, "执行失败" + step)
        self.assertIn('text_var2', invoke_package, "执行失败" + step)

    def tearDown(self):
        step = 'step4:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(
            f'''drop package ￥;
            drop table {self.table};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.drop_package_success_msg, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
