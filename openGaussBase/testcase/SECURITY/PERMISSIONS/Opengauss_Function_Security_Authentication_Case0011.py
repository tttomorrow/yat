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
Case Name   : 修改密码到期提醒天数为1000，-1，不支持
Description :
    1.登录数据库，执行gs_guc set -N all -I all -c "password_notify_time=1000"
    2.gs_guc set -N all -I all -c "password_notify_time=-1
Expect      :
    1.修设置失败，参数超范围
    2.设置失败，参数无效
History     :
"""
import time
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '===Opengauss_Function_Security_Authentication_Case0011 start===')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_policy(self):
        self.logger.info('-------------设置password_notify_time------------')
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                   gs_guc set -N all -I all -c "password_notify_time=1000"'''
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find("ERROR: The value 1000 is outside the "
                                  "valid range for parameter "
                                  "\"password_notify_time\" (0 .. 999)") > -1)
        excute_cmd2 = f'''
                source {self.DB_ENV_PATH};
               gs_guc set -N all -I all -c "password_notify_time=-1"'''
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find(
            "ERROR: The value -1 is outside the valid range for parameter "
            "\"password_notify_time\" (0 .. 999)") > -1)

    def tearDown(self):
        self.logger.info(
            '===Opengauss_Function_Security_Authentication_Case0011 finish===')
