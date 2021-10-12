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
Case Name   : 使用不同方式设置文本搜索配置
Description :
    1.-创建数据库
    2.连接test_db007数据库，查看默认分词器
    3.修改分词器参数值,设置数据库级别的参数
    4.退出会话，查询
    5.恢复默认
    6.设置会话级别的参数
    7.恢复默认值
    8.删除数据库
Expect      :
    1.创建数据库成功
    2.查看默认分词器为pg_catalog.english
    3.不退出会话，查看参数值（不生效）
    4.分词器为pg_catalog.simple
    5.恢复默认值成功
    6.设置成功
    7.恢复默认值成功
    8.删除数据库成功
History     :
"""
import unittest
import time
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class FullTextSearch(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_Function_Text_Match_Case0007开始执行--------------------------")
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_dictionary(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop database if exists test_db007;
                                         create database test_db007;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_DATABASE_SUCCESS, sql_cmd1)
        sql_cmd2 = '''show default_text_search_config;
                      ALTER DATABASE test_db007 SET default_text_search_config to 'pg_catalog.simple';
                      show default_text_search_config;'''
        excute_cmd1 = f'''
                                  source {self.DB_ENV_PATH};
                                  gsql -d test_db007 -p {self.userNode.db_port} -c "{sql_cmd2}"
                                  '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.res = sql_cmd2.splitlines()[-2].strip()
        self.assertIn(constant.ALTER_DATABASE_SUCCESS_MSG, msg1)
        time.sleep(3)
        sql_cmd3 = ''' show default_text_search_config;
        ALTER DATABASE test_db007 SET default_text_search_config to 'pg_catalog.english';'''
        excute_cmd1 = f'''
                                         source {self.DB_ENV_PATH};
                                         gsql -d test_db007 -p {self.userNode.db_port} -c "{sql_cmd3}"
                                         '''
        logger.info(sql_cmd3)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('simple', msg1)
        self.assertIn(constant.ALTER_DATABASE_SUCCESS_MSG, msg1)
        time.sleep(3)
        sql_cmd4 = ''' show default_text_search_config;
                      set default_text_search_config to 'simple';
                      show default_text_search_config;'''
        excute_cmd1 = f'''
                                                source {self.DB_ENV_PATH};
                                                gsql -d test_db007 -p {self.userNode.db_port} -c "{sql_cmd4}"
                                                '''
        logger.info(sql_cmd3)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('english', msg1)
        self.assertIn(constant.SET_SUCCESS_MSG, msg1)
        self.assertIn('simple', msg1)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd5= commonsh.execut_db_sql('''reset default_text_search_config;
        drop database test_db007;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_Text_Match_Case0007执行结束--------------------------')

