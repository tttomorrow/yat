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
Case Name   : 普通用户无CREATE权限不能创建Schema
Description :
    1.初始用户执行：CRETE USER wf WITH password '*****';
    2.wf用户执行：CREATE SCHEMA schema01;
Expect      :
    1.CREATE SCHEMA1.CREATE ROLE
    2.PERMISSION DENIED
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_Security_Schema_Case0002 start------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_schema(self):
        logger.info('-------------------------create user || table-------------------------')
        sql_cmd1 = f'''create user wf with password '{macro.COMMON_PASSWD}';'''
        sql_cmd2 = "CREATE SCHEMA schema01;"
        execute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        execute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  wf -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                    '''
        logger.info(execute_cmd1)
        logger.info(execute_cmd2)
        msg1 = self.userNode.sh(execute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        msg2 = self.userNode.sh(execute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg2)

    def tearDown(self):
        sql_cmd1 = '''drop schema schema01;'''
        execute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  wf -W '{macro.COMMON_PASSWD}' -c "{sql_cmd1}"'''
        logger.info(execute_cmd1)
        msg1 = self.userNode.sh(execute_cmd1).result()
        logger.info(msg1)
        sql_cmd2 = '''drop user if exists wf cascade;'''
        execute_cmd2 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd2}"'''

        logger.info(execute_cmd2)
        msg2 = self.userNode.sh(execute_cmd2).result()
        logger.info(msg2)
        logger.info('--------Opengauss_Function_Security_Schema_Case0002 finish------------')
