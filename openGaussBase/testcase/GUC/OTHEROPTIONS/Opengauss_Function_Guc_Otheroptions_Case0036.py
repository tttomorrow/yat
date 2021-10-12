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
Case Name   : 设置behavior_compat_options为有效值，观察预期结果；
Description :
    1、查询behavior_compat_options默认值,show behavior_compat_options;
    2、查看未配置项，执行相关行为，观察预期结果;
    3、使用gs_guc set方式，配置多个兼容性配置项，
       display_leading_zero,end_month_calculate,return_null_string;
    4、查看配置项，执行相关行为，观察预期结果;
    5、恢复默认值；
Expect      :
    1、显示默认值为空；
    2、执行相关行为，预期正确；
    3、设置成功；
    4、执行相关行为，预期正确；
    5、恢复默认值成功；
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0036开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======步骤1：查询behavior_compat_options期望，默认值为空======")
        cmd1 = self.comsh.execut_db_sql('''show behavior_compat_options;''')
        logger.info(cmd1)
        self.assertIn('', cmd1.split("\n")[-2].strip())

        logger.info("======步骤2：查看未配置相关参数，执行相关语句的行为，符合预期======")
        logger.info("===配置项:display_leading_zero，查看浮点数显示，不显示小数点前0===")
        sql_res1 = self.comsh.execut_db_sql('''select 0.25;''')
        logger.info(sql_res1)
        self.assertEqual('.25', sql_res1.split('\n')[-2].strip())

        logger.info("===配置项:end_month_calculate，add_months函数计算逻辑,日期一致===")
        sql_res2 = self.comsh.execut_db_sql('''select 
            add_months('2021-02-28',3);''')
        logger.info(sql_res2)
        self.assertIn('2021-05-28', sql_res2)

        logger.info("配置项:return_null_string,函数lpad()和rpad()结果为空字符串''的显示为空")
        sql_res3 = self.comsh.execut_db_sql('''select 
            length(lpad('123',0,'*'));''')
        logger.info(sql_res3)
        self.assertIn('', sql_res3.split('\n')[-2])

        logger.info("======步骤3：使用gs_guc set方式，配置以上多个兼容性配置项======")
        set_res = self.comsh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          "behavior_compat_options = "
                                          "'display_leading_zero,"
                                          "end_month_calculate,"
                                          "return_null_string'")
        logger.info(set_res)
        self.assertTrue(set_res)
        restart = self.comsh.restart_db_cluster()
        logger.info(restart)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        logger.info("======步骤4：查看配置相关参数后，执行相关语句的行为，符合预期======")
        logger.info("======配置项:display_leading_zero，查看浮点数显示，显示小数点前0======")
        sql_res4 = self.comsh.execut_db_sql('''select 0.25;''')
        logger.info(sql_res4)
        self.assertEqual('0.25', sql_res4.split('\n')[-2].strip())

        logger.info("===配置项:end_month_calculate，add_months函数计算逻辑,和月末日期一致===")
        sql_res5 = self.comsh.execut_db_sql('''select 
            add_months('2021-02-28',3);''')
        logger.info(sql_res5)
        self.assertIn('2021-05-31', sql_res5)

        logger.info("配置项:return_null_string,函数lpad()和rpad()结果为空字符串''的显示为0")
        sql_res6 = self.comsh.execut_db_sql('''select 
            length(lpad('123',0,'*'));''')
        logger.info(sql_res6)
        self.assertEqual('0', sql_res6.split('\n')[-2].strip())

    def tearDown(self):
        logger.info("======步骤5：恢复默认值======")
        rec = self.comsh.execut_db_sql('''show behavior_compat_options;''')
        logger.info(rec)
        if rec.split('\n')[-2].strip() != '':
            self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                    "behavior_compat_options = ''")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0036执行结束===")
