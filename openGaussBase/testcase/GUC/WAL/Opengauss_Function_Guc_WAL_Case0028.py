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
Case Name   : 修改enable_incremental_checkpoint为off，观察预期结果；
Description :
    1、查询enable_incremental_checkpoint默认值；
    show enable_incremental_checkpoint;
    2、修改enable_incremental_checkpoint为off.重启使其生效，建立mot表，观察预期结果。
    gs_guc set -D /openGauss/zyn_gauss922/cluster/dn1 -c "enable_incremental_checkpoint=off"
    drop FOREIGN table if exists test cascade;create FOREIGN table test(x int);
    3、恢复默认值；
Expect      :
    1、查询默认值成功；
    2、修改参数成功，因mot表只支持增量检查点关闭状态下建表，此时建表成功，预期结果正常；
    3、恢复默认值成功；
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
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0028开始执行-----------------------------")
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.stopstartCmd = f'source {macro.DB_ENV_PATH};gs_om -t stop && gs_om -t start'
        self.statusCmd = f'source {macro.DB_ENV_PATH};gs_om -t status --detail'

    def test_guc_wal(self):
        logger.info("查询enable_incremental_checkpoint 期望：默认值on")
        sql_cmd = commonsh.execut_db_sql(f'''show enable_incremental_checkpoint;''')
        logger.info(sql_cmd)
        self.value = sql_cmd.splitlines()[-2].strip()

        logger.info("方式一修改enable_incremental_checkpoint为off，重启使其生效，期望：设置成功")
        sql_cmd = f'''source {self.DB_ENV_PATH};gs_guc set -D {self.DB_INSTANCE_PATH} -c "enable_incremental_checkpoint=off"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info("期望：重启后查询结果为off")
        msg = self.userNode.sh(self.stopstartCmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.START_SUCCESS_MSG, msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)
        status = self.userNode.sh(self.statusCmd).result()
        logger.info(status)
        sql_cmd = commonsh.execut_db_sql(f'''show enable_incremental_checkpoint;''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.CLOSE_STATUS_MSG[0], sql_cmd)

        logger.info("创建表，期望：创建成功")
        sql_cmd = commonsh.execut_db_sql(f'''drop FOREIGN table if exists test cascade;create FOREIGN table test(x int);''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn(self.Constant.CREATE_FOREIGN_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        logger.info("删除表")
        sql_cmd = commonsh.execut_db_sql(f'''drop FOREIGN table test cascade;''')
        logger.info(sql_cmd)
        logger.info("恢复默认值")
        commonsh.execute_gsguc('set', 
                               self.Constant.GSGUC_SUCCESS_MSG, 
                               f'enable_incremental_checkpoint={self.value}')
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0028执行结束---------------------------")