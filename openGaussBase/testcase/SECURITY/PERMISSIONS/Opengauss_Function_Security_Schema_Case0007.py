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
Case Name   : 查看schema列表
Description :
    1.初始用户执行：CREATE USER wf WITH PASSWORD '$PASSWORD';
    GRANT ALL PRIVILEGES TO wf;
    2.wf用户执行：SELECT nspname FROM pg_namespace where nspname='wf';
Expect      :
    1.CREATE ROLE
    GRANT
    2.查出wf的schema信息
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
        logger.info(
            '----Opengauss_Function_Security_Schema_Case0007 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()
    
    def test_schema(self):
        logger.info('--------create user || table---------')
        sql_cmd1 = f'CREATE USER wf WITH PASSWORD \'{macro.COMMON_PASSWD}\';' \
            f'GRANT ALL PRIVILEGES TO wf;'
        sql_cmd2 = 'SELECT nspname FROM pg_namespace where nspname=\'wf\';'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-c "{sql_cmd1}"'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U ' \
            f'wf -W \'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd1)
        logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'nspname', 'wf', '(1 row)', flag='1')
    
    def tearDown(self):
        sql_cmd1 = 'drop user if exists wf cascade;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
            f' gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-c "{sql_cmd1}"'
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Schema_Case0007 finish----')
