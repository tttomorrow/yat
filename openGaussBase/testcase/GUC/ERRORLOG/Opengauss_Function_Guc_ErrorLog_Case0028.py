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
Case Name   : 参数log_truncate_on_rotation的值为非法的
Description :
    1.设置log_truncate_on_rotation参数的值为数值类型：gs_guc reload -N all -I all 
    -c"log_truncate_on_rotation=5"
    2.设置log_truncate_on_rotation参数的值为空：gs_guc reload -N all -I all -c
      "log_truncate_on_rotation=null"
    3.设置log_truncate_on_rotation参数的值为非法字符串：gs_guc reload -N all -I all
     -c"log_truncate_on_rotation=‘abc’"
Expect      :
    1.返回报错信息：ERROR: The value "5" for parameter "log_truncate_on_rotation" 
    is incorrect
    2.返回报错信息：ERROR: The value "null" for parameter 
    "log_truncate_on_rotation" is incorrect
    3.返回报错信息：ERROR: The value "'abc'" for parameter 
    "log_truncate_on_rotation" is incorrect
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0024 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info("-------修改参数log_truncate_on_rotation值为5-------")
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c ' \
                      f'"log_truncate_on_rotation=5"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find(
            "The value \"5\" for parameter \"log_truncate_on_rotation\" is "
            "incorrect") > -1)
        self.logger.info("-----修改参数log_truncate_on_rotation值为'abc'-----")
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_truncate_on_rotation=\'abc\'"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find(
            "The value \"'abc'\" for parameter \"log_truncate_on_rotation\" "
            "is incorrect") > -1)
        self.logger.info("------修改参数log_truncate_on_rotation值为null----")
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_truncate_on_rotation=null"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find(
            "The value \"null\" for parameter \"log_truncate_on_rotation\" "
            "is incorrect") > -1)

    def tearDown(self):
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0024 finish--')
