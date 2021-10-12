"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : GUC
Case Name   : 修改参数uncontrolled_memory_context，观察预期结果
Description :
        1、查询uncontrolled_memory_context默认值；
           show uncontrolled_memory_context;
           仅适用于DEBUG版本，故只查看默认值，
        该参数受enable_memory_context_control影响，改参数也只能在DEBUG版本验证
Expect      :
        1、显示默认值为空，但是会在参数值的最前面添加标题含义字符串
        “MemoryContext white list:"。；
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_Resource_Case00021.py start-----')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_startdb(self):
        self.log.info('查询该参数默认值')
        sql_cmd = self.commonsh.execut_db_sql('''show 
            uncontrolled_memory_context;''')
        self.log.info(sql_cmd)
        self.assertIn('MemoryContext white list', sql_cmd)

    def tearDown(self):
        self.log.info('------无须清理环境-----------')
        self.log.info(
            '----Opengauss_Function_Guc_Resource_Case0021.py执行完成---')
