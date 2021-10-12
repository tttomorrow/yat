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
Case Type   : GUC
Case Name   : 设置参数log_directory的值为非法路径，数据库无法启动
Description :
    1.设置参数log_directory的值为无效字符串：gs_guc set -N all -I all -c
    "log_directory='/stgff'"，重启数据库
Expect      :
    1.设置参数无效，数据库启动失败
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common

Logger = Logger()


class Errorlog(unittest.TestCase):
    def setUp(self):
        Logger.info('--Opengauss_Function_Guc_ErrorLog_Case0013 start--')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.log_path = os.path.join(macro.PG_LOG_PATH, 'dn_6001')

    def test_errorlog(self):
        Logger.info('-------修改参数log_directory的值为错误路径------')
        self.sh_primysh.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'log_directory=\'/stgff\'', single=True)
        restart_msg = self.sh_primysh.restart_db_cluster()
        Logger.info(restart_msg)
        status_msg = self.sh_primysh.get_db_cluster_status()
        Logger.info(status_msg)

    def tearDown(self):
        Logger.info('---------恢复参数值----------')
        self.sh_primysh.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'log_directory=\'{self.log_path}\'', single=True)
        restart_msg = self.sh_primysh.restart_db_cluster()
        Logger.info(restart_msg)
        status_msg = self.sh_primysh.get_db_cluster_status()
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        Logger.info('-------参数校验--------')
        sql_cmd2 = 'show log_directory;'
        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        Logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_directory', f'{self.log_path}',
                                  '(1 row)', flag='1')
        Logger.info('--Opengauss_Function_Guc_ErrorLog_Case0013 finish--')
