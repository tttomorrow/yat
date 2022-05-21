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
Case Type   : security-auditing
Case Name   : 设置audit_system_object=-1，不支持
Description :
    1.设置"audit_system_object=-1"
Expect      :
    1.设置失败，超出范围
History     :
"""
import unittest
import os
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant




class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
    
    def test_security(self):
        text = '-----step1:设置"audit_system_object=-1";expect:失败-----'
        self.logger.info(text)
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"audit_system_object=-1"'
        msg1 = self.common.get_sh_result(self.userNode, excute_cmd1)
        self.assertIn('ERROR: The value -1 is outside the valid range '
                      'for parameter', msg1, text + '执行失败')
    
    def tearDown(self):
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
