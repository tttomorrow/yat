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
Case Type   : GUC
Case Name   : 参数log_rotation_age的值为非法的
Description :
    1.修改参数log_rotation_age的值为-1：gs_guc reload -N all -I all -c
    "log_rotation_age=-1"
    2.修改参数log_rotation_age的值为-5.5：gs_guc reload -N all -I all -c
     "log_rotation_age=5.5"
    3.修改参数log_rotation_age的值为sfg：gs_guc reload -N all -I all -c
    "log_rotation_age='dfg'"
    4.修改参数log_rotation_age的值为60s：gs_guc reload -N all -I all -c
     "log_rotation_age=60s"
Expect      :
    1.返回报错信息: The value -1 is outside the valid range for parameter
    "log_rotation_age"
    2.返回报错信息ERROR: Valid units for this parameter "log_rotation_age"
    are "min", "h", and "d"
    3.返回报错信息The parameter "log_rotation_age" requires an integer value
    4.返回报错信息ERROR: Valid units for this parameter "log_rotation_age" are
     "min", "h", and "d"
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Errorlog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0033 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info("--------修改参数log_rotation_age值为-1----------")
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c "log_rotation_age=-1"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find("The value -1 is outside the valid range "
                                  "for parameter \"log_rotation_age\" (0 .. "
                                  "35791394)") > -1)
        self.logger.info("------修改参数log_rotation_age值为'5.5'-------")
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_rotation_age=5.5"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find(
            "Valid units for this parameter \"log_rotation_age\" are "
            "\"min\", \"h\", and \"d\"") > -1)
        self.logger.info("---------修改参数log_rotation_age值为dfg-------")
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_rotation_age=\'dfg\'"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find("The parameter \"log_rotation_age\" "
                                  "requires an integer value") > -1)
        self.logger.info("------------修改参数log_rotation_age值为60s---------")
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_rotation_age=60s"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(
            msg3.find("Valid units for this parameter \"log_rotation_age\" "
                      "are \"min\", \"h\", and \"d\"") > -1)

    def tearDown(self):
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0033 finish--')
