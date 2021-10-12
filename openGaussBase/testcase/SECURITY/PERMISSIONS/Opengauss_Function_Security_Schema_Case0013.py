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
Case Name   : 更改当前会话的默认Schema
Description :
    1.初始用户执行：CREATE SCHEMA wf_schema;
                    SET SEARCH_PATH TO wf_schema, public;
                    SHOW SEARCH_PATH;
Expect      :
    1.CREATE SCHEMA
    SET
    查询出SCHEMA路径“wf_schema, public”
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
        logger.info('--------------Opengauss_Function_Security_Schema_Case0013 start-------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()

    def test_schema(self):
        logger.info('----------------------------create user || table-----------------------------')
        sql_cmd1 = '''CREATE SCHEMA wf_schema;
                    SET SEARCH_PATH TO wf_schema, public;
                    SHOW SEARCH_PATH;
                    '''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'CREATE SCHEMA', 'SET', 'search_path', '-------------------', 'wf_schema, public',
                                '(1 row)')

    def tearDown(self):
        sql_cmd1 = '''drop schema  wf_schema;'''
        excute_cmd1 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"'''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info('--------------Opengauss_Function_Security_Schema_Case0013 finish------------')
