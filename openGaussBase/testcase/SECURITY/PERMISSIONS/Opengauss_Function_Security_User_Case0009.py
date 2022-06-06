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
Case Type   : security-user
Case Name   : alter用户为系统管理员
Description :
    1.初始用户执行：CREATE USER sysadmin WITH SYSADMIN password '$PASSWORD';
Expect      :
    1.CREATE ROLE
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '----Opengauss_Function_Security_User_Case0009 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
    
    def test_default_permission(self):
        self.logger.info(
            '-------create user || table------')
        sql_cmd1 = f'CREATE USER adminuser WITH ' \
            f'password \'{macro.COMMON_PASSWD}\';' \
            f'ALTER USER adminuser SYSADMIN;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-c "{sql_cmd1}"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, msg1)
    
    def tearDown(self):
        self.logger.info('--------清理环境------')
        sql_cmd1 = f'drop user if exists adminuser cascade;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-c "{sql_cmd1}"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info(
            '------Opengauss_Function_Security_User_Case0009 finish-----')
