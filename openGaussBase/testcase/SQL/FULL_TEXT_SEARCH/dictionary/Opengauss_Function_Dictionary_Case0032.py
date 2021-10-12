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
Case Name   : 创建Thesaurus词典，词典定义文件名测试
Description :
    1.创建thesaurus1_astro.ths文件并定义短语
    词典定义文件名由小写字母，数字和下划线组成
    2.创建词典
    3.清理环境
Expect      :
    1.创建成功
    2.创建词典成功
    3.清理环境完成
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
            '--Opengauss_Function_Dictionary_Case0032开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.user_node = Node('dbuser')
        self.constant = Constant()
        self.FILE_NAME = "thesaurus1_astro.ths"
        self.FILE_PATH = os.path.join(macro.DB_INSTANCE_PATH, self.FILE_NAME)

    def test_user_permission(self):
        # 创建thesaurus_astro.ths文件并定义了短语及其同义词
        excute_cmd = f'echo "supernovae stars : sn" > {self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg1)
        # 查看
        excute_cmd = f'cat { self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertIn('supernovae stars : sn', msg1)
        # 创建词典
        sql_cmd = commonsh.execut_db_sql(f'''
    drop text search dictionary if exists thesaurus_astro cascade;
    create text search dictionary thesaurus_astro (
    TEMPLATE = thesaurus,
    DICTFILE = thesaurus1_astro,
    Dictionary = pg_catalog.english_stem,
    FILEPATH = 'file://{self.DB_INSTANCE_PATH}');''')
        logger.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd)

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
            '----Opengauss_Function_Dictionary_Case0032执行结束---')





