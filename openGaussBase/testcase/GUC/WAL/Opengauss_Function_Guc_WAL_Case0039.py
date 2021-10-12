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
Case Name   : 修改参数wal_writer_delay为其他数据类型及超边界值，并校验其预期结果。
Description :
    1、查看wal_writer_delay默认值 期望：200ms；
    show wal_writer_delay;
    gs_guc set -D {cluster/dn1} -c "wal_writer_delay=test";
    gs_guc set -D {cluster/dn1} -c "wal_writer_delay='test'";
    3、恢复默认值 无需恢复
Expect      :
    1、查看wal_writer_delay默认值 期望：200ms；
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
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0039开始执行-----------------------------")
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.stopstartCmd = f'source {macro.DB_ENV_PATH};gs_om -t stop && gs_om -t start'
        self.statusCmd = f'source {macro.DB_ENV_PATH};gs_om -t status --detail'

    def test_guc_wal(self):
        logger.info("------------------------查询wal_writer_delay 期望：默认值200ms---------------------------")
        sql_cmd = commonsh.execut_db_sql(f'''show wal_writer_delay;''')
        logger.info(sql_cmd)
        self.assertIn("200ms", sql_cmd)

        logger.info("-----------修改wal_writer_delay为test，期望：修改失败，show参数为默认值-------------")
        sql_cmd = f'''source {self.DB_ENV_PATH};gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_writer_delay=test"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_writer_delay;''')
        logger.info(sql_cmd)
        self.assertIn("200ms", sql_cmd)

        logger.info("-----------修改wal_writer_delay为'test'，期望：修改失败，show参数为默认值-------------")
        sql_cmd = f'''source {self.DB_ENV_PATH};gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_writer_delay='test'"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_writer_delay;''')
        logger.info(sql_cmd)
        self.assertIn("200ms", sql_cmd)

        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)
        sql_cmd = commonsh.execut_db_sql(f'''show wal_writer_delay;''')
        logger.info(sql_cmd)
        self.assertIn("200ms", sql_cmd)

    def tearDown(self):
        logger.info("--------------------------------恢复默认值-----------------------------------")
        commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'wal_writer_delay=200ms')
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0039执行结束---------------------------")