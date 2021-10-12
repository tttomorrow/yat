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
Case Name   : 设置分词器解析为ngram，检索中文字符
Description :
    1.创建一个GBK编码的数据库music
    2.切换至music数据库创建模式
    3.创建表并插入数据
    4.设置文本搜索解析器为ngram
    5.检索中文（添加配置项）
    6.检索中文（省略配置项）
    7.恢复默认值
    8.删除表
    9.删除模式
Expect      :
    1.创建数据库成功
    2.模式创建成功
    3.建表成功且数据插入成功
    4.设置成功
    5.检索成功
    6.检索成功
    7.恢复默认值成功
    8.删除表成功
    9.模式删除成功
"""
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class FullTextSearch(unittest.TestCase):

    def setUp(self):
        logger.info(
            "---Opengauss_Function_Text_Search_Case0008开始执行---------")
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_dictionary(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop database if exists music;
        create database music encoding 'gbk' template = template0;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_DATABASE_SUCCESS, sql_cmd1)
        sql_cmd2 = '''drop schema if exists tsearch cascade;
                    create schema tsearch;
                    drop table if exists tsearch.ts_ngram;
                    create table tsearch.ts_ngram(id int, body text);
                    insert into tsearch.ts_ngram values(1, '中文');
                    insert into tsearch.ts_ngram values(2, '中文检索');
                    insert into tsearch.ts_ngram values(3, '检索中文');'''
        excute_cmd1 = f'''source {self.DB_ENV_PATH};\
        gsql -d music -p {self.userNode.db_port} -c "{sql_cmd2}"'''
        logger.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.CREATE_SCHEMA_SUCCESS_MSG, msg1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, msg1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, msg1)
        sql_cmd3 = '''set default_text_search_config to ngram;
        show default_text_search_config;
        SELECT id, body, ts_rank_cd(to_tsvector('ngram',body), query) AS rank \
        FROM tsearch.ts_ngram, to_tsquery('中文') query WHERE \
        query @@ to_tsvector(body);
        SELECT id, body, ts_rank_cd(to_tsvector('ngram',body), query) AS rank \
        FROM tsearch.ts_ngram, to_tsquery('中文') query WHERE \
        query @@ to_tsvector('ngram',body);
        reset default_text_search_config;'''
        excute_cmd1 = f'''source {self.DB_ENV_PATH};\
        gsql -d music -p {self.userNode.db_port} -c "{sql_cmd3}"'''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.SET_SUCCESS_MSG, msg1)
        self.res = sql_cmd2.splitlines()[-2].strip()
        self.assertIn(constant.RESET_SUCCESS_MSG, msg1)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop database if exists music;''')
        logger.info(sql_cmd4)
        logger.info(
            '----Opengauss_Function_Text_Search_Case0008执行结束-----')
