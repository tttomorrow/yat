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
Case Name   : 创建Thesaurus词典,词典文件定义的sample words中，
              用$号替代停用词位置
Description :
    1.创建test_data29.ths文件并定义了短语及其同义词
    2.创建词典
    3.创建文本搜索配置
    4.创建词典后，将其绑定到对应文本搜索配置中需要处理的token类型上
    5.使用词典测试,SELECT plainto_tsquery('russian','a one the two');
    SELECT plainto_tsquery('russian','fats');
    6.清理环境
Expect      :
    1.创建成功
    2.创建词典成功
    3.创建文本搜索配置成功
    4.增加映射成功
    5.显示 'one' & 'two';
      显示'fat'
    6.清理环境完成
History     :
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


class Dictionary(unittest.TestCase):

    def setUp(self):
        logger.info(
            '--Opengauss_Function_Dictionary_Case0029开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.user_node = Node('dbuser')
        self.constant = Constant()
        self.FILE_NAME = "test_data29.ths"
        self.FILE_PATH = os.path.join(macro.DB_INSTANCE_PATH, self.FILE_NAME)

    def test_user_permission(self):
        # 创建thesaurus_astro.ths文件并定义了短语及其同义词
        excute_cmd = f'echo "\$ one \$ two : swsw" > {self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg1)
        # 查看
        excute_cmd = f'cat { self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertIn('$ one $ two : swsw', msg1)
        # 创建词典
        sql_cmd = commonsh.execut_db_sql(f'''
    drop text search dictionary if exists thesaurus_astro cascade;
    create text search dictionary thesaurus_astro (
    TEMPLATE = thesaurus,
    DICTFILE = test_data29,
    Dictionary = pg_catalog.english_stem,
    FILEPATH = 'file://{self.DB_INSTANCE_PATH}');''')
        logger.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd)
        # 创建文本搜索配置
        sql_cmd = commonsh.execut_db_sql('''
drop text search configuration if exists russian cascade;
create text search configuration russian (parser =pg_catalog.default);''')
        logger.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TEXT_SEARCH_CONFIGURATION, sql_cmd)
        # 创建词典后，将其绑定到对应文本搜索配置中需要处理的token类型上
        sql_cmd = commonsh.execut_db_sql('''
    alter text search configuration russian
    alter mapping for asciiword, asciihword, hword_asciipart
    with thesaurus_astro, english_stem;''')
        logger.info(sql_cmd)
        self.assertIn(self.constant.ALTER_TEXT_SEARCH_CONFIGURATION, sql_cmd)
        # 使用词典，测试,同义词不生效
        sql_cmd = commonsh.execut_db_sql(
        "SELECT plainto_tsquery('russian','a one the two');"
        "SELECT plainto_tsquery('russian','fats');")
        logger.info(sql_cmd)
        self.assertIn("'one' & 'two'", sql_cmd)
        self.assertIn("'fat'", sql_cmd)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd = commonsh.execut_db_sql('''
      drop TEXT SEARCH DICTIONARY thesaurus_astro cascade;''')
        logger.info(sql_cmd)
        excute_cmd = f'rm { self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Dictionary_Case0029执行结束---')





