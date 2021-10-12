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
Case Name   : 修改remote_read_mode，观察预期结果；
Description :
    1、查询remote_read_mode默认值,show remote_read_mode;
    2、修改remote_read_mode为其他有效值off / non_authentication，
       gs_guc set -D {cluster/dn1} -c "remote_read_mode=off"
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功；
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0054开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.show_cmd = 'show remote_read_mode'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询remote_read_mode,默认值为authentication======")
        cmd1 = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(cmd1)
        self.assertEqual("authentication", cmd1.split("\n")[-2].strip())

        logger.info("======修改remote_read_mode为off，期望：修改成功======")
        res1 = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "remote_read_mode = off")
        self.assertTrue(res1)

        logger.info("======查询修改后的参数是否成功======")
        self.comsh.restart_db_cluster()
        cmd2 = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(cmd2)
        self.assertEqual("off", cmd2.split("\n")[-2].strip())

        logger.info("====修改remote_read_mode为non_authentication，期望：修改成功====")
        res2 = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "remote_read_mode=non_authentication")
        self.assertTrue(res2)

        logger.info("======查询修改后的参数是否成功======")
        self.comsh.restart_db_cluster()
        cmd3 = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(cmd3)
        self.assertEqual("non_authentication", cmd3.split("\n")[-2].strip())

    def tearDown(self):
        logger.info("======恢复配置======")
        cmd4 = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(cmd4)
        if 'authentication' != cmd4.split('\n')[-2].strip():
            self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                    "remote_read_mode = authentication")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0054执行结束===")
