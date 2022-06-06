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
Case Name   : 设置参数log_rotation_size值为设置值为非法
Description :
    1.设置参数log_rotation_size值为-1：gs_guc reload -N all -I all -c
    "log_rotation_size=-1"
    2.设置参数log_rotation_size值为2097152：gs_guc reload -N all -I all -c
    "log_rotation_size=2097152"
    3.设置参数log_rotation_size值为2097151MB：gs_guc reload -N all -I all -c
    "log_rotation_size=2097151MB"
    4.设置参数log_rotation_size值为10.5MB：gs_guc reload -N all -I all \-c
    "log_rotation_size=10.5MB
    5.设置参数log_rotation_size值为2GB：gs_guc reload -N all -I all -c
    "log_rotation_size=2GB"
Expect      :
    1.返回报错：ERROR: The value -1 is outside the valid range for parameter
    "log_rotation_size" (0 .. 2097151)
    2.返回报错：ERROR: The value 2097152 is outside the valid range for
    parameter "log_rotation_size" (0 .. 2097151)
    3.返回报错ERROR: The value 2147482624 is outside the valid range for
    parameter "log_rotation_size" (0 .. 2097151)
    4.返回报错ERROR: The parameter "log_rotation_size" requires an integer value
    5.返回报错ERROR: The value "2GB" for parameter "log_rotation_size" is
    incorrect
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0041 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('----修改参数log_rotation_size值为-1-----')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c "log_rotation_size=-1"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(
            msg1.find("The value -1 is outside the valid range for parameter "
                      "\"log_rotation_size\" (0 .. 2097151)") > -1)
        self.logger.info('-----修改参数log_rotation_size值为2097152-----')
        excute_cmd2 = f' source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_rotation_size=2097152"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find(
                "The value 2097152 is outside the valid range for parameter "
                "\"log_rotation_size\" (0 .. 2097151)") > -1)
        self.logger.info('------修改参数log_rotation_size值为2097151MB-------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_rotation_size=2097151MB"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(
            msg3.find("The value 2147482624 is outside the valid range for "
                      "parameter \"log_rotation_size\" (0 .. 2097151)") > -1)
        self.logger.info('--------修改参数log_rotation_size值为10.5MB-----')
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_rotation_size=10.5MB"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find("The parameter \"log_rotation_size\" "
                                  "requires an integer value") > -1)
        self.logger.info('--------修改参数log_rotation_size值为2GB--------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_rotation_size=2GB"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find('The value "2GB" for parameter '
                                  '"log_rotation_size" is incorrect') > -1)

    def tearDown(self):
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0041 finish--')
