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
Case Type   : 内建函数
Case Name   : HLL函数和操作符
Description :
    1.hll_hash_bytea(bytea),对bytea类型数据计算哈希值
    2.hll_hash_bytea(bytea, int32),对bytea类型数据计算哈希值，并设置hashseed（即改变哈希策略）
    3.hll_hash_bytea(bytea, int32),入参2为其他类型时
Expect      :
    1.hll_hash_bytea(bytea),对bytea类型数据计算哈希值成功
    2.hll_hash_bytea(bytea, int32),对bytea类型数据计算哈希值，并设置hashseed（即改变哈希策略）成功
    3.hll_hash_bytea(bytea, int32),入参2为其他类型时合理报错
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Hll_Case0020开始执行-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        self.log.info('---步骤1.hll_hash_bytea(bytea),对bytea类型数据计算哈希值---')
        sql_cmd = self.commonsh.execut_db_sql(f'select hll_hash_bytea'
                                              f'(e\'\\x\');'
                                              f'select hll_hash_bytea'
                                              f'(e\'\\xdeadbeef\');')
        self.log.info(sql_cmd)

        self.log.info('---步骤2.hll_hash_bytea(bytea, int32),对bytea类型数据计算哈希值，'
                 '并设置hashseed（即改变哈希策略）---')
        sql_cmd = self.commonsh.execut_db_sql(f'select hll_hash_bytea'
                                              f'select hll_hash_bytea'
                                              f'(e\'\\xdeadbeef\', 0);')
        self.log.info(sql_cmd)

        self.log.info('---hll_hash_bytea(bytea, int32),入参2为其他类型时,合理报错---')
        sql_cmd = self.commonsh.execut_db_sql(f'select hll_hash_bytea'
                                              f'select hll_hash_bytea'
                                              f'(e\'\\xdeadbeef\', -1);')
        self.log.info(sql_cmd)
        self.assertIn('ERROR:  function hll_hash_bytea(unknown, bigint)'
                      ' does not exist', sql_cmd)

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Innerfunc_Hll_Case0020结束-')
