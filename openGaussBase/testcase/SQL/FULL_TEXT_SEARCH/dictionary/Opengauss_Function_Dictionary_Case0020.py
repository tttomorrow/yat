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
#--  @testpoint:创建Synonym词典，添加option选项且使用词典
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0020开始执行--------------------------")

    # 创建同义词词典, FILEPATH使用本地目录（/Datadir/cluster/app/share/postgresql/tsearch_data）
    def test_directoary_1(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY if exists thesaurus_astro;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)

        SqlMdg = commonsh.execut_db_sql(f'''CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
                                      TEMPLATE = thesaurus,
                                      DictFile = thesaurus_sample,
                                      Dictionary = pg_catalog.english_stem,
                                      FILEPATH = 'file:{file_path}');''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, SqlMdg)
        #删除文本搜索配置
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH CONFIGURATION if exists russian cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_TEXT_SEARCH_CONFIGURATION, SqlMdg)
       #创建文本搜索配置
        SqlMdg = commonsh.execut_db_sql('''create TEXT SEARCH CONFIGURATION russian (parser =pg_catalog.default);''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_TEXT_SEARCH_CONFIGURATION, SqlMdg)
        #增加映射
        SqlMdg = commonsh.execut_db_sql('''ALTER TEXT SEARCH CONFIGURATION russian ALTER MAPPING FOR asciiword, asciihword, hword_asciipart WITH thesaurus_astro, english_stem;''')
        logger.info(SqlMdg)
        self.assertIn(constant.ALTER_TEXT_SEARCH_CONFIGURATION, SqlMdg)

        #使用词典
        SqlMdg = commonsh.execut_db_sql('''SELECT plainto_tsquery('russian','supernova star');''')
        logger.info(SqlMdg)
        self.assertIn("'sn'", SqlMdg )

        SqlMdg = commonsh.execut_db_sql('''SELECT to_tsvector('russian','supernova star');''')
        logger.info(SqlMdg)
        self.assertIn("'sn':1", SqlMdg)


    #删除词典
    def tearDown(self):
        logger.info('----------this is teardown-------')
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY thesaurus_astro cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0020执行结束--------------------------')
