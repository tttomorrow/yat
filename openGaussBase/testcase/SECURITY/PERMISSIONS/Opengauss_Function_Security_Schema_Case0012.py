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
Case Type   : security-schema
Case Name   : 数据库下不存在与用户名同名Schema，对象被添加到Public Schema下
Description :
    1.初始用户执行：CREATE SCHEMA wf;
            SELECT s.nspname AS nspowner FROM pg_namespace s WHERE nspname='wf';1.初始用户执行：CREATE SCHEMA wf_schema;
            CREATE TABLE wf_table001(id int,name char(10));
            select * from public.wf_table001;
Expect      :
    1.CREATE SCHEMA
    CREATE TABLE
    查询出表wf_table001中内容id name
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
        logger.info('-------------Opengauss_Function_Security_Schema_Case0012 start-----------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()

    def test_schema(self):
        logger.info('----------------------------create user || table-----------------------------')
        sql_cmd1 = '''CREATE SCHEMA wf_schema;
                    CREATE TABLE wf_table001(id int,name char(10));
                    select * from public.wf_table001;
                    '''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'CREATE SCHEMA', 'CREATE TABLE', 'id | name', '----+------', '(0 rows)')

    def tearDown(self):
        sql_cmd1 = '''drop table wf_table001;
                    drop schema  wf_schema;
                    '''
        excute_cmd1 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"'''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info('-------------Opengauss_Function_Security_Schema_Case0012 finish----------')
