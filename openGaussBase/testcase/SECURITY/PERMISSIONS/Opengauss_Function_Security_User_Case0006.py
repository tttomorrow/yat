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
Case Type   : security-user
Case Name   : 收回用户所有权限
Description :
    1.初始用户执行：create user wf with sysadmin password ‘****';
    REVOKE ALL PRIVILEGES FROM wf;
    2.wf用户执行：create user user001 with password '****';
Expect      :
    1.CREATE ROLE
        GRANT
    2.PERMISSION DENIED
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-------------------Opengauss_Function_Security_User_Case0006 start-------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()

    def test_user(self):
        self.logger.info('----------------------------create user || table-----------------------------')
        sql_cmd1 = f'''create user wf with sysadmin password '{macro.COMMON_PASSWD}';
                        select usename FROM pg_user where usename='wf';
                        revoke all privileges from wf;'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue(msg1.find('ALTER ROLE') > -1)
        sql_cmd2 = f'''create user user001 with password '{macro.COMMON_PASSWD}';'''
        excute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U wf -W {macro.COMMON_PASSWD} -c "{sql_cmd2}"'''
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find('Permission denied') > -1)

    def tearDown(self):
        sql_cmd1 = '''drop user if exists wf cascade;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"'''
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-----------------Opengauss_Function_Security_User_Case0006 finish--------------')
