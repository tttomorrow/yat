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
Case Name   : total_memory()描述：获取当前节点使用的虚拟内存大小，单位KB。
Description :
    1.获取主节点节点使用的虚拟内存大小
    1.获取备节点节点使用的虚拟内存大小
Expect      :
    1.获取主节点使用的虚拟内存大小成功
    1.获取备节点使用的虚拟内存大小成功
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
        self.log.info('Opengauss_Function_statistics_function_Case0073开始')
        self.commonsh1 = CommonSH('Standby1DbUser')

    def test_built_in_func(self):
        self.log.info('-----步骤1.获取当前节点使用的虚拟内存大小（主节点）-----')
        sql_cmd = Primary_SH.execut_db_sql(
            f'select total_memory();')
        self.log.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        str_info = sql_cmd.split('\n')[2]
        self.log.info(str_info)
        num = len(str_info.split(','))
        self.log.info(f'num = {num}')
        if num == 1:
            self.log.info('获取当前节点使用的虚拟内存大小成功')
        else:
            raise Exception('函数执行异常，请检查')

        self.log.info('-----步骤2.获取当前节点使用的虚拟内存大小（备节点）-----')
        sql_cmd = self.commonsh1.execut_db_sql(
            f'select total_memory();')
        self.log.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        str_info = sql_cmd.split('\n')[2]
        self.log.info(str_info)
        num = len(str_info.split(','))
        self.log.info(f'num = {num}')
        if num == 1:
            self.log.info('获取当前节点使用的虚拟内存大小成功')
        else:
            raise Exception('函数执行异常，请检查')

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0073结束')
