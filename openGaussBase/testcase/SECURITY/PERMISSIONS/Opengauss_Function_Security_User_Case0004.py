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
Case Name   : 普通用户赋予管理员权限后修改密码并创建用户
Description :
    1.初始用户执行：create user wf with password '******';
                        grant all privileges to wf;
                        alter user wf with password '******';
    2.wf用户执行：create user user001 with password '******';
Expect      :
    1.CREATE ROLE
    ALTER ROLE
    ALTER ROLE
    2.CREATE ROLE
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
        self.logger.info('----------Opengauss_Function_Security_User_Case0004 start---------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password = macro.COMMON_PASSWD + "qaz"
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_user(self):
        self.logger.info('--------------------create user || table-------------------')
        sql_cmd1 = f'''create user wf with password '{macro.COMMON_PASSWD}';
                        grant all privileges to wf;
                        alter user wf with password '{self.new_password}';'''
        sql_cmd2 = f'''create user user001 with password '{macro.COMMON_PASSWD}';'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"
                    '''
        excute_cmd2 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  wf -W {self.new_password} -c "{sql_cmd2}"
                    '''
        self.logger.info(excute_cmd1)
        self.logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, msg1)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg2)

    def tearDown(self):
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.logger.info('----------------Opengauss_Function_Security_User_Case0004 end------------------')
        try:
            db_status = self.sh_primy.get_db_instance_status()
            self.logger.info(db_status)
            if db_status:
                pass
            else:
                is_started = self.sh_primy.start_db_cluster()
                self.assertTrue(is_started)
                self.logger.info(f'db_status: {is_started}')
        finally:
            sql_cmd1 = '''drop user if exists wf cascade;'''
            sql_cmd2 = '''drop user user001;'''
            excute_cmd1 = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  wf -W {self.new_password} -c "{sql_cmd2}"'''
            excute_cmd2 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd1}"'''
            self.logger.info(excute_cmd1)
            self.logger.info(excute_cmd2)
            msg1 = self.userNode.sh(excute_cmd1).result()
            msg2 = self.userNode.sh(excute_cmd2).result()
            self.logger.info(msg1)
            self.logger.info(msg2)
        self.logger.info('--------------Opengauss_Function_Security_User_Case0004 finish-----------------')
