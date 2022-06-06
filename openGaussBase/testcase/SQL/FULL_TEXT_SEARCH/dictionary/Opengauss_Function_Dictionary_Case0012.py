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
#--  @testpoint:创建Synonym词典,同义词词典的定义文件名不合理
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0012开始执行--------------------------")

    #创建词典前，先进行删除操作
    def test_directoary_1(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY if exists my_synonym cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)
        # 创建同义词词典, FILEPATH使用本地目录（/Datadir/cluster/app/share/postgresql/tsearch_data），词典文件名不合理，报错
        SqlMdg = commonsh.execut_db_sql(f'''CREATE TEXT SEARCH DICTIONARY my_synonym (
                    TEMPLATE = synonym,
                    SYNONYMS = synonym_sample.syns,
                    FILEPATH = 'file:{file_path}');''')
        logger.info(SqlMdg)
        self.assertIn('ERROR:  invalid text search configuration file name "synonym_sample.syns"', SqlMdg)

    #清理环境：no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0012执行结束--------------------------')
