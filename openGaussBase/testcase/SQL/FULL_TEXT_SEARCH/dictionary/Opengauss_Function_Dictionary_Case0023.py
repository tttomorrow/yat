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
Case Name   : 创建Thesaurus词典，词典定义文件内容测试(省略冒号)
Description :
    1.创建词典文件并写入内容,省略中间冒号作为短语和其替换词间的分隔符
    2.创建词典
Expect      :
    1.创建成功
    2.合理报错
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
            '--Opengauss_Function_Dictionary_Case0023开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.user_node = Node('dbuser')
        self.constant = Constant()
        self.FILE_NAME = "test_data.ths"
        self.FILE_PATH = os.path.join(macro.DB_INSTANCE_PATH, self.FILE_NAME)

    def test_user_permission(self):
        # 创建文件并写入内容，省略中间冒号作为短语和其替换词间的分隔符
        excute_cmd = f'echo "supernovae stars sn" > {self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg1)
        # 查看
        excute_cmd = f'cat { self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertIn('supernovae stars sn', msg1)
        # 创建词典，合理报错
        sql_cmd = commonsh.execut_db_sql(f'''
    drop text search dictionary if exists thesaurus_astro  cascade;
    create text search dictionary thesaurus_astro (
    TEMPLATE = thesaurus,
    DICTFILE = test_data,
    DICTIONARY = pg_catalog.english_stem,
    FILEPATH = 'file://{self.DB_INSTANCE_PATH}');''')
        logger.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        excute_cmd = f'rm { self.FILE_PATH}';
        logger.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Dictionary_Case0023执行结束---')





