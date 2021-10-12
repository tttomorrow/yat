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
#--  @testpoint:创建并使用Ispell词典,对复合词拆分
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0031开始执行--------------------------")

    # 创建Ispell词典, FILEPATH使用本地目录（/Datadir/cluster/app/share/postgresql/tsearch_data）,词典定义文件全名为ispell_sample.dict，词缀文件全名为ispell_sample.affix
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
        # 使用Ispell词典进行复合词拆分
        SqlMdg = commonsh.execut_db_sql('''SELECT ts_lexize('ispell_test', 'footballklubber');''')
        logger.info(SqlMdg)
        self.assertIn('{footballklubber,foot,ball,klubber,football,klubber}', SqlMdg)

       # 删除词典
    def tearDown(self):
        logger.info('----------this is teardown-------')
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY ispell_test cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0031执行结束--------------------------')
