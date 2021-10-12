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
Case Name   : pg_control_group_config描述：在当前节点上打印cgroup配置
Description : 在当前节点上打印cgroup配置
Expect      : 在当前节点上打印cgroup配置成功
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0027开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----在当前节点上打印cgroup配置-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_control_group_config();')
        self.log.info(sql_cmd)
        self.assertIn('There is no Cgroup configuration '
                      'information for without initialization', sql_cmd)

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0027结束')
