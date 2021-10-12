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
Case Name   : 修改参数wal_level为其他数据类型及超边界值，并校验其预期结果。
Description :
    1、查看wal_level默认值 期望：hot_standby；
    show wal_level;
    2、修改wal_level为6666、'test'、false等，期望：合理报错
    gs_guc set -D {cluster/dn1} -c "wal_level=6666";
    gs_guc set -D {cluster/dn1} -c "wal_level=test";
    gs_guc set -D {cluster/dn1} -c "wal_level=false";
    3、恢复默认值 无需恢复
Expect      :
    1、查看wal_level默认值 期望：hot_standby；
    2、修改wal_level为6666、'test'、false等，期望：合理报错
    3、恢复默认值 无需恢复
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
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0005开始执行-----------------------------")
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.stopstartCmd = f'source {macro.DB_ENV_PATH};gs_om -t stop && gs_om -t start'
        self.statusCmd = f'source {macro.DB_ENV_PATH};gs_om -t status --detail'

    def test_common_user_permission(self):
        logger.info("------------------------查询wal_level 期望：默认值hot_standby---------------------------")
        sql_cmd = commonsh.execut_db_sql(f'''show wal_level;''')
        logger.info(sql_cmd)
        self.assertIn("hot_standby", sql_cmd)

        logger.info("-----------修改wal_level为6666、'test'、false等，期望：合理报错-------------")
        logger.info("-----------修改wal_level为'test'，期望：修改失败，show参数为默认值-------------")
        sql_cmd = f'''source {self.DB_ENV_PATH};gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_level=6666"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_level;''')
        logger.info(sql_cmd)
        self.assertIn("hot_standby", sql_cmd)

        logger.info("-----------修改wal_level为'test'，期望：修改失败，show参数为默认值-------------")
        sql_cmd = f'''source {self.DB_ENV_PATH};gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_level='test'"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_level;''')
        logger.info(sql_cmd)
        self.assertIn("hot_standby", sql_cmd)

        logger.info("-----------修改wal_level为false，期望：修改失败，show参数为默认值-------------")
        sql_cmd = f'''source {self.DB_ENV_PATH};gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_level=false"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_level;''')
        logger.info(sql_cmd)
        self.assertIn("hot_standby", sql_cmd)

    def tearDown(self):
        logger.info("--------------------------------恢复默认值-----------------------------------")
        commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'wal_level=hot_standby')
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0005执行结束---------------------------")