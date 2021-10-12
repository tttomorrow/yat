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
Case Type   :全文检索--解析器
Case Name   : 函数ts_debug结合ngram解析器测试（无效性测试），合理报错
Description :
        1.数据库编码为SQL_ASCII，ts_debug函数指定解析ngram
Expect      :
        1.合理报错
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Parser(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Text_Search_Case0019开始执行-----------------------------')
        self.userNode = Node('dbuser')

    def test_ngram_parser(self):
        # 数据库编码为SQL_ASCII，ts_debug函数指定解析ngram，合理报错
        sql_cmd1 = commonsh.execut_db_sql('''SELECT ts_debug('ngram', 'The Brightest supernovaes');
                                           SELECT ts_debug('ngram', '中文检索');
                                           SELECT ts_debug('pound', '中文检索');''')
        logger.info(sql_cmd1)
        self.assertIn('ERROR:  ngram parser only support UTF8/GBK encoding', sql_cmd1)

    # 清理环境no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_Text_Search_Case0019执行结束--------------------------')





