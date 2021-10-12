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
Case Name   : 修改ngram_gram_size为其他无效值，观察预期结果；
Description :
    1、查询ngram_gram_size默认值,show ngram_gram_size;
    2、set方式修改ngram_gram_size为其他无效值，字符串和空值;
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
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0029开始执行===")
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询ngram_gram_size期望，默认值2======")
        sql_cmd1 = self.commonsh.execut_db_sql('''show ngram_gram_size;''')
        logger.info(sql_cmd1)
        self.assertEqual("2", sql_cmd1.split("\n")[-2].strip())

        logger.info("======修改ngram_gram_size为'test'，期望：设置失败======")
        result1 = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                             "ngram_gram_size='test'")
        self.assertFalse(result1)

        logger.info("======修改ngram_gram_size为''，期望：设置失败======")
        result2 = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                             "ngram_gram_size=''")
        self.assertFalse(result2)

        logger.info("======恢复默认值======")
        res_set = self.commonsh.execut_db_sql('''set ngram_gram_size to 2;''')
        self.assertIn(self.constant.SET_SUCCESS_MSG, res_set)

    def tearDown(self):
        logger.info("======恢复默认值======")
        sql_cmd3 = self.commonsh.execut_db_sql('''show ngram_gram_size;''')
        logger.info(sql_cmd3)
        if "2" not in sql_cmd3.split('\n')[-2].strip():
            self.commonsh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "ngram_gram_size=2")
            result3 = self.commonsh.restart_db_cluster()
            logger.info(result3)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0029执行结束===")
