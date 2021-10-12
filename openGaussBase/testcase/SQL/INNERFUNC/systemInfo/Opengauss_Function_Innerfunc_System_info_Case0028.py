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
Case Type   : 系统信息函数-模式可见性查询函数 
Case Name   : 使用函数pg_get_serial_sequence()，获取对应表名和列名上的序列
Description :
    1.创建表
    2.创建与表关联的序列
    3.使用函数pg_get_serial_sequence()，获取对应表名和列名上的序列
    4.删除序列
Expect      :
    1.创建表
    2.创建与表关联的序列
    3.使用函数pg_get_serial_sequence()，获取对应表名和列名上的序列
    4.删除序列
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0028开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'----------步骤1.创建表----------')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop table if exists test_sequences;'
            f'create table test_sequences (id int, name char(10));')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)

        LOG.info(f'----------步骤2.创建序列----------')
        sql_cmd = self.commonsh.execut_db_sql(
            f'create sequence serial1  '
            f'start 101 cache 20 owned by test_sequences.id;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_SEQUENCE_SUCCESS_MSG, sql_cmd)

        LOG.info(f'-步骤3.使用函数pg_get_serial_sequence()，获取对应表名和列名上的序列-')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_get_serial_sequence(\'test_sequences\', \'id\');')
        LOG.info(sql_cmd)
        self.assertIn('public.serial1', sql_cmd)

        LOG.info(f'----------步骤4.清理环境----------')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop sequence serial1;  '
            f'drop table test_sequences ')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.DROP_SEQUENCE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)

    def tearDown(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0028结束-')
