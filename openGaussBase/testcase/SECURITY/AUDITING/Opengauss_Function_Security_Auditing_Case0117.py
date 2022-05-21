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
Case Type   : security
Case Name   : 审计日志删除，starttime或endtime非法
Description :
    1.登录数据库执行SELECT pg_delete_audit('start_time ','end_time');
    start_time or en_time illegall
Expect      :
    1.提示无效的输入
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
        logger.info('--Opengauss_Function_Security_Auditing_Case0117 start--')
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
        sql_cmd1 = '''SELECT pg_delete_audit('start_time ','end_time');'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.find('ERROR:  invalid input syntax') > -1)

    def tearDown(self):
        logger.info('--Opengauss_Function_Security_Auditing_Case0117 finish--')
