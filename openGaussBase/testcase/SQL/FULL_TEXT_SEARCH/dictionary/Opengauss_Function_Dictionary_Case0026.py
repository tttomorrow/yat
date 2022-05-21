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
Case Type   : 全文检索
Case Name   : 创建Thesaurus词典,子词典名不存在，合理报错
Description :
    1.创建词典， Dictionary为pg_catalog.chinese_stem
Expect      :
    1.合理报错
History     :
"""
import unittest
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class FullTextSearch(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0026开始执行--------------------------")

    def test_dictionary(self):
        SqlMdg = commonsh.execut_db_sql('''drop text search dictionary if exists thesaurus_astro cascade;
                                        create text search dictionary thesaurus_astro (
                                        template = thesaurus,
                                        dictfile =  thesaurus_sample,
                                        dictionary = pg_catalog.chinese_stem);''')
        logger.info(SqlMdg)
        self.assertIn('NOTICE:  text search dictionary "thesaurus_astro" does not exist, skipping', SqlMdg)
        self.assertIn('ERROR:  text search dictionary "pg_catalog.chinese_stem" does not exist', SqlMdg)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0026执行结束--------------------------')
