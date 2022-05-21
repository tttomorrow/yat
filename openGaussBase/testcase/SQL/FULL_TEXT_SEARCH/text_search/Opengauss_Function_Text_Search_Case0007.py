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
'''
#--  @testpoint:ts_rank_cd函数测试
'''

import unittest
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Hostname(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_Function_Text_Search_Case0007开始执行--------------------------")

    # 排序文件查询使用覆盖密度
    def test_directoary_1(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''SELECT ts_rank_cd('hello world'::tsvector, 'world'::tsquery);''')
        logger.info(SqlMdg)
        self.assertTrue('ts_rank_cd >= 0', SqlMdg)

        # 创建schema
        SqlMdg = commonsh.execut_db_sql('''DROP SCHEMA IF EXISTS tsearch CASCADE;
                                     CREATE SCHEMA tsearch;''')
        logger.info(SqlMdg)
        self.assertIn('CREATE SCHEMA', SqlMdg)

       # 创建表
        SqlMdg = commonsh.execut_db_sql('''DROP TABLE if exists tsearch.pgweb;
                                    CREATE TABLE tsearch.pgweb(id int, body text, title text, last_mod_date date);''')
        logger.info(SqlMdg)
        self.assertIn('CREATE TABLE', SqlMdg)

       # 插入数据
        SqlMdg = commonsh.execut_db_sql('''INSERT INTO tsearch.pgweb VALUES(1, 'China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.', 'China', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(2, 'America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley.', 'America', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(3, 'England is a country that is part of the United Kingdom. It shares land borders with Scotland to the north and Wales to the west.', 'England', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(4, 'Australia, officially the Commonwealth of Australia, is a country comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands.', 'Australia', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(5, 'Russia, also officially known as the Russian Federation, is a sovereign state in northern Eurasia.', 'Russia', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(6, 'Japan is an island country in East Asia.', 'Japan', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(7, 'Germany, officially the Federal Republic of Germany, is a sovereign state and federal parliamentary republic in central-western Europe.', 'Germany', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(8, 'France, is a sovereign state comprising territory in western Europe and several overseas regions and territories.', 'France', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(9, 'Italy officially the Italian Republic, is a unitary parliamentary republic in Europe.', 'Italy', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(10, 'India, officially the Republic of India, is a country in South Asia.', 'India', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(11, 'Brazil, officially the Federative Republic of Brazil, is the largest country in both South America and Latin America.', 'Brazil', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(12, 'Canada is a country in the northern half of North America.', 'Canada', '2010-1-1');
                                     INSERT INTO tsearch.pgweb VALUES(13, 'Mexico, officially the United Mexican States, is a federal republic in the southern part of North America.', 'Mexico', '2010-1-1');
                                     ''')
        logger.info(SqlMdg)
        self.assertIn('INSERT', SqlMdg)

        # 从body列检索字串为'america'查询排名前十的覆盖密度
        SqlMdg = commonsh.execut_db_sql('''SELECT id, title, ts_rank_cd(to_tsvector(body), query) AS rank FROM tsearch.pgweb, to_tsquery('america') query WHERE query @@ to_tsvector(body) ORDER BY rank DESC LIMIT 10;''')
        logger.info(SqlMdg)
        self.assertTrue('ts_rank_cd >= 0', SqlMdg)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        SqlMdg = commonsh.execut_db_sql('''DROP TABLE tsearch.pgweb cascade;''')
        logger.info(SqlMdg)
        self.assertIn('DROP TABLE', SqlMdg)

        # 删除schema
        SqlMdg = commonsh.execut_db_sql('''DROP SCHEMA tsearch cascade;''')
        logger.info(SqlMdg)
        self.assertIn('DROP SCHEMA', SqlMdg)
        logger.info('------------------------Opengauss_Function_Text_Search_Case0007执行结束--------------------------')
