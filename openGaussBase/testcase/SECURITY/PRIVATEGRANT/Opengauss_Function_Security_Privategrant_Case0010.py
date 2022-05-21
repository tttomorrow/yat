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
Case Type   : security
Case Name   : 授予private用户UPDATE行的权限
Description :
    1.初始用户执行：CREATE USER private WITH INDEPENDENT IDENTIFIED BY 'Gauss_234';
    2.private用户执行：CREATE TABLE granttest(W_WAREHOUSE_SK INTEGER NOT NULL,W_WAREHOUSE_ID CHAR(16) NOT NULL,
                    W_WAREHOUSE_NAME VARCHAR(20),W_WAREHOUSE_SQ_FT INTEGER,W_STREET_NUMBER CHAR(10),
                    W_STREET_NAME VARCHAR(60),W_STREET_TYPE CHAR(15),W_SUITE_NUMBER CHAR(10),W_CITY VARCHAR(60),
                    W_COUNTY VARCHAR(30),W_STATE CHAR(2));
                    REVOKE ALL PRIVILEGES ON granttest FROM private;
                    GRANT update ON granttest TO private;
                    INSERT INTO granttest(W_WAREHOUSE_SK, W_WAREHOUSE_ID, W_WAREHOUSE_NAME) VALUES (1, '1111', 'test1'),(2, '2222','test2');
                    update granttest set w_warehouse_name='hehe1' where w_warehouse_name='test1';
Expect      :
    1.CREATE ROLE
    2.REVOKE
    GRANT
    PERMISSION DENIED
    PERMISSION DENIED
History     :
"""
import os
import sys
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('----------Opengauss_Function_Security_Privategrant_Case0010 start-----------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_updatecolumn(self):

        logger.info('----------------------------create user && table-----------------------------')
        sql_cmd1 = f'''CREATE USER private WITH INDEPENDENT IDENTIFIED BY '{macro.COMMON_PASSWD}';'''
        sql_cmd2 = '''CREATE TABLE granttest(W_WAREHOUSE_SK INTEGER NOT NULL,W_WAREHOUSE_ID CHAR(16) NOT NULL,
                    W_WAREHOUSE_NAME VARCHAR(20),W_WAREHOUSE_SQ_FT INTEGER,W_STREET_NUMBER CHAR(10),
                    W_STREET_NAME VARCHAR(60),W_STREET_TYPE CHAR(15),W_SUITE_NUMBER CHAR(10),W_CITY VARCHAR(60),
                    W_COUNTY VARCHAR(30),W_STATE CHAR(2));
                    REVOKE ALL PRIVILEGES ON granttest FROM private;
                    GRANT update ON granttest TO private;
                    INSERT INTO granttest(W_WAREHOUSE_SK, W_WAREHOUSE_ID, W_WAREHOUSE_NAME) VALUES (1, '1111', 'test1'),(2, '2222','test2');
                    update granttest set w_warehouse_name='hehe1' where w_warehouse_name='test1';
                    '''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        excute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  private -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg1)
        logger.info(msg2)
        self.assertIn(self.Constant.REVOKE_SUCCESS_MSG, msg2)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg2)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg2)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg2)

    def tearDown(self):
        sql_cmd1 = '''drop table granttest;'''
        sql_cmd2 = '''drop user private;'''

        excute_cmd1 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U private -W '{macro.COMMON_PASSWD}' -c "{sql_cmd1}"
                        '''
        excute_cmd2 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd2}"'''
        logger.info(excute_cmd1)
        logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg1)
        logger.info(msg2)
        logger.info('----Opengauss_Function_Security_Privategrant_Case0010 finish---------------')
