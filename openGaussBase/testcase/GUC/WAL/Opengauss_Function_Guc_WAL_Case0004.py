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
Case Name   : 修改参数wal_level为minimal、archive、hot_standby，并校验其预期结果。
Description :
    1、查看wal_level默认值 期望：hot_standby；
    show wal_level;
    2、主备环境下修改参数wal_level为minimal，archive，logical 期望：logical重启成功，其他重启失败
    gs_guc set -D {cluster/dn1} -c "wal_level=minimal";
    gs_guc set -D {cluster/dn1} -c "wal_level=archive";
    gs_guc set -D {cluster/dn1} -c "wal_level=logical";
    3、恢复默认值 期望：hot_standby；
Expect      :
    1、查看wal_level默认值 期望：hot_standby；
    2、主备环境下修改参数wal_level为minimal，archive，logical 期望：logical重启成功，其他重启失败
    3、恢复默认值 期望：hot_standby；
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
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0004开始执行-----------------------------")
        self.Constant = Constant()
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        
    def test_common_user_permission(self):
        logger.info("------------------------查询wal_level 期望：默认值hot_standby---------------------------")
        sql_cmd = commonsh.execut_db_sql(f'''show wal_level;''')
        logger.info(sql_cmd)
        self.assertIn("hot_standby", sql_cmd)

        logger.info("-----------主备环境下修改参数wal_level为minimal，archive，logical 期望：logical重启成功，其他重启失败-------------")
        temp_list = ["minimal", "archive", "logical"]
        for case in temp_list:
            result = commonsh.execute_gsguc("set",
                                            self.Constant.GSGUC_SUCCESS_MSG,
                                            f"wal_level={case}")
            self.assertTrue(result)
            result = commonsh.restart_db_cluster()
            if case != "logical":
                logger.info("-----------期望：重启失败-----------")
                self.assertFalse(result)
            else:
                logger.info("-----------期望：重启成功-----------")
                is_started = commonsh.get_db_cluster_status()
                self.assertTrue("Degraded" in is_started
                                or "Normal" in is_started)

    def tearDown(self):
        logger.info("--------------------------------恢复默认值-----------------------------------")
        commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'wal_level=hot_standby')
        commonsh.restart_db_cluster()
        is_started = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0004执行结束---------------------------")