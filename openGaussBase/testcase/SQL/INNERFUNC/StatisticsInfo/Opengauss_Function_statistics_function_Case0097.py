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
Case Type   : 统计信息函数
Case Name   : get_instr_rt_percentile()描述：获取数据库SQL响应时间P80,P95分布信息
Description : 获取数据库SQL响应时间P80,P95分布信息
Expect      : 获取数据库SQL响应时间P80,P95分布信息成功
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0097开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        text = '--step1:获取数据库SQL响应时间P80,P95分布信息;expect:执行成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select get_instr_rt_percentile(1);')
        self.log.info(sql_cmd)
        str1 = sql_cmd.split('\n')[-2]
        self.log.info(f'str1 = {str1}')
        num = len(str1.split(','))
        self.log.info(f'list1 = {num}')
        self.assertEqual(num, 2, '执行失败:' + text)

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0097结束')
