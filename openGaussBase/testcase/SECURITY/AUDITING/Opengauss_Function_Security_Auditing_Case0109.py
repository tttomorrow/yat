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
Case Name   : 审计日志文件的最小保存时间默认90天
Description :
    1.登录数据库执行show audit_file_remain_time
Expect      :
    1.返回90
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
        logger.info('--Opengauss_Function_Security_Auditing_Case0109 start--')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        sql_cmd = 'show audit_resource_policy;'
        msg = self.sh_primy.execut_db_sql(sql_cmd)
        logger.info(msg)
        self.common.equal_sql_mdg(msg, 'audit_resource_policy', 'on',
                                  '(1 row)', flag="1")

    def test_policy(self):
        sql_cmd1 = '''show audit_file_remain_time;'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'audit_file_remain_time', '90',
                                  '(1 row)', flag="1")

    def tearDown(self):
        logger.info('--Opengauss_Function_Security_Auditing_Case0109 finish--')
