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
#--  @testpoint:删除词典，权限测试（sysadmin用户）
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0049开始执行--------------------------")

    # 创建词典,词典定义文件全名为thesaurus_sample.ths, FILEPATH使用本地目录（/Datadir/cluster/app/share/postgresql/tsearch_data）
    def test_directoary_1(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY if exists thesaurus_astro cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)

        SqlMdg = commonsh.execut_db_sql(f'''CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
                                 TEMPLATE = thesaurus,
                                 DictFile = thesaurus_sample,
                                 Dictionary = pg_catalog.english_stem,
                                 FILEPATH = 'file:{file_path}');''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, SqlMdg)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除词典
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY thesaurus_astro cascade;''')
        logger.info(SqlMdg)
        self.assertIn(constant.DROP_DICTIONARY_SUCCESS_MSG, SqlMdg)
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0049执行结束--------------------------')
