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
Case Type   : 全文检索
Case Name   : 修改对应的词典定义文件参数，词典定义文件不存在，合理报错
Description :
    1.创建词典
    2.修改词典定义文件
    3.删除词典
Expect      :
    1.词典创建成功
    2.合理报错
    3.删除成功
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0041开始执行--------------------------")

    def test_dictionary(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop text search dictionary if exists thesaurus_astro cascade;
                                        create text search dictionary thesaurus_astro (
                                        template = thesaurus,
                                        dictfile =  thesaurus_sample,
                                        dictionary = pg_catalog.english_stem);''')
        logger.info(sql_cmd1)
        self.assertIn('NOTICE:  text search dictionary "thesaurus_astro" does not exist, skipping', sql_cmd1)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''ALTER TEXT SEARCH DICTIONARY thesaurus_astro (DictFile = thesaurus_sample1);''')
        logger.info(sql_cmd2)
        self.assertIn('ERROR', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop text search dictionary if exists thesaurus_astro cascade;''')
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0041执行结束--------------------------')
