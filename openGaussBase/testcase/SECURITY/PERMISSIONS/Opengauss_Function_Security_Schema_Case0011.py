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
Case Type   : security-schema
Case Name   : 登录数据库的用户名与数据库中的Schema同名，创建表会添加到该同名Schema下
Description :
    1.初始用户执行：CREATE SCHEMA wf_schema001;
                CREATE SCHEMA wf_schema002;
                CREATE TABLE wf_schema001.wf_table001(id int,name char(10));
                INSERT INTO wf_schema001.wf_table001 VALUES(4,'lili');
                CREATE TABLE wf_schema002.wf_table001(id int,name char(10));
                INSERT INTO wf_schema002.wf_table001 VALUES(6,'jhon');
                SELECT *  FROM wf_schema001.wf_table001;
                SELECT *  FROM wf_schema002.wf_table001;
Expect      :
    1.CREATE SCHEMA
    CREATE SCHEMA
    CREATE TABLE
    INSERT
    CREATE TABLE
    INSERT
    查询出表中内容
    查询出表中内容
History     :
"""
'''
Case Type   : schema
Case Name   : 登录数据库的用户名与数据库中的Schema同名，创建表会添加到该同名Schema下
Create at   :  2020/9/16
Description :  登录数据库的用户名与数据库中的Schema同名，创建表会添加到该同名Schema下
'''
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------Opengauss_Function_Security_Schema_Case0011 start---------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()

    def test_schema(self):
        logger.info('----------------------------create user || table-----------------------------')
        sql_cmd1 = f'''create database wfdb;
                    create user wf with password '{macro.COMMON_PASSWD}';
                    grant all privileges to wf;'''
        sql_cmd2 = '''CREATE SCHEMA wf;
                    CREATE TABLE wf_table001(id int,name char(10));
                    '''
        sql_cmd3 = '''select * from wf.wf_table001;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        excute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d wfdb -p {self.userNode.db_port} -U wf -W '{macro.COMMON_PASSWD}' -c"{sql_cmd2}"
                    '''
        excute_cmd3 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d wfdb -p {self.userNode.db_port} -U wf -W '{macro.COMMON_PASSWD}' -c"{sql_cmd3}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, msg1)
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.CREATE_SCHEMA_SUCCESS_MSG, msg2)
        logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'id | name', '(0 rows)', flag='1')

    def tearDown(self):
        sql_cmd1 = '''DROP database wfdb;
                    drop user if exists wf cascade;
                    '''
        excute_cmd1 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"'''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info('--------------Opengauss_Function_Security_Schema_Case0011 finish-----------')
