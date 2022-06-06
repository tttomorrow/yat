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
Case Name   : get_node_stat_reset_time()描述：获取当前节点的统计信息重置时间。
Description :
    1.获取当前节点的统计信息重置时间
Expect      :
    1.获取当前节点的统计信息重置时间成功
History     :
"""
import time
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0070开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----步骤1.获取当前节点的统计信息重置时间-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select get_node_stat_reset_time();')
        self.log.info(sql_cmd)
        number = len(sql_cmd.splitlines())
        self.log.info(number)
        if number >= 3:
            str_info = sql_cmd.split('\n')[-2]
            self.log.info(str_info)
            list2 = str_info.split('.')[0]
            self.log.info(list2)

            self.log.info('-----步骤2.重置数据库之后再次获取时间-----')
            time.sleep(60)
            sql_cmd = self.commonsh.execut_db_sql(
                f'create database yat1;'
                f'drop database yat1;'
                f'select get_node_stat_reset_time();')
            self.log.info(sql_cmd)
            list3 = sql_cmd.split('\n')[-2]
            self.log.info(list3)
            list4 = list3.split('.')[0]
            self.log.info(list4)
            self.assertNotEqual(list2, list4)
        else:
            raise Exception('函数执行异常，请检查')

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0070结束')
