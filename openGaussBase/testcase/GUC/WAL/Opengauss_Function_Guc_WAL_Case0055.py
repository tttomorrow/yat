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
Case Name   : 修改参数incremental_checkpoint_timeout为其他数据类型及超边界值，并校验其预期结果。
Description :
    1、查看incremental_checkpoint_timeout默认值 期望：1min；
    show incremental_checkpoint_timeout;
    gs_guc set -D {cluster/dn1} -c "incremental_checkpoint_timeout=test";
    gs_guc set -D {cluster/dn1} -c "incremental_checkpoint_timeout='test'";
    3、恢复默认值 无需恢复
Expect      :
    1、查看incremental_checkpoint_timeout默认值 期望：1min；
    3、恢复默认值 无需恢复
History     :
"""

import sys
import unittest
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')

class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0055开始执行-----------------------------")
        self.Constant = Constant()

    def test_guc_wal(self):
        logger.info("------------------------查询incremental_checkpoint_timeout 期望：默认值1min---------------------------")
        sql_cmd = commonsh.execut_db_sql(f'''show incremental_checkpoint_timeout;''')
        logger.info(sql_cmd)
        self.assertIn("1min", sql_cmd)

        logger.info("-----------修改incremental_checkpoint_timeout为test，期望：修改失败，show参数为默认值-------------")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, "incremental_checkpoint_timeout=test")
        self.assertFalse(result)
        sql_cmd = commonsh.execut_db_sql(f'''show incremental_checkpoint_timeout;''')
        logger.info(sql_cmd)
        self.assertIn("1min", sql_cmd)

        logger.info("-----------修改incremental_checkpoint_timeout为'test'，期望：修改失败，show参数为默认值-------------")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, "incremental_checkpoint_timeout='test'")
        self.assertFalse(result)
        sql_cmd = commonsh.execut_db_sql(f'''show incremental_checkpoint_timeout;''')
        logger.info(sql_cmd)
        self.assertIn("1min", sql_cmd)

        self.assertFalse(result)
        sql_cmd = commonsh.execut_db_sql(f'''show incremental_checkpoint_timeout;''')
        logger.info(sql_cmd)
        self.assertIn("1min", sql_cmd)

    def tearDown(self):
        logger.info("--------------------------------恢复默认值-----------------------------------")
        logger.info("恢复默认值")
        sql_cmd = commonsh.execut_db_sql(f'''show incremental_checkpoint_timeout;''')
        if "1min" not in sql_cmd:
            commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'incremental_checkpoint_timeout=1min')
            commonsh.restart_db_cluster()
            is_started = commonsh.get_db_cluster_status()
            self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0055执行结束---------------------------")