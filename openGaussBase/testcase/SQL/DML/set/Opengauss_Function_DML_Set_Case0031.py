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
'''
--  @date:2020/11/11
--  @testpoint:设置无效的字符编码集，合理报错
'''
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0031开始执行-----------------------------')

    def test_set(self):
       # 设置客户端编码分别为SQL_ASCII1和UTF9，合理报错
        sql_cmd1 = commonsh.execut_db_sql('''set names 'SQL_ASCII1';
                                      set  names 'UTF9';
                                      set  names 'GBK*&^\$#@#%^^';
                                      show client_encoding;
                                      set  names '(UTF8)';
                                      show client_encoding;''')
        logger.info(sql_cmd1)
        self.assertIn('ERROR:  invalid value for parameter "client_encoding"', sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('GBK', sql_cmd1)
        self.assertIn('UTF8', sql_cmd1)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0031执行结束--------------------------')
