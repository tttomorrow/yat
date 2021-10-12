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
Case Name   : 修改autovacuum_mode为其他数据类型，观察其预期结果；
Description :
            1、查询autovacuum_mode默认值；
            show autovacuum_mode；
            gs_guc set -D {cluster/dn1}  -c "autovacuum_mode='test'"
Expect      :
            1、显示默认值；
            2、修改autovacuum_mode失败，预期结果正常；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):
    def setUp(self):
        LOGGER.info('==Guc_Autovacuum_Case0004开始执行==')
        self.constant = Constant()

        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("==查询autovacuum_mode 期望：默认值mix==")
        sql_cmd = COMMONSH.execut_db_sql('''show autovacuum_mode;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("mix", sql_cmd.split("\n")[-2].strip())

                    "期望：合理报错==")
        LOGGER.info("==期望：修改失败，show参数为默认值==")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql('''show autovacuum_mode;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("mix", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("==修改autovacuum_mode为'test'，期望：合理报错==")
        LOGGER.info("==期望：修改失败，show参数为默认值==")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            "autovacuum_mode='test'")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql('''show autovacuum_mode;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("mix", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('''show autovacuum_mode;''')
        if "mix" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                  'autovacuum_mode=mix')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Guc_Autovacuum_Case0004执行结束==")
