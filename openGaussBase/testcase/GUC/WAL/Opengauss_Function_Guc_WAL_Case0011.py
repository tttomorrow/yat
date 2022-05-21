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
Case Name   : 修改参数synchronous_commit为其他数据类型及超边界值
Description :
    1、查看synchronous_commit默认值 期望：off；
    show synchronous_commit;
    2、修改synchronous_commit为6666、'test'等，期望：合理报错
    gs_guc set -D {cluster/dn1} -c "synchronous_commit=6666";
    gs_guc set -D {cluster/dn1} -c "synchronous_commit=test";
    3、恢复默认值 无需恢复
Expect      :
    1、查看synchronous_commit默认值 期望：off；
    2、修改synchronous_commit为6666、'test'等，期望：合理报错
    3、恢复默认值
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("==Opengauss_Function_Guc_WAL_Case0011开始执行==")
        self.constant = Constant()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)

    def test_guc_wal(self):
        logger.info("==查询synchronous_commit 期望：默认值on==")
        sql_cmd = COMMONSH.execut_db_sql("show synchronous_commit;")
        logger.info(sql_cmd)
        self.default_result = sql_cmd.split("\n")[-2].strip()
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        logger.info("==修改synchronous_commit为6666、'test'等，"
                    "期望：合理报错==")
        logger.info("==修改synchronous_commit为'test'，"
                    "期望：修改失败，show参数为默认值==")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "synchronous_commit=6666")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show synchronous_commit;")
        logger.info(sql_cmd)
        self.assertEqual(f"{self.default_result}",
                         sql_cmd.split("\n")[-2].strip())
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        logger.info("==修改synchronous_commit为'test'，期望：修改失败==")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "synchronous_commit=test")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show synchronous_commit;")
        logger.info(sql_cmd)
        self.assertEqual(f"{self.default_result}",
                         sql_cmd.split("\n")[-2].strip())
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

    def tearDown(self):
        logger.info("==恢复默认值==")
        sql_cmd = COMMONSH.execut_db_sql("show synchronous_commit;")
        logger.info(sql_cmd)
        result = sql_cmd.split("\n")[-2].strip()
        if result != self.default_result:
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   f'synchronous_commit='
                                  f'{self.default_result}')
            COMMONSH.restart_db_cluster()
        is_started = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started)
        logger.info("==Opengauss_Function_Guc_WAL_Case0011执行结束==")
