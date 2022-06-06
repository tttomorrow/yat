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
Case Type   : Separation_rights
Case Name   : 普通用户修改角色
Description :
    1.初始用户执行：CREATE USER sysadmin01 WITH password '$PASSWORD1';
                CREATE ROLE manager IDENTIFIED BY '$PASSWORD2';
    2.sysadmin01 用户执行：ALTER ROLE manager IDENTIFIED BY '$PASSWORD3'
    REPLACE '$PASSWORD2';
Expect      :
    1.CREATE ROLE
    2.CREATE ROLE
    PERMISSION DENIED
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_Security_Separation_Case0027 start----')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.new_password = macro.COMMON_PASSWD + "qaz"
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('------------create user -------------')
        sql_cmd1 = f'CREATE USER sysadmin01 WITH password ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'CREATE ROLE manager IDENTIFIED BY ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        sql_cmd2 = f'ALTER ROLE manager IDENTIFIED BY \'' \
                   f'{self.new_password}\' REPLACE \'{macro.COMMON_PASSWD}\';'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U sysadmin01 -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.PERMISSION_DENY_MSG, msg2)

    def tearDown(self):
        logger.info('-----------清理环境-----------')
        sql_cmd1 = 'DROP ROLE manager;DROP USER sysadmin01;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Separation_Case0027 finish----')
