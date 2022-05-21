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
Case Name   : 修改参数plog_merge_age的值为非法值
Description :
    1.修改参数plog_merge_age的值为-1：gs_guc reload -N all -I all -c
     "plog_merge_age=-1"
    2.修改参数plog_merge_age的值2147483648:gs_guc reload -N all -I all
     -c "plog_merge_age=2147483648"
    3.修改参数plog_merge_age的值为10.5：gs_guc reload -N all -I all -c
     "plog_merge_age=10.5"
    4.修改参数plog_merge_age的值为null：gs_guc reload -N all -I all -c
     "plog_merge_age=null"
    5.修改参数plog_merge_age的值为stdee: gs_guc reload -N all -I all -c
     "plog_merge_age='stdee'"
Expect      :
    1.返回报错信息：ERROR: The value 2147483648 is outside the valid range
    for parameter "plog_merge_age" (0 .. 2147483647)
    2.返回报错信息：ERROR: The value 2147483648 is outside the valid range
    for parameter "plog_merge_age" (0 .. 2147483647)
    3.返回报错信息：The parameter "plog_merge_age" requires an integer value.
    4.返回报错信息：The parameter "plog_merge_age" requires an integer value
    5.返回报错信息：The parameter "plog_merge_age" requires an integer value
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0078 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info("--------修改参数plog_merge_age值为-1---------")
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c "plog_merge_age=-1"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(
            msg1.find("The value -1 is outside the valid range for parameter "
                      "\"plog_merge_age\" (0 .. 2147483647)") > -1)
        self.logger.info("-------修改参数plog_merge_age值为2147483648----")
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"plog_merge_age=2147483648"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(
            msg2.find("The value 2147483648 is outside the valid range for "
                      "parameter \"plog_merge_age\" (0 .. 2147483647)") > -1)
        self.logger.info("---------修改参数plog_merge_age值为10.5--------")
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "plog_merge_age=10.5"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(
            msg2.find("The parameter \"plog_merge_age\" requires an integer "
                      "value") > -1)
        self.logger.info("-------修改参数plog_merge_age值为stdee----------")
        excute_cmd2 = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
                      f'all -c "plog_merge_age=\'stdee\'"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(
            msg2.find("The parameter \"plog_merge_age\" requires an integer "
                      "value") > -1)
        self.logger.info("---------修改参数plog_merge_age值为null--------")
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "plog_merge_age=null"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(
            msg2.find("The parameter \"plog_merge_age\" requires an integer "
                      "value") > -1)

    def tearDown(self):
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0078 finish--')