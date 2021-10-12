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
Case Name   : 设置max_active_global_temporary_table为其他无效值，观察预期结果
Description :
    1、查询max_active_global_temporary_table默认值
       show max_active_global_temporary_table;
    2、设置max_active_global_temporary_table为'test'、10000001、-10,
       gs_guc set -D {cluster/dn1} -c "max_active_global_temporary_table=无效值"
    3、恢复默认值;
Expect      :
    1、显示默认值，1000;
    2、参数修改失败;
    3、恢复默认值成功;
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("===Opengauss_Function_Guc_Globaltemptab_Case0005开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.table = 'test'
        self.config_param = 'show max_active_global_temporary_table;'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("====查询max_active_global_temporary_table期望，默认值1000====")
        sql_cmd1 = self.comsh.execut_db_sql(self.config_param)
        logger.info(sql_cmd1)
        self.assertEqual('1000', sql_cmd1.splitlines()[-2].strip())

        logger.info("===修改max_active_global_temporary_table为test，期望：设置失败===")
        res1 = self.comsh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "max_active_global_temporary_table="
                                        "'test'")
        self.assertFalse(res1)

        res2 = self.comsh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "max_active_global_temporary_table="
                                        "10000001")
        self.assertFalse(res2)

        logger.info("===修改max_active_global_temporary_table为-20，期望：设置失败===")
        res3 = self.comsh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "max_active_global_temporary_table="
                                        "-20")
        self.assertFalse(res3)

    def tearDown(self):
        logger.info("======清理环境，恢复默认值======")
        sql_cmd = self.comsh.execut_db_sql(self.config_param)
        logger.info(sql_cmd)
        if '1000' not in sql_cmd.splitlines()[-2].strip():
            self.comsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "max_active_global_temporary_table=1000")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Globaltemptab_Case0005执行结束===")
