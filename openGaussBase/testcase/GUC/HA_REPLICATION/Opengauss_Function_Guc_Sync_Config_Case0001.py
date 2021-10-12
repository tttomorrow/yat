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
Case Name   : 修改参数sync_config_strategy为合法值，并校验其预期结果
Description :
    1、查看sync_config_strategy的默认值
    show sync_config_strategy
    2、修改sync_config_strategy为合法值
    gs_guc set -D {cluster/dn1} -c "sync_config_strategy='none_node'"
    gs_guc set -D {cluster/dn1} -c "sync_config_strategy='all_node'"
    gs_guc set -D {cluster/dn1} -c "sync_config_strategy='only_sync_node'"
    3、恢复默认值
Expect      :
    1、查看sync_config_strategy的默认值为all_node
    2、三次修改均成功
    3、恢复默认值成功
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
executor = CommonSH('PrimaryDbUser')


class PrivateGrant(unittest.TestCase):

    def setUp(self):
        status = executor.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        logger.info("---OpenGauss_Function_Guc_Sync_Config_Case0001 start---")
        self.Constant = Constant()

    def test_guc_sync_config(self):
        logger.info("---show sync_config_strategy default value---")
        sql_result = executor.execut_db_sql(f'''show sync_config_strategy;''')
        logger.info(sql_result)
        self.assertIn("all_node", sql_result)

        logger.info("---modify sync_config_strategy to valid value---")
        logger.info("---modify sync_config_strategy to none_node---")
        guc_result = executor.execute_gsguc('set',
                                            self.Constant.GSGUC_SUCCESS_MSG,
                                           "sync_config_strategy='none_node'")
        self.assertTrue(guc_result)
        restart_status = executor.restart_db_cluster()
        self.assertTrue(restart_status)
        sql_result = executor.execut_db_sql(f'''show sync_config_strategy;''')
        logger.info(sql_result)
        self.assertIn("none_node", sql_result)

        logger.info("---modify sync_config_strategy to only_sync_node---")
        guc_result = executor.execute_gsguc('set',
                                            self.Constant.GSGUC_SUCCESS_MSG,
                                           "sync_config_strategy="
                                           "'only_sync_node'")
        self.assertTrue(guc_result)
        restart_status = executor.restart_db_cluster()
        self.assertTrue(restart_status)
        sql_result = executor.execut_db_sql(f'''show sync_config_strategy;''')
        logger.info(sql_result)
        self.assertIn("only_sync_node", sql_result)

        logger.info("---modify sync_config_strategy to all_node---")
        guc_result = executor.execute_gsguc('set',
                                            self.Constant.GSGUC_SUCCESS_MSG,
                                           "sync_config_strategy='all_node'")
        self.assertTrue(guc_result)
        restart_status = executor.restart_db_cluster()
        self.assertTrue(restart_status)
        sql_result = executor.execut_db_sql(f'''show sync_config_strategy;''')
        logger.info(sql_result)
        self.assertIn("all_node", sql_result)

    def tearDown(self):
        logger.info("---modify sync_config_strategy to default value---")
        sql_result = executor.execut_db_sql(f'''show sync_config_strategy;''')
        param_value = sql_result.split("\n")[-2].strip()
        if "all_node" != param_value:
            _ = executor.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG,
                                      "sync_config_strategy='all_node'")
            _ = executor.restart_db_cluster()
        status = executor.get_db_cluster_status()
        check_status = executor.execute_gsguc('check', 'all_node',
                                             'sync_config_strategy')
        self.assertTrue("Normal" in status)
        self.assertTrue(check_status)
        logger.info("---OpenGauss_Function_Guc_Sync_Config_Case0001 finish---")
