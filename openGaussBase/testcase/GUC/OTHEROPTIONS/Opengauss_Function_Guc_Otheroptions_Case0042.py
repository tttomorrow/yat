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
Case Name   : 修改datanode_heartbeat_interval，观察预期结果；
Description :
    1、查询datanode_heartbeat_interval默认值,show datanode_heartbeat_interval;
    2、修改datanode_heartbeat_interval为3s，
    gs_guc set -D {cluster/dn1} -c "datanode_heartbeat_interval=3s"
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0042开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询datanode_heartbeat_interval,默认值为1s======")
        cmd1 = self.comsh.execut_db_sql('''show datanode_heartbeat_interval;''')
        logger.info(cmd1)
        self.assertEqual("1s", cmd1.split("\n")[-2].strip())

        logger.info("======修改datanode_heartbeat_interval为3s，期望：修改成功======")
        res = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      "datanode_heartbeat_interval = 3s")
        self.assertTrue(res)

        logger.info("======查询修改后的参数是否生效======")
        self.comsh.restart_db_cluster()
        cmd2 = self.comsh.execut_db_sql('''show datanode_heartbeat_interval;''')
        logger.info(cmd2)
        self.assertEqual("3s", cmd2.split("\n")[-2].strip())

    def tearDown(self):
        logger.info("======恢复配置======")
        cmd3 = self.comsh.execut_db_sql('''show datanode_heartbeat_interval;''')
        logger.info(cmd3)
        if '1s' not in cmd3.split('\n')[-2].strip():
            self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                    "datanode_heartbeat_interval = 1s")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0042执行结束===")
