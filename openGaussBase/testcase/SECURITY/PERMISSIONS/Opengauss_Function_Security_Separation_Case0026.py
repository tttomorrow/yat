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
Case Type   : Separation_rights
Case Name   : 系统管理员用户删除角色
Description :
    1.初始用户执行：CREATE ROLE manager IDENTIFIED BY 'Bigdata@123';
                DROP ROLE manager;
Expect      :
    1.CREATE ROLE
    DROP ROLE
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
            '----Opengauss_Function_Security_Separation_Case0026 start----')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('----------create user --------------')
        sql_cmd1 = f'CREATE ROLE manager IDENTIFIED BY ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'DROP ROLE manager;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U {self.userNode.ssh_user}' \
                      f' -c "{sql_cmd1}"'
        logger.info(excute_cmd1)
        msg2 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg2)
        self.assertTrue(msg2.find('DROP ROLE') > -1)

    def tearDown(self):
        logger.info(
            '----Opengauss_Function_Security_Separation_Case0026 finish----')
