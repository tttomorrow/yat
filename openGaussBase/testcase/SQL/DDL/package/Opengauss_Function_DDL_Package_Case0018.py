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
Case Name   : 非A风格数据库下package定义存储过程,合理报错
Description :
    1.创建B风格数据库
    2.新建数据库下声明package
    3.清理环境
Expect      :
    1.成功
    2.合理报错
    3.成功
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
        self.database = 'd_package_0018'
        self.package = 'p_test_0018'
        self.procedure = 'p_package_0018'

    def test_package(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:创建B风格数据库 expect:成功'
        self.logger.info(step)
        create_database = self.primary_sh.execut_db_sql(
            f'''drop database if exists {self.database};
            create database {self.database} with dbcompatibility = 'B';''')
        self.logger.info(create_database)
        self.assertIn(self.Con.CREATE_DATABASE_SUCCESS, create_database,
                      '执行失败' + step)

        step = 'step2:新建数据库下声明package expect:合理报错'
        self.logger.info(step)
        spec_package = self.primary_sh.execut_db_sql(
            f'''create or replace package {self.package} is
            var1 int:=1;
            var2 int:=2;
            procedure {self.procedure}();
            end {self.package};''', dbname=self.database)
        self.logger.info(spec_package)
        text = 'ERROR:  Package only allowed create in A compatibility'
        self.assertIn(text, spec_package, '执行失败' + step)

    def tearDown(self):
        step = 'step3:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(
            f'''drop database {self.database};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.DROP_DATABASE_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
