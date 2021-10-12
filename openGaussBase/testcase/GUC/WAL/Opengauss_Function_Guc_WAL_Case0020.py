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
Case Name   : 查看参数recovery_parallelism，并尝试修改（只读参数）
Description :
    1、查看recovery_parallelism默认值；
    show recovery_parallelism;
    2、修改recovery_parallelism为正常值4,校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "recovery_parallelism=4";
Expect      :
    1、显示默认值；
    2、参数修改失败；
History     :
"""

import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')

class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0020开始执行-----------------------------")
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.stopstartCmd = f'source {macro.DB_ENV_PATH};gs_om -t stop && gs_om -t start'
        self.statusCmd = f'source {macro.DB_ENV_PATH};gs_om -t status --detail'

    def test_common_user_permission(self):
        logger.info("------------------------查询recovery_parallelism 期望：默认值4---------------------------")
        sql_cmd = commonsh.execut_db_sql(f'''show recovery_parallelism;''')
        logger.info(sql_cmd)
        self.assertIn("4", sql_cmd)

        logger.info("-----------修改recovery_parallelism为正常值4,校验其预期结果；-------------")
        logger.info("-----------期望：设置失败-------------")
        sql_cmd = '''source ''' + self.DB_ENV_PATH + f''';gs_guc reload -D {self.DB_INSTANCE_PATH} -c "recovery_parallelism=4"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)

    def tearDown(self):
        logger.info("--------------------------------恢复默认值-----------------------------------")
        commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'recovery_parallelism=4')
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0020执行结束---------------------------")