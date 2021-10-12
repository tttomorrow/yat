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
Case Name   : 不同Schema中存在同名的对象时，查询对象不指定Schema
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
        logger.info('--------------Opengauss_Function_Security_Schema_Case0010 start-------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()

    def test_schema(self):
        logger.info('----------------------------create user || table-----------------------------')
        sql_cmd1 = '''CREATE SCHEMA wf_schema001;
                    CREATE SCHEMA wf_schema002;
                    CREATE TABLE wf_schema001.wf_table001(id int,name char(10));
                    INSERT INTO wf_schema001.wf_table001 VALUES(4,'lili');
                    CREATE TABLE wf_schema002.wf_table001(id int,name char(10));
                    INSERT INTO wf_schema002.wf_table001 VALUES(6,'jhon');
                    '''
        sql_cmd2 = '''SELECT *  FROM wf_schema001.wf_table001;'''
        sql_cmd3 = '''SELECT *  FROM wf_schema002.wf_table001;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        excute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd2}"
                    '''
        excute_cmd3 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd3}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'id |    name', '4 | lili', '(1 row)', flag='1')
        logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'id |    name', '6 | jhon', '(1 row)', flag='1')

    def tearDown(self):
        sql_cmd1 = '''DROP TABLE wf_schema002.wf_table001;
                    DROP TABLE wf_schema001.wf_table001;
                    DROP SCHEMA wf_schema002;
                    DROP SCHEMA wf_schema001;
                    '''
        excute_cmd1 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"'''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info('---------------Opengauss_Function_Security_Schema_Case0010 finish-------------')
