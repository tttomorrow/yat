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
Case Name   : package声明ref cursor类型游标变量合理报错
Description :
    1.package声明ref cursor类型变量
Expect      :
    1.合理报错
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
        self.package = 'p_test_0010'
        self.type = 'cur_type'
        self.cursor = 'my_var'

    def test_package(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:package声明ref cursor类型变量 expect:合理报错'
        self.logger.info(step)
        spec_package = self.primary_sh.execut_db_sql(
            f'''create or replace package {self.package} is
            type {self.type} is ref cursor;
            {self.cursor} cur_type;
            end {self.package};''')
        self.logger.info(spec_package)
        text = 'ERROR:  not allow use ref cursor in package at or near ";"'
        self.assertIn(text, spec_package, '执行失败' + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
