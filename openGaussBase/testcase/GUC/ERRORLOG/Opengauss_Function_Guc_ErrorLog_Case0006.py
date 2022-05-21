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
Case Name   : 设置参数log_destination的值为非法的，不支持
Description :
    1.设置参数log_destination的值为数值类型：gs_guc reload -N all -I all
    -c "log_destination=5"
    2.设置参数log_destination的值为其他字符串：gs_guc reload -N all -I all
    -c "log_destination='abc'"
Expect      :
    1.参数设置失败，返回报错信息：ERROR: The value "5" for parameter
    "log_destination" is incorrect.
    Please do it like this "parameter = 'value'"
    2.登录数据库查看，参数未生效，仍未默认值stdrr
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0006 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info("----------修改参数log_destination值为5------------")
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_destination=5"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(
            msg1.find("for parameter \"log_destination\" is incorrect") > -1)
        self.logger.info("----------修改参数log_destination值为'abc'-----------")
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_destination=\'abc\'"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        sql_cmd3 = '''show log_destination;'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'log_destination', 'stderr', '(1 row)',
                                flag='1')

    def tearDown(self):
        self.logger.info('-----------,恢复配置-----------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_destination=\'stderr\'"'
        self.logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg1)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0006 finish--')
