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
Case Name   : 文本搜索配置token_type（multisymbol）测试（解析器为pg_catalog.pound）
Description :
    1.创建数据库编码为UTF8
    2.切换至test_db_083数据库,创建文本搜索配置;创建simple字典
    3.增加文本搜索配置字串类型映射，token为multisymbol
    4.使用文本检索函数对所创建的词典配置test_pound083进行测试
    5.删除文本搜索配置
    6.删除词典
    7.删除test_db_083数据库
Expect      :
    1.创建数据库成功
    2.创建文本搜索配置成功；创建simple字典成功
    3.增加文本搜索配置字串类型映射成功
    4.检索成功
    5.删除成功
    6.删除成功
    7.删除数据库成功
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class FullTextSearch(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_Function_Text_Search_Configuration_Case0083开始执行--------------------------")
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.com = Common()

    def test_dictionary(self):
        logger.info('-------------创建数据库----------------')
        sql_cmd1 = commonsh.execut_db_sql('''drop database if exists test_db_083;
                                           create database test_db_083 encoding 'utf8' template = template0;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_DATABASE_SUCCESS, sql_cmd1)
        logger.info('-------------创建文本搜索配置和词典----------------')
        sql_cmd2 = '''drop text search configuration if exists test_pound083 cascade;
                      create text search configuration test_pound083 (parser=pg_catalog.pound);
                      drop text search dictionary if exists pg_dict083 cascade;
                      create text search dictionary pg_dict083 (template = simple);'''
        excute_cmd1 = f'''
                                            source {self.DB_ENV_PATH};
                                            gsql -d test_db_083 -p {self.userNode.db_port} -c "{sql_cmd2}"
                                                '''
        logger.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.CREATE_TEXT_SEARCH_CONFIGURATION, msg1)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, msg1)
        logger.info('-------------增加文本搜索配置和词典----------------')
        sql_cmd3 = '''alter text search configuration test_pound083 add mapping for multisymbol with pg_dict083;
                      select ts_debug('pound','8/2*9-4');'''
        excute_cmd1 = f'''
                                  source {self.DB_ENV_PATH};
                                  gsql -d test_db_083 -p {self.userNode.db_port} -c "{sql_cmd3}"
                                  '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.ALTER_TEXT_SEARCH_CONFIGURATION, msg1)
        self.assertIn('(multisymbol,"multiple symbol",8/2*9-4,{simple},simple,{8/2*9-4})', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop database test_db_083;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_Text_Search_Configuration_Case0083执行结束--------------------------')


