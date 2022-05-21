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
Case Name   : 修改词典所属模式,模式不存在，合理报错
Description :
    1.创建词典
    2.查询test_myschema模式信息
    3.修改词典为不存在的模式
    4.查看词典模式
    5.删除词典
Expect      :
    1.创建词典成功
    2.无数据显示
    3.合理报错
    4.模式仍是在public
    5.删除词典成功
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0046开始执行--------------------------")

    def test_dictionary(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY if exists thesaurus_astro cascade;
        CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
        TEMPLATE = thesaurus,
        DictFile = thesaurus_sample,
        Dictionary = pg_catalog.english_stem);''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, SqlMdg)
        SqlMdg = commonsh.execut_db_sql('''drop schema if exists test_myschema;
       ''')
        logger.info(SqlMdg)
        self.assertIn('NOTICE:  schema "test_myschema" does not exist, skipping', SqlMdg )
        SqlMdg = commonsh.execut_db_sql('''ALTER TEXT SEARCH DICTIONARY thesaurus_astro SET SCHEMA test_myschema;''')
        logger.info(SqlMdg)
        self.assertIn('ERROR:  schema "test_myschema" does not exist', SqlMdg)
        SqlMdg = commonsh.execut_db_sql('''\\dFd+ thesaurus_astro''')
        logger.info(SqlMdg)
        self.assertIn('public', SqlMdg)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY  thesaurus_astro cascade;''')
        logger.info(SqlMdg)
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0046执行结束--------------------------')
