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
Case Type   : GUC参数
Case Name   : 修改参数gin_fuzzy_search_limit,为其他数值及超边界值，合理报错
Description :
    1.show参数默认值
    2.修改参数默认值为abc
    3.修改参数默认值为2147483648
Expect      :
    1.数默认值为0
    2.修改参数默认值为abc，合理报错
    3.修改参数默认值为2147483648，合理报错
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Guc_ClientConnection_Case0258开始')
        self.dbuser = Node('PrimaryDbUser')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_guc_developeroptions(self):
        error_msg1 = "ERROR: The parameter \"gin_fuzzy_search_limit\" " \
                     "requires an integer value"
        error_msg2 = "ERROR: The value 2147483648 is outside the valid " \
                     "range for parameter \"gin_fuzzy_search_limit\" " \
                     "(0 .. 2147483647)."

        text = '--step1:show参数默认值;expect:默认值是0--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show gin_fuzzy_search_limit;')
        self.log.info(sql_cmd)
        default_value1 = sql_cmd.splitlines()[2].strip()
        self.log.info(default_value1)

        text = '--step2:修改参数默认值为abc;expect:合理报错--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              error_msg1,
                                              f"gin_fuzzy_search_limit='abc'")
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)

        text = '--step3:.修改参数默认值为2147483648;expect:合理报错--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              error_msg2,
                                              f"gin_fuzzy_search_limit"
                                              f"=2147483648")
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)

    def tearDown(self):
        self.log.info('Opengauss_Function_Guc_ClientConnection_Case0258结束')
