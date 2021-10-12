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
Case Type   : Separation_permission
Case Name   : 支持CREATE权限
Description :
    1.初始用户执行：create user wf with password 'Qazwsx@123';
                    grant create on database postgres to wf;
    2.wf用户执行：create table security_table02(col_1 int,col_2 int, col_3 int);
Expect      :
    1.CREATE ROLE
    GRANT
    2.CREATE TABLE
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
        logger.info(
            '---Opengauss_Function_Security_Permission_Case0001 start-----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_default_permission(self):
        logger.info('------------create user || table------------')
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';' \
                   f'grant create on database postgres to wf;'
        sql_cmd2 = 'create table ' \
                   'security_table02(col_1 int,col_2 int, col_3 int);'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd1}"'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd1)
        logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg1)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg2)

    def tearDown(self):
        sql_cmd1 = 'drop table if exists security_table02 cascade;'
        sql_cmd2 = 'drop user if exists wf cascade;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U wf -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd1}"'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd2}"'
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0001 finish----')
