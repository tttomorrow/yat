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
Case Name   : 函数ts_parse测试（无效性测试），合理报错
Description :
        1.省略解析器名字
        2.解析器名字为ngram
        3.数据库编码为SQL_ASCII，解析器为pound，解析中文
        4.查看default解析器的oid
        5.ts_parse函数指定错误parser_oid
        6.查看pound解析器的oid
        7.ts_parse函数指定错误parser_oid
Expect      :
        1.合理报错
        2.合理报错
        3.合理报错
        4.default解析器的oid为3722
        5.合理报错
        6.pound解析器的oid为3801
        7.合理报错
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
        logger.info('------------------------Opengauss_Function_Text_Search_Case0021开始执行-----------------------------')
        self.userNode = Node('dbuser')

    def test_ngram_parser(self):
        # 省略解析器名字，合理报错
        sql_cmd1 = commonsh.execut_db_sql('''SSELECT * FROM ts_parse('123 - a number');
                                           SELECT * FROM ts_parse('ngram','123 - a number');
                                          SELECT * FROM ts_parse('pound', '中文检索');''')
        logger.info(sql_cmd1)
        self.assertIn('ERROR', sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''select oid from PG_TS_PARSER where prsname = 'default';
                                           SELECT ts_parse(3721, 'foo - bar');
                                           select oid from PG_TS_PARSER where prsname = 'pound';
                                           SELECT ts_parse(3802, 'foo - bar');''')
        logger.info(sql_cmd2)
        self.assertIn('3722', sql_cmd2)
        self.assertIn('ERROR', sql_cmd2)
        self.assertIn('3801', sql_cmd2)

    # 清理环境no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_Text_Search_Case0021执行结束--------------------------')





