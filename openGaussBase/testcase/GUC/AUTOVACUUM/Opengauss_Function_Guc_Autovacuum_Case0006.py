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
Case Name   : 修改autoanalyze_timeout为其他数据类型，观察其预期结果；
Description :
            1、查询autoanalyze_timeout默认值；
            show autoanalyze_timeout；
            2、修改autoanalyze_timeout为'test'，观察预期结果；
            gs_guc set -D {cluster/dn1}  -c "autoanalyze_timeout='test'"
Expect      :
            1、显示默认值5min；
            2、修改autoanalyze_timeout失败，预期结果正常；
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
        LOGGER.info('==Guc_Autovacuum_Case0006开始执行==')
        self.constant = Constant()

        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("==查询autoanalyze_timeout 期望：默认值5min==")
        sql_cmd = COMMONSH.execut_db_sql('''show autoanalyze_timeout;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("5min", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("==修改autoanalyze_timeout为'test'，"
                    "期望：合理报错==")
        LOGGER.info("==期望：修改失败，show参数为默认值==")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            "autoanalyze_timeout='test'")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql('''show autoanalyze_timeout;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("5min", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('''show autoanalyze_timeout;''')
        if "5min" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                  "autoanalyze_timeout=300")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        sql_cmd = COMMONSH.execut_db_sql('''show autoanalyze_timeout;''')
        LOGGER.info(sql_cmd)
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertEqual("5min", sql_cmd.split("\n")[-2].strip())
        LOGGER.info("==Guc_Autovacuum_Case0006执行结束==")
