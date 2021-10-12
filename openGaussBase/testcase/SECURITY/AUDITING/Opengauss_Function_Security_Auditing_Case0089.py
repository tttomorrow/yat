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
Case Type   : security
Case Name   : 设置audit_function_exec=-1，不支持
Description :
    1.设置gs_guc set -N all -I all -c "audit_function_exec=-1"
Expect      :
    1.设置失败，不支持负数
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('--Opengauss_Function_Security_Auditing_Case0089 start--')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        sql_cmd = 'show audit_resource_policy;'
        msg = self.sh_primy.execut_db_sql(sql_cmd)
        logger.info(msg)
        self.common.equal_sql_mdg(msg, 'audit_resource_policy', 'on',
                                  '(1 row)', flag="1")

    def test_policy(self):
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c "audit_function_exec=-1"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertTrue(msg1.find(
            'The value -1 is outside the valid range for parameter '
            '"audit_function_exec" (0 .. 1)') > -1)

    def tearDown(self):
        logger.info('--Opengauss_Function_Security_Auditing_Case0089 finish--')
