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
Case Type   : Separation_permission
Case Name   : 支持CREATE权限
Description :
    1.初始用户执行：create user wf with password '$PASSWORD';
                    grant create on database $database to wf;
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
        self.user = 'u_security_permission_0001'
        self.table = 'table_security_permission_0001'
    
    def test_default_permission(self):
        logger.info('------------create user || table------------')
        sql_cmd1 = f'drop user if exists {self.user};' \
            f'create user {self.user} with ' \
            f'password \'{macro.COMMON_PASSWD}\';' \
            f'grant create on database {self.userNode.db_name} to {self.user};'
        logger.info(sql_cmd1)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg1)
        sql_cmd2 = f'drop table if exists {self.table};' \
            f'create table {self.table}(col_1 int,col_2 int, col_3 int);' \
            f'drop table {self.table};'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.user} -W ' \
            f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg2)
    
    def tearDown(self):
        logger.info('------清理环境------')
        sql_cmd1 = f'drop user {self.user} cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0001 finish----')
