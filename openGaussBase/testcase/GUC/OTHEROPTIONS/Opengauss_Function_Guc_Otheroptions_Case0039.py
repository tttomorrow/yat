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
Case Name   : 修改table_skewness_warning_threshold为其他无效值，观察预期结果；
Description :
    1、查询table_skewness_warning_threshold默认值,
      show table_skewness_warning_threshold;
    2、修改table_skewness_warning_threshold为其它无效值，
       gs_guc set -D {cluster/dn1} -c "table_skewness_warning_threshold='t'"
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改失败；
    3、恢复默认值成功；
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0039开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.show_cmd = 'show table_skewness_warning_threshold;'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询table_skewness_warning_threshold,默认值为1======")
        sql_cmd = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(sql_cmd)
        self.assertEqual("1", sql_cmd.split("\n")[-2].strip())

        logger.info("=====修改table_skewness_warning_threshold为t，期望：修改失败=====")
        re = self.comsh.execute_gsguc('set',
                                      self.constant.GSGUC_SUCCESS_MSG,
                                     "table_skewness_warning_threshold = 't'")
        self.assertFalse(re)

    def tearDown(self):
        logger.info("======恢复配置======")
        sql_cmd = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(sql_cmd)
        if '1' not in sql_cmd.split('\n')[-2].strip():
            self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                    "table_skewness_warning_threshold = 1")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0039执行结束===")
