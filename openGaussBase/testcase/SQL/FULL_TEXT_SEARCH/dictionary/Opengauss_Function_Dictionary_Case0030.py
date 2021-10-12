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
#--  @date:2020/9/17
#--  @testpoint:创建并使用Ispell词典
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0030开始执行--------------------------")

    # 创建Ispell词典, FILEPATH使用本地目录（/Datadir/cluster/app/share/postgresql/tsearch_data）
    def test_directoary_1(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY if exists ispell_test cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)

        SqlMdg = commonsh.execut_db_sql(f'''CREATE TEXT SEARCH DICTIONARY ispell_test (
                                      TEMPLATE = ispell,
                                      DictFile = ispell_sample,
                                      AffFile = ispell_sample,
                                      FILEPATH = 'file:{file_path}');''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, SqlMdg)
        # 删除文本搜索配置
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH CONFIGURATION if exists ts_conf cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_TEXT_SEARCH_CONFIGURATION, SqlMdg)
       # 创建文本搜索配置
        SqlMdg = commonsh.execut_db_sql('''CREATE TEXT SEARCH CONFIGURATION ts_conf (parser =pg_catalog.default);''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_TEXT_SEARCH_CONFIGURATION, SqlMdg)
        # 修改文本搜索配置字串类型
        SqlMdg = commonsh.execut_db_sql('''ALTER TEXT SEARCH CONFIGURATION ts_conf ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,word, hword, hword_part WITH ispell_test;''')
        logger.info(SqlMdg)
        self.assertIn(constant.ALTER_TEXT_SEARCH_CONFIGURATION, SqlMdg)

        # 使用词典
        SqlMdg = commonsh.execut_db_sql('''SELECT * FROM ts_debug('ts_conf', 'PostgreSQL');''')
        logger.info(SqlMdg)
        self.assertIn('asciiword ', SqlMdg )

       # 删除词典
    def tearDown(self):
        logger.info('----------this is teardown-------')
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY ispell_test cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0030执行结束--------------------------')
