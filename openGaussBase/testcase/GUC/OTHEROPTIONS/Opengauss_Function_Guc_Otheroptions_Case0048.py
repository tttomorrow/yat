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
Case Name   : 修改pagewriter_thread_num，观察预期结果；
Description :
    1、查询pagewriter_thread_num默认值,show pagewriter_thread_num;
    2、修改pagewriter_thread_num为其他有效值8，
       gs_guc set -D {cluster/dn1} -c "pagewriter_thread_num=8"
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0048开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.show_cmd = 'show pagewriter_thread_num'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询pagewriter_thread_num,默认值为2======")
        cmd1 = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(cmd1)
        self.assertEqual("2", cmd1.split("\n")[-2].strip())

        logger.info("======修改pagewriter_thread_num为8，期望：修改成功======")
        res = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      "pagewriter_thread_num = 8")
        self.assertTrue(res)

        logger.info("======查询修改后的参数是否生效======")
        self.comsh.restart_db_cluster()
        cmd2 = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(cmd2)
        self.assertEqual("8", cmd2.split("\n")[-2].strip())

    def tearDown(self):
        logger.info("======恢复配置======")
        cmd3 = self.comsh.execut_db_sql(self.show_cmd)
        logger.info(cmd3)
        if '2' not in cmd3.split('\n')[-2].strip():
            self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                    "pagewriter_thread_num = 2")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0048执行结束===")
