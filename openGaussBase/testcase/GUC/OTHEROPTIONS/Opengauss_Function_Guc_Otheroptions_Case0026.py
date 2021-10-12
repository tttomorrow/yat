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
Case Name   : 使用set方式修改job_queue_processes为100，观察预期结果；
Description :
    1、查询job_queue_processes默认值,show job_queue_processes;
    2、使用set方式修改job_queue_processes为100，set job_queue_processes to 100;
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0026开始执行===")
        self.Constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询job_queue_processes期望，默认值10======")
        sql_cmd = self.commonsh.execut_db_sql('''show job_queue_processes;''')
        logger.info(sql_cmd)
        self.assertEqual("10", sql_cmd.split("\n")[-2].strip())

        logger.info("======修改job_queue_processes为100，期望：设置失败======")
        res = self.commonsh.execut_db_sql('''set job_queue_processes to 100;''')
        self.assertIn('cannot be changed', res)

    def tearDown(self):
        logger.info("======恢复默认值======")
        sql_cmd = self.commonsh.execut_db_sql('''show job_queue_processes; ''')
        logger.info(sql_cmd)
        if "10" not in sql_cmd:
            self.commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG,
                                       "job_queue_processes=10")
            result = self.commonsh.restart_db_cluster()
            logger.info(result)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0026执行结束===")
