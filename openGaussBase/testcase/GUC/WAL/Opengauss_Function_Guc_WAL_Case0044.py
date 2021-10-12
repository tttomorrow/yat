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
Case Name   : 修改checkpoint_timeout为20min，观察预期结果；
Description :
    1、查询checkpoint_timeout默认值；
    show checkpoint_timeout;
    2、修改checkpoint_timeout为20min，重启使其生效，并校验其预期结果；
    gs_guc set -D /openGauss/zyn1026_gauss/cluster/dn1 -c "checkpoint_timeout=20min"
    gs_om -t stop && gs_om -t start
    show checkpoint_timeout;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为20min；
    3、DML无报错
    4、恢复默认值成功；
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
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0044开始执行-----------------------------")
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.stopstartCmd = f'source {macro.DB_ENV_PATH};gs_om -t stop && gs_om -t start'
        self.statusCmd = f'source {macro.DB_ENV_PATH};gs_om -t status --detail'

    def test_guc_wal(self):
        logger.info("查询checkpoint_timeout 期望：默认值15min")
        sql_cmd = commonsh.execut_db_sql(f'''show checkpoint_timeout;''')
        logger.info(sql_cmd)
        self.assertIn("15min", sql_cmd)

        logger.info("方式一修改checkpoint_timeout为20min，重启使其生效，期望：设置成功")
        sql_cmd = f'''source {self.DB_ENV_PATH};gs_guc set -D {self.DB_INSTANCE_PATH} -c "checkpoint_timeout=20min"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info("期望：重启后查询结果为20min")
        msg = self.userNode.sh(self.stopstartCmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.START_SUCCESS_MSG, msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        status = self.userNode.sh(self.statusCmd).result()
        logger.info(status)
        sql_cmd = commonsh.execut_db_sql(f'''show checkpoint_timeout;''')
        logger.info(sql_cmd)
        self.assertIn("20min", sql_cmd)

        logger.info("创建表，期望：创建成功")
        sql_cmd = commonsh.execut_db_sql(f'''drop table if exists test cascade;create table test(x int);''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_cmd)

    def tearDown(self):
        logger.info("删除表")
        sql_cmd = commonsh.execut_db_sql(f'''drop table test cascade;''')
        logger.info(sql_cmd)
        logger.info("恢复默认值")
        commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'checkpoint_timeout=15min')
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0044执行结束---------------------------")