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
Case Name   : 创建synonym词典，添加所有option
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
            '--Opengauss_Function_Dictionary_Case0018开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.user_node = Node('dbuser')
        self.FILE_NAME = "synonym_sample18.syn"
        self.FILE_PATH = os.path.join(macro.DB_INSTANCE_PATH, self.FILE_NAME)
        self.result = r"'index':1"

    def test_user_permission(self):
        logger.info('创建词典文件并写入内容')
        excute_cmd = f'echo "indices index*" > {self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertNotIn(constant.SQL_WRONG_MSG[1], msg1)
        logger.info('查看')
        excute_cmd = f'cat { self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertIn('indices index*', msg1)
        logger.info('创建词典')
        sql_cmd = commonsh.execut_db_sql(f'''drop text search dictionary if 
            exists syn cascade;
            create text search dictionary syn (
            TEMPLATE = synonym,
            SYNONYMS = synonym_sample18,
            FILEPATH = 'file://{self.DB_INSTANCE_PATH}');''')
        logger.info(sql_cmd)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd)
        logger.info('创建文本搜索配置并增加映射')
        sql_cmd = commonsh.execut_db_sql('''drop text search configuration if 
            exists tst;
            create text search configuration tst (copy = simple);
            alter text search configuration tst alter mapping for asciiword 
            with syn;''')
        logger.info(sql_cmd)
        self.assertIn(constant.CREATE_TEXT_SEARCH_CONFIGURATION, sql_cmd)
        self.assertIn(constant.ALTER_TEXT_SEARCH_CONFIGURATION, sql_cmd)
        logger.info('使用词典测试')
        sql_cmd = commonsh.execut_db_sql('''select 
            to_tsvector('tst','INDICES');
            select 'INDEXES are very useful'::tsvector;
            select 'INDEXES are very useful'
            ::tsvector @@ to_tsquery('tst','indices');''')
        logger.info(sql_cmd)
        self.assertIn(self.result, sql_cmd)
        self.assertIn("'INDEXES' 'are' 'useful' 'very'", sql_cmd)
        self.assertIn('f', sql_cmd)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd = f'''rm -rf {self.FILE_PATH};'''
        logger.info(sql_cmd)
        result = self.user_node.sh(sql_cmd).result()
        logger.info(result)
        sql_cmd = commonsh.execut_db_sql('''drop text search dictionary if 
            exists syn cascade;''')
        logger.info(sql_cmd)
        logger.info(
            '----Opengauss_Function_Dictionary_Case0018执行结束---')
