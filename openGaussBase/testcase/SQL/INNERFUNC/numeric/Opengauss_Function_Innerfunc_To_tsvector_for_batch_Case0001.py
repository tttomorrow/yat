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
Case Type   : 文本检索函数
Case Name   : 函数to_tsvector_for_batch(),去除文件信息，并转换为tsvector类型
Description :
    1.用to_tsvector_for_batch函数处理英文文本信息
    2.用to_tsvector_for_batch函数处理中文文本信息
Expect      :
    1.用to_tsvector_for_batch函数处理英文文本信息成功
    2.用to_tsvector_for_batch函数处理中文文本信息，合理报错
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Functions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-Opengauss_Function_Innerfunc_To_'
                 f'tsvector_for_batch_Case0001开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        self.log.info('---步骤1.用to_tsvector_for_batch函数处理英文文本信息---')
        sql_cmd = self.commonsh.execut_db_sql(f'select to_tsvector_for_'
                                              f'batch(\'english\', '
                                              f'\'The Fat Rats\');')
        self.log.info(sql_cmd)
        self.assertIn('\'fat\':2 \'rat\':3', sql_cmd)

        self.log.info('---步骤2.用to_tsvector_for_batch函数处理中文文本信息---')
        sql_cmd = self.commonsh.execut_db_sql(f'select to_tsvector_for_'
                                              f'batch(\'中文\', '
                                              f'\'你好\');')
        self.log.info(sql_cmd)
        self.assertIn('ERROR:  text search configuration "中文" does not exist',
                      sql_cmd)

    def tearDown(self):
        self.log.info('-------------------无需清理环境------------------')
        self.log.info(f'-Opengauss_Function_Innerfunc_To_'
                 f'tsvector_for_batch_Case0001结束--')
