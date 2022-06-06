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
Case Name   : 修改behavior_compat_options为其他无效值，观察预期结果；
Description :
    1、查询behavior_compat_options默认值,show behavior_compat_options;
    2、gs_guc set方式修改behavior_compat_options为其他无效值;
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，重启数据库失败；
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0037开始执行===")
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======步骤1：查询behavior_compat_options期望，默认值为空======")
        cmd = self.commonsh.execut_db_sql('''show behavior_compat_options;''')
        logger.info(cmd)
        self.assertIn('', cmd.split("\n")[-2].strip())

        logger.info("=====步骤2：修改behavior_compat_options为'test'，期望：重启失败=====")
        result = self.commonsh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            "behavior_compat_options='test'")
        self.assertTrue(result)
        restart = self.commonsh.restart_db_cluster()
        logger.info(restart)
        self.assertFalse(restart)

        logger.info("======步骤3：恢复默认值，重启数据库======")
        rec_res = self.commonsh.execute_gsguc('set',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             "behavior_compat_options = ''")
        logger.info(rec_res)
        self.assertTrue(rec_res)
        rec_restart = self.commonsh.restart_db_cluster()
        logger.info(rec_restart)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def tearDown(self):
        logger.info("======恢复默认值======")
        rec = self.commonsh.execut_db_sql('''show behavior_compat_options;''')
        logger.info(rec)
        if rec.split('\n')[-2].strip() != '':
            self.commonsh.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "behavior_compat_options = ''")
            result = self.commonsh.restart_db_cluster()
            logger.info(result)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0037执行结束===")
