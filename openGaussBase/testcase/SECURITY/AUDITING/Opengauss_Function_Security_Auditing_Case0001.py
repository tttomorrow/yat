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
Case Type   : security-auditing
Case Name   : 查看审计总开关audit_enabled的值默认为on
Description :
    步骤 1.登录数据库，查看audit_enabled的默认值，SHOW audit_enabled;
Expect      :
    步骤 1.显示on
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '--Opengauss_Function_Security_Auditing_Case0001 start--')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        sql_cmd1 = 'show audit_enabled;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'audit_enabled', 'on', '(1 row)',
                                  flag="1")

    def tearDown(self):
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0001 finish----')
