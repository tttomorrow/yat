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
Case Name   : 文本搜索配置token_type测试，（解析器为pg_catalog.ngram）不支持的编码，合理报错
Description :
        1.创建文本搜索配置，解析器为pg_catalog.ngram
        2.创建simple字典
        3.增加文本搜索配置字串类型映射，token为grapsymbol
        4.使用文本检索函数对所创建的词典配置english2进行测试
        5.删除文本搜索配置；删除词典
Expect      :
        1.创建成功
        2.创建成功
        3.增加文本搜索配置字串类型映射成功
        4.合理报错
        5.删除成功
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
        logger.info('------------------------Opengauss_Function_Text_Search_Configuration_Case0070开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.Constant = Constant()

    def test_ngram_parser(self):

       logger.info('------------创建文本搜索配置和词典-------------------')
       sql_cmd1 = commonsh.execut_db_sql('''DROP TEXT SEARCH CONFIGURATION if exists english2 cascade;
                                          CREATE TEXT SEARCH CONFIGURATION english2 (parser=ngram);
                                           DROP TEXT SEARCH DICTIONARY IF EXISTS pg_dict cascade;
                                           CREATE TEXT SEARCH DICTIONARY pg_dict (TEMPLATE = Simple);''')
       logger.info(sql_cmd1)
       self.assertIn(self.Constant.CREATE_TEXT_SEARCH_CONFIGURATION, sql_cmd1)
       self.assertIn(self.Constant. CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd1)
       logger.info('--------------------增加文本搜索配置字串类型映射，token为grapsymbol ---------')
       sql_cmd2 = commonsh.execut_db_sql('''ALTER TEXT SEARCH CONFIGURATION english2 ADD MAPPING FOR  grapsymbol WITH pg_dict;''')
       logger.info(sql_cmd2)
       self.assertIn(self.Constant.ALTER_TEXT_SEARCH_CONFIGURATION, sql_cmd2)
       logger.info('-----------使用文本检索函数对所创建的词典配置english2进行测试---------')
       sql_cmd3 = commonsh.execut_db_sql('''SELECT ts_debug('ngram','●');''')
       logger.info(sql_cmd3)
       self.assertIn('ERROR:  ngram parser only support UTF8/GBK encoding', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''DROP TEXT SEARCH CONFIGURATION english2 cascade;
                                           DROP TEXT SEARCH DICTIONARY pg_dict cascade;''')
        logger.info(sql_cmd4)
        logger.info('-----------------------Opengauss_Function_Text_Search_Configuration_Case0070执行结束--------------------------')





