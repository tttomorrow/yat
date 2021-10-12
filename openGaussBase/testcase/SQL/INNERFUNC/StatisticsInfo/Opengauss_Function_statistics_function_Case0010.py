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
Case Name   : get_instr_wait_event(NULL)，描述：获取当前节点event等待的统计信息
Description : 获取当前节点event等待的统计信息
Expect      : 获取当前节点event等待的统计信息成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0010开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('-步骤1.get_instr_wait_event(NULL)，获取当前节点event等待的统计信息-')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select get_instr_wait_event(NULL) limit 3;')
        self.log.info(sql_cmd)
        number = len(sql_cmd.splitlines())
        self.log.info(number)
        if number >= 3:
            list1 = sql_cmd.split('\n')[-2]
            self.log.info(list1)
            list2 = len(list1.split(','))
            self.log.info(list2)
            if list2 == 10:
                self.log.info('汇聚各节点GUC参数配置信息成功')
            else:
                raise Exception('函数执行异常，请检查')
        else:
            raise Exception('执行结果异常，请检查')

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0010结束')
