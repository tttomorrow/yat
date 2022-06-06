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
Case Type   : 用户-权限测试
Case Name   : 创建的用户赋予CREATEDB权限，创建数据库，成功
Description :
    1.创建用户
    2.用户创建数据库
    3.删除用户
Expect      :
    1.用户创建成功
    2.数据库创建成功
    3.用户删除成功
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


class userpermission(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_User_Case0006开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        sql_cmd1 = commonsh.execut_db_sql(f'''drop user if exists test_user006 cascade;
       create user test_user006 with CREATEDB identified by '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = '''drop database if exists test_user006db;
                      create database test_user006db encoding 'UTF8'; '''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_user006 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg1)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop database if exists test_user006db;
                                        drop user if exists test_user006 cascade;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DDL_User_Case0006执行结束--------------------------')