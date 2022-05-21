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
Case Type   : GUC_ErrorLog
Case Name   : 设置参数log_rotation_size值为设置值为1MB，1GB
Description :
    1.设置参数log_rotation_size值为1MB：gs_guc reload -N all -I all -c
    "log_rotation_size=1MB",查看修改后的参数：show log_rotation_size;
    2.设置参数log_rotation_size值为1GB：gs_guc reload -N all -I all -c
    "log_rotation_size=1GB",查看修改后的参数：show log_rotation_size;
Expect      :
    1.返回值：1MB
    2.返回值：1GB
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0040 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('----------查看log_rotation_size默认值----------')
        sql_cmd0 = 'show log_rotation_size;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'log_rotation_size', '20MB', '(1 row)',
                                flag='1')
        self.logger.info('---------设置参数log_rotation_size值为1MB--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_rotation_size=1MB"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('----------查看log_rotation_size修改后的值----------')
        sql_cmd2 = 'show log_rotation_size;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_rotation_size', '1MB', '(1 row)',
                                flag='1')
        self.logger.info('---------设置参数log_rotation_size值为1GB--------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "log_rotation_size=1GB"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('----------查看log_rotation_size修改后的值----------')
        sql_cmd4 = 'show log_rotation_size;'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.common.equal_sql_mdg(msg4, 'log_rotation_size', '1GB', '(1 row)',
                                flag='1')

    def tearDown(self):
        self.logger.info('--------------恢复配置----------')
        excute_cmd1 = f' source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_rotation_size=20MB"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('------------查看 log_rotation_size修改后的值--------')
        sql_cmd2 = 'show log_rotation_size;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_rotation_size', '20MB', '(1 row)',
                                flag='1')
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0040 finish--')
