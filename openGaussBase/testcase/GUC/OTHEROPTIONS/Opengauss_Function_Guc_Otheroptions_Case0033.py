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
Case Name   : 修改ngram_punctuation_ignore为其他无效值，观察预期结果；
Description :
    1、查询ngram_punctuation_ignore默认值,show ngram_punctuation_ignore;
    2、set方式修改ngram_punctuation_ignore为其他无效值，字符串和空值;
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0033开始执行===")
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询ngram_punctuation_ignore期望，默认值on======")
        cmd = self.commonsh.execut_db_sql('''show ngram_punctuation_ignore;''')
        logger.info(cmd)
        self.assertEqual("on", cmd.split("\n")[-2].strip())

        logger.info("======修改ngram_punctuation_ignore为'test'，期望：设置失败======")
        res1 = self.commonsh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                          "ngram_punctuation_ignore='test'")
        self.assertFalse(res1)

        logger.info("======修改ngram_punctuation_ignore为''，期望：设置失败======")
        res2 = self.commonsh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                          "ngram_punctuation_ignore=''")
        self.assertFalse(res2)

    def tearDown(self):
        logger.info("======恢复默认值======")
        rec = self.commonsh.execut_db_sql('''show ngram_punctuation_ignore;''')
        logger.info(rec)
        if "on" not in rec.split('\n')[-2].strip():
            self.commonsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "ngram_punctuation_ignore = on")
            result = self.commonsh.restart_db_cluster()
            logger.info(result)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0033执行结束===")
