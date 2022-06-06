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
Case Type   : 常量与宏
Case Name   : CURRENT_CATALOG有效值测试
Description :
    1.查看当前数据库CURRENT_CATALOG
    2.创建新数据库testdb
    3.切换至数据库testdb
    4.查看当前CURRENT_CATALOG
    5.删除数据库
Expect      :
    1.显示当前连接的数据库
    2.新数据创建成功
    3.切换数据库成功
    4.当前数据库为testdb
    5.删除数据库成功
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class ConstantsMacros(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0001开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_current_catalog(self):
        sql_cmd1 = commonsh.execut_db_sql('''select current_catalog;''')
        logger.info(sql_cmd1)
        self.res = sql_cmd1.splitlines()[-2].strip()
        sql_cmd2 = commonsh.execut_db_sql('''drop database if exists testdb;
                                           create database testdb;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_DATABASE_SUCCESS, sql_cmd2)
        sql_cmd3 = '''select current_catalog;
                      select current_database();'''
        excute_cmd1 = f'''
                           source {self.DB_ENV_PATH};
                           gsql -d testdb -p {self.userNode.db_port} -c "{sql_cmd3}"
                           '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('testdb', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop database if exists testdb;''')
        logger.info(sql_cmd3)
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0001执行结束--------------------------')
