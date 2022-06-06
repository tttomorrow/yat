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
Case Name   : 修改transparent_encrypt_kms_url为其他无效值，观察预期结果；
Description :
    1、查询transparent_encrypt_kms_url默认值,show transparent_encrypt_kms_url;
    2、set方式修改transparent_encrypt_kms_url为其他无效值，字符串;
    3、恢复默认值；
Expect      :
    1、显示默认值为空；
    2、参数修改成功，重启失败；
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0034开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询transparent_encrypt_kms_url期望，默认值为空======")
        cmd = self.comsh.execut_db_sql('''show transparent_encrypt_kms_url;''')
        logger.info(cmd)
        self.assertEqual('', cmd.split("\n")[-2].strip())

        logger.info("====修改transparent_encrypt_kms_url为'^test^'，期望：重启失败====")
        res = self.comsh.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                      "transparent_encrypt_kms_url='^test^'")
        self.assertTrue(res)
        restart = self.comsh.restart_db_cluster()
        logger.info(restart)
        self.assertFalse(restart)

    def tearDown(self):
        logger.info("======恢复默认值======")
        self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                "transparent_encrypt_kms_url = ''")
        result = self.comsh.restart_db_cluster()
        logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0034执行结束===")
