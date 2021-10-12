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
Case Type   : 统计信息函数
Case Name   : total_cpu()描述：获取当前节点使用的CPU时间，单位是jiffies。
Description :
    1.获取主节点使用的CPU时间
    2.获取备节点使用的CPU时间
Expect      :
    1.获取主节点使用的CPU时间成功
    2.获取备节点使用的CPU时间成功
History     :
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0072开始')
        self.commonsh1 = CommonSH('Standby1DbUser')

    def test_built_in_func(self):
        self.log.info('-----步骤1.获取当前节点使用的CPU时间（主节点）-----')
        sql_cmd = Primary_SH.execut_db_sql(
            f'select total_cpu();')
        self.log.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)

        self.log.info('-----步骤2.获取当前节点使用的CPU时间（备节点）-----')
        sql_cmd = self.commonsh1.execut_db_sql(
            f'select total_cpu();')
        self.log.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0072结束')
