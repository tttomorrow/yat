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
Case Name   : 修改remote_read_mode为其他无效值，观察预期结果；
Description :
    1、查询remote_read_mode默认值,show remote_read_mode;
    2、修改remote_read_mode为其它无效值，
       gs_guc set -D {cluster/dn1} -c "remote_read_mode='test'"
    3、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改失败；
    3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0055开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询remote_read_mode,默认值为======")
        cmd1 = self.comsh.execut_db_sql('''show remote_read_mode;''')
        logger.info(cmd1)
        self.assertEqual("authentication", cmd1.split("\n")[-2].strip())

        logger.info("======修改remote_read_mode为test，期望：修改失败======")
        res1 = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "remote_read_mode = 'test'")
        self.assertFalse(res1)

        logger.info("======修改remote_read_mode为''，期望：修改失败======")
        res2 = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "remote_read_mode = ''")
        self.assertFalse(res2)

    def tearDown(self):
        logger.info("======恢复配置======")
        cmd2 = self.comsh.execut_db_sql('''show remote_read_mode;''')
        logger.info(cmd2)
        if 'authentication' != cmd2.split('\n')[-2].strip():
            self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                    "remote_read_mode = authentication")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0055执行结束===")
