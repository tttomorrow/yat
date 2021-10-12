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
Case Name   : 审计文件占用的磁盘空间总量小于1024GB
Description :
    1.登录数据库执行gs_guc reload -N all -I all -c "audit_space_limit=1023"
Expect      :
    1.报错，提示超范围
History     :
"""
import unittest
import datetime
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0106 start----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        sql_cmd1 = f'source {self.DB_ENV_PATH};' \
                   f'gs_guc reload -N all -I all -c "audit_space_limit=1023"'
        msg1 = self.userNode.sh(sql_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find(
            'The value 1023 is outside the valid range for parameter '

    def tearDown(self):
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0106 end----')
