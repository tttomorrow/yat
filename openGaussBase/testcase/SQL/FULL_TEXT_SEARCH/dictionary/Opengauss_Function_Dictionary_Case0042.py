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
Case Name   : 仅修改词典FILEPATH参数不修改对应的词典定义文件参数，合理报错
Description :
    1.创建THESAURUS_astro.ths文件并定义了短语
     词典定义文件名由大写字母，下划线组成
    2.创建词典
    3.仅修改FILEPATH参数不修改对应的词典定义文件参数
    4.清理环境
Expect      :
    1.创建成功
    2.词典创建成功
    3.合理报错
    4.清理环境完成
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
constant = Constant()


class Dictionary(unittest.TestCase):

    def setUp(self):
        logger.info(
            '--Opengauss_Function_Dictionary_Case0042开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.user_node = Node('dbuser')
        self.FILE_NAME = "thesaurus_astro42.ths"
        self.FILE_PATH = os.path.join(macro.DB_INSTANCE_PATH, self.FILE_NAME)

    def test_user_permission(self):
        # 创建thesaurus_astro.ths文件并定义了短语及其同义词
        excute_cmd = f'echo "supernovae stars : sn" > {self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertNotIn(constant.SQL_WRONG_MSG[1], msg1)
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
    DictFile = thesaurus_astro42,
    Dictionary = pg_catalog.english_stem,
    FILEPATH = 'file://{self.DB_INSTANCE_PATH}');
    select dictname,dictinitoption from PG_TS_DICT where 
    dictname='thesaurus_astro';''')
        logger.info(sql_cmd)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd)
        self.assertIn('thesaurus_astro', sql_cmd)
        # 修改词典FILEPATH参数,合理报错
        sql_cmd = commonsh.execut_db_sql(f'''
       alter text search dictionary thesaurus_astro 
(FILEPATH = 'file:/home');''')
        logger.info(sql_cmd)
        self.assertIn(
            'ERROR:  FilePath parameter should be with DictFile', sql_cmd)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        excute_cmd = f'rm {self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        sql_cmd = commonsh.execut_db_sql('''
          drop text search dictionary if exists thesaurus_astro cascade;''')
        logger.info(sql_cmd)
        logger.info(
            '----Opengauss_Function_Dictionary_Case0042执行结束---')
