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
Case Type   : security
Case Name   : 赋予private用户对行的select权限
Description :
    1.初始用户执行：CREATE USER private WITH INDEPENDENT IDENTIFIED BY 'Gauss_234';
    2.private用户执行：CREATE TABLE granttest(W_WAREHOUSE_SK INTEGER NOT NULL,W_WAREHOUSE_ID CHAR(16) NOT NULL,
                    W_WAREHOUSE_NAME VARCHAR(20),W_WAREHOUSE_SQ_FT INTEGER,W_STREET_NUMBER CHAR(10),
                    W_STREET_NAME VARCHAR(60),W_STREET_TYPE CHAR(15),W_SUITE_NUMBER CHAR(10),W_CITY VARCHAR(60),
                    W_COUNTY VARCHAR(30),W_STATE CHAR(2));
                    REVOKE ALL PRIVILEGES ON granttest FROM private;
                    GRANT SELECT (W_WAREHOUSE_SK, W_WAREHOUSE_ID, W_WAREHOUSE_NAME) ON granttest TO private;
    3.private用户执行：select w_warehouse_sk,w_warehouse_id,w_warehouse_name from granttest;
Expect      :
    1.CREATE ROLE
    2.REVOKE
    GRANT
    3. w_warehouse_sk | w_warehouse_id | w_warehouse_name
    ----------------+----------------+------------------
    (0 rows)
History     :
"""
import os
import sys
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
common = Common()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('-----------Opengauss_Function_Security_Privategrant_Case0007 start----------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_selectcolumn(self):

        logger.info('----------------------------create user && table-----------------------------')
        sql_cmd1 = f'''CREATE USER private WITH INDEPENDENT IDENTIFIED BY '{macro.COMMON_PASSWD}';'''
        sql_cmd2 = '''CREATE TABLE granttest(W_WAREHOUSE_SK INTEGER NOT NULL,W_WAREHOUSE_ID CHAR(16) NOT NULL,
                    W_WAREHOUSE_NAME VARCHAR(20),W_WAREHOUSE_SQ_FT INTEGER,W_STREET_NUMBER CHAR(10),
                    W_STREET_NAME VARCHAR(60),W_STREET_TYPE CHAR(15),W_SUITE_NUMBER CHAR(10),W_CITY VARCHAR(60),
                    W_COUNTY VARCHAR(30),W_STATE CHAR(2));
                    REVOKE ALL PRIVILEGES ON granttest FROM private;
                    GRANT SELECT (W_WAREHOUSE_SK, W_WAREHOUSE_ID, W_WAREHOUSE_NAME) ON granttest TO private;
                    '''
        sql_cmd3 = '''select w_warehouse_sk,w_warehouse_id,w_warehouse_name from granttest;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        excute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  private -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                    '''
        excute_cmd3 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  private -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        msg3 = self.userNode.sh(excute_cmd3).result()
        logger.info(msg3)
        self.assertIn(self.Constant.REVOKE_SUCCESS_MSG, msg2)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg2)
        common.equal_sql_mdg(msg3, 'w_warehouse_sk | w_warehouse_id | w_warehouse_name', '(0 rows)', flag='1')

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
        logger.info('---------Opengauss_Function_Security_Privategrant_Case0007 finish--------------')
