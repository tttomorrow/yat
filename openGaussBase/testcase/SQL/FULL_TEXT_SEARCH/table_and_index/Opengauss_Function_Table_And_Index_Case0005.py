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
Case Type   :全文检索--解析器
Case Name   : :索引使用约束测试，不支持编码，合理报错
Description :
        1.创建行存表和gin索引
        2.创建文本搜索配置
        3.设置文本搜索配置
        4.查询
        5.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.设置文本搜索配置
        4.合理报错，ASCII编码不支持中文检索
        5.清理完成
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
        logger.info('------------------------Opengauss_Function_Table_And_Index_Case0005开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.Constant = Constant()

    def test_ngram_parser(self):
       logger.info('---------------创建行存表和索引---------------')
       sql_cmd1 = commonsh.execut_db_sql('''drop table if exists table1;
                                          create table table1 (c_int int,c_bigint bigint,c_varchar varchar,c_text text) with(orientation=row);
                                          drop index if exists idx1;
                                          create index idx1 on table1 using gin(to_tsvector(c_text));''')
       logger.info(sql_cmd1)
       self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
       logger.info('-------------创建文本搜索配置，解析器为pound-----------------')
       sql_cmd2 = commonsh.execut_db_sql('''drop text search configuration if exists ts_conf_1;
                                          create text search configuration ts_conf_1(parser=POUND);
                                          drop text search configuration if exists ts_conf_2;
                                          create text search configuration ts_conf_2(parser=POUND) with(split_flag='%');''')
       logger.info(sql_cmd2)
       self.assertIn(self.Constant.CREATE_TEXT_SEARCH_CONFIGURATION, sql_cmd2)
       logger.info('-------------设置文本搜索配置后查询---------------')
       sql_cmd3 = commonsh.execut_db_sql('''set default_text_search_config='ts_conf_2';
       select c_varchar,to_tsvector(c_varchar) from table1 where to_tsvector(c_text) @@ plainto_tsquery('￥#@……&**') 
       and to_tsvector(c_text) @@ plainto_tsquery('some company')   and c_varchar is not null order by 1 desc limit 3;''')
       logger.info(sql_cmd3)
       self.assertIn('ERROR:  Chinese is not supported by ASCII!', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop TABLE table1 cascade;
                                           drop text search configuration ts_conf_1;
                                           drop text search configuration ts_conf_2;
                                           reset default_text_search_config;
                                           show default_text_search_config;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_Table_And_Index_Case0005执行结束--------------------------')





