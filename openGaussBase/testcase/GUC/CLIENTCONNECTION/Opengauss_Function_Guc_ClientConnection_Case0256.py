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
Case Name   : 修改参数dynamic_library_path,为其他数值，合理报错
Description :
    1.show参数默认值
    2.修改参数默认值为123#
    3.show参数值
Expect      :
    1.默认值是$libdir
    2.合理报错
    3.参数值不变
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
        self.log.info('Opengauss_Function_Guc_ClientConnection_Case0256开始')
        self.dbuser = Node('PrimaryDbUser')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_guc_developeroptions(self):
        error_msg1 = "The parameter('123#') exists illegal character:#"
        text = '--step1:show参数默认值;expect:默认值是$libdir--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show dynamic_library_path;')
        self.log.info(sql_cmd)
        default_value1 = sql_cmd.splitlines()[2].strip()
        self.log.info(default_value1)

        text = '--step2:修改参数默认值为123#--;expect:修改失败--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              error_msg1,
                                              f"dynamic_library_path = '123#'")
        self.log.info(mod_msg)
        self.assertTrue(mod_msg,  '执行失败:' + text)

        text = '--step3:show参数值--;expect:参数值不变--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show dynamic_library_path;')
        self.log.info(sql_cmd)
        self.assertIn(default_value1, sql_cmd,  '执行失败:' + text)

    def tearDown(self):
        self.log.info('Opengauss_Function_Guc_ClientConnection_Case0256结束')
