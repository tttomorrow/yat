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
Case Name   : 使用不同方式查看文本搜索配置
Description :
    1.gsql的\dF命令查询分词器
    2.查看默认文本搜索配置
Expect      :
    1.显示所有的可用分词器，包括所属模式，名字以及描述
    2.默认是pg_catalog.english
"""
import os
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class FullTextSearch(unittest.TestCase):
    def setUp(self):
        logger.info('----------------this is setup-----------------------')
        logger.info(
            '---Opengauss_Function_Text_Match_Case0006开始执行-----')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.comsh = CommonSH('dbuser')
        self.com = Common()
        self.file_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        self.expect_result_dict = {
            'Schema': ['pg_catalog', 'pg_catalog', 'pg_catalog', 'pg_catalog',
                       'pg_catalog', 'pg_catalog', 'pg_catalog', 'pg_catalog',
                       'pg_catalog', 'pg_catalog', 'pg_catalog', 'pg_catalog',
                       'pg_catalog', 'pg_catalog', 'pg_catalog', 'pg_catalog',
                       'pg_catalog', 'pg_catalog',
                       'pg_catalog'],
            'Name': ['danish', 'dutch', 'english', 'finnish', 'french',
                     'german', 'hungarian', 'italian', 'ngram',
                     'norwegian', 'portuguese', 'pound', 'romanian', 'russian',
                     'simple', 'spanish', 'swedish',
                     'turkish', 'zhparser']}

    def test_text_match(self):
        sql_cmd = self.comsh.execut_db_sql('''drop database if exists test_db;
            create database test_db;''')
        logger.info(sql_cmd)
        excute_cmd1 = f'''source {self.DB_ENV_PATH};\
        gsql -d test_db \
        -p {self.userNode.db_port} \
        -U {self.userNode.ssh_user} \
        -c "\dF"
        '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        result_dict = self.com.format_sql_result(msg1)
        logger.info(result_dict)
        del result_dict['Description']
        self.assertDictEqual(self.expect_result_dict, result_dict)
        self.res = msg1.splitlines()[-2].strip()
        excute_cmd = f'cat {self.file_path}| grep default_text_search_config;'
        logger.info(excute_cmd)
        msg1 = self.userNode.sh(excute_cmd).result()
        logger.info(msg1)
        self.assertIn('pg_catalog.english', msg1)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        sql_cmd = self.comsh.execut_db_sql('''drop database test_db;''')
        logger.info(sql_cmd)
        logger.info(
            '----Opengauss_Function_Text_Match_Case0006执行完成-----')
