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
Case Name   : 修改参数enable_nestloop为其他数据类型，观察预期结果
Description :
    1.show参数默认值
    2.修改参数默认值为test
    3.修改参数默认值为9999999999
Expect      :
    1.参数默认值为off
    2.修改参数默认值为test，合理报错
    3.修改参数默认值为9999999999，合理报错
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
        self.log.info('Opengauss_Function_Guc_Parameter_Case1262开始')
        self.dbuser = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_guc_parameter(self):
        text = '--step1:show参数默认值;expect:参数默认值off--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show enable_nestloop;')
        self.log.info(sql_cmd)
        default_value = sql_cmd.splitlines()[2].strip()
        self.log.info(default_value)
        error_msg1 = 'ERROR: The value "test" for parameter' \
                     ' "enable_nestloop" is incorrect, ' \
                     'requires a boolean value'
        error_msg2 = 'ERROR: The value "9999999999" for parameter ' \
                     '"enable_nestloop" is incorrect, ' \
                     'requires a boolean value'
        text = '--step2.修改参数默认值为test--;expect:合理报错--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              error_msg1,
                                              'enable_nestloop =test')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)

        text = '--step2.修改参数默认值为9999999999--;expect:合理报错--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              error_msg2,
                                              'enable_nestloop = 9999999999')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)

    def tearDown(self):
        self.log.info('--无需清理环境--')
        self.log.info('Opengauss_Function_Guc_Parameter_Case1262结束')
