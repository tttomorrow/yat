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
Case Name   : 创建Thesaurus词典，词典定义文件内容正确
Description :
    1.创建词典
    2.创建文本搜索配置并增加映射
    3.使用词典测试，SELECT to_tsvector('tst','INDICES');
    SELECT 'INDEXES are very useful'::tsvector;
    SELECT 'INDEXES are very useful'::tsvector @@ to_tsquery('tst','indices');
    4.删除词典
Expect      :
    1.创建词典成功
    2.创建文本搜索配置并增加映射成功
    3.显示'index':1;结果为INDICES；返回f
    4.删除成功
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Dictionary(unittest.TestCase):

    def setUp(self):
        logger.info(
            '--Opengauss_Function_Dictionary_Case0024开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.user_node = Node('dbuser')
        self.FILE_NAME = "thesaurus_sample24.ths"
        self.FILE_PATH = os.path.join(macro.DB_INSTANCE_PATH, self.FILE_NAME)

    def test_user_permission(self):
        logger.info('创建词典文件并写入内容')
        excute_cmd = f'echo "supernovae stars : *sn" > {self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertNotIn(constant.SQL_WRONG_MSG[1], msg1)
        logger.info('查看')
        excute_cmd = f'cat { self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertIn('supernovae stars : *sn', msg1)
        logger.info('创建词典')
        sql_cmd = commonsh.execut_db_sql(f'''drop text search dictionary if 
        exists thesaurus_astro cascade;
        create text search dictionary thesaurus_astro (
                    TEMPLATE = thesaurus,
                    DictFile = thesaurus_sample24,
                    Dictionary = pg_catalog.english_stem,
                    filepath = 'file://{self.DB_INSTANCE_PATH}');''')
        logger.info(sql_cmd)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd)
        logger.info('创建文本搜索配置并增加映射')
        sql_cmd = commonsh.execut_db_sql('''drop text search configuration 
        if exists russian cascade;
        create text search configuration russian (parser =pg_catalog.default);
        alter text search configuration russian alter mapping for asciiword,
        asciihword, hword_asciipart with thesaurus_astro, english_stem;
        ''')
        logger.info(sql_cmd)
        self.assertIn(constant.CREATE_TEXT_SEARCH_CONFIGURATION, sql_cmd)
        self.assertIn(constant.ALTER_TEXT_SEARCH_CONFIGURATION, sql_cmd)
        logger.info('使用词典测试')
        sql_cmd = commonsh.execut_db_sql("select plainto_tsquery"
                                         "('russian','supernova star');"
                                         "select to_tsvector"
                                         "('russian','supernova star');"
                                         "select to_tsquery"
                                         "('russian','''supernova star''');")
        logger.info(sql_cmd)
        self.assertIn(" 'sn'", sql_cmd)
        self.assertIn("'sn':1", sql_cmd)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd = f'''rm -rf {self.FILE_PATH};'''
        logger.info(sql_cmd)
        result = self.user_node.sh(sql_cmd).result()
        logger.info(result)
        sql_cmd = commonsh.execut_db_sql('''drop text search dictionary 
            thesaurus_astro cascade;''')
        logger.info(sql_cmd)
        logger.info(
            '----Opengauss_Function_Dictionary_Case0024执行结束---')
