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
Case Name   : 修改dirty_page_percent_max为其他无效值，观察预期结果；
Description :
    1、查询dirty_page_percent_max默认值,show dirty_page_percent_max;
    2、修改dirty_page_percent_max为其它无效值，
       gs_guc set -D {cluster/dn1} -c "dirty_page_percent_max='test'"
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0051开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询dirty_page_percent_max,默认值为0.9======")
        cmd1 = self.comsh.execut_db_sql('''show dirty_page_percent_max;''')
        logger.info(cmd1)
        self.assertEqual("0.9", cmd1.split("\n")[-2].strip())

        logger.info("======修改dirty_page_percent_max为test，期望：修改失败======")
        res1 = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "dirty_page_percent_max = 'test'")
        self.assertFalse(res1)

        logger.info("======修改dirty_page_percent_max为''，期望：修改失败======")
        res2 = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "dirty_page_percent_max = ''")
        self.assertFalse(res2)

        logger.info("======修改dirty_page_percent_max为10，期望：修改失败======")
        res3 = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "dirty_page_percent_max = 10")
        self.assertFalse(res3)

    def tearDown(self):
        logger.info("======恢复配置======")
        cmd2 = self.comsh.execut_db_sql('''show dirty_page_percent_max;''')
        logger.info(cmd2)
        if '0.9' not in cmd2.split('\n')[-2].strip():
            self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                    "dirty_page_percent_max = 0.9")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0051执行结束===")
