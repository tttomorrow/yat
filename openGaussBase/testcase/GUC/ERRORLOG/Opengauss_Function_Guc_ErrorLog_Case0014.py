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
Case Name   : 设置参数log_filename的值为设置非法值，合理报错
Description :
    1.设置参数logging_collector的值为数值：gs_guc reload -N all -I all -c
    \"log_filename=5"
    2.设置参数logging_collector的值为空值：gs_guc reload -N all -I all -c
    \"log_filename=null"
Expect      :
    1.参数设置失败，返回报错信息：ERROR: The value "5" for parameter "log_filename"
    is incorrect
    2.参数设置失败，返回报错信息：ERROR: The value "null" for parameter
    "log_filename" is incorrect
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0014 star--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('----------修改参数log_filename值为5---------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_filename=5"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find(
            'The value "5" for parameter "log_filename" is incorrect') > -1)
        self.logger.info('------------修改参数log_filename值为null-----------')
        excute_cmd3 = f' source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_filename=null"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find(
            'The value "null" for parameter "log_filename" is incorrect') > -1)

    def tearDown(self):
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0014 finish--')
