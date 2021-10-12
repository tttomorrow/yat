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
#--  @testpoint:修改词典定义语法测试
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0040开始执行--------------------------")

    # 创建snowball词典
    def test_directoary_1(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY if exists snowball_test cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)

        SqlMdg = commonsh.execut_db_sql(f'''CREATE TEXT SEARCH DICTIONARY snowball_test (
                                      TEMPLATE = snowball,
                                      LANGUAGE = 'english',
                                      STOPWORDS = english);''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, SqlMdg)
        # 更新词典定义，不实际更改任何内容
        SqlMdg = commonsh.execut_db_sql('''ALTER TEXT SEARCH DICTIONARY snowball_test ( dummy );''')
        logger.info(SqlMdg)
        self.assertIn('ALTER TEXT SEARCH DICTIONARY', SqlMdg)

        # 查询词典信息(和创建词典的信息一致)
        SqlMdg = commonsh.execut_db_sql('''select dictname,dictinitoption FROM pg_ts_dict WHERE dictname ='snowball_test';''')
        logger.info(SqlMdg)
        self.assertIn('snowball_test', SqlMdg)

       # 删除词典
    def tearDown(self):
        logger.info('----------this is teardown-------')
        SqlMdg = commonsh.execut_db_sql(''' drop TEXT SEARCH DICTIONARY snowball_test cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0040执行结束--------------------------')
