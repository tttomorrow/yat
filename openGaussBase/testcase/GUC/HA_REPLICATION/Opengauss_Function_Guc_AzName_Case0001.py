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
Case Name   : 修改参数available_zone为合法值，并校验其预期结果
Description :
    1、查看数据库available_zone的初始值
    show available_zone
    2、修改available_zone为合法值
    gs_guc set -D {cluster/dn1} -c "available_zone='AZ10'"
    gs_guc set -D {cluster/dn1} -c "available_zone='001'"
    3、恢复初始值
Expect      :
    1、查看available_zone的初始值成功
    2、修改available_zone成功
    3、恢复初始值成功
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
executor = CommonSH('PrimaryDbUser')


class PrivateGrant(unittest.TestCase):

    def setUp(self):
        status = executor.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        logger.info("---OpenGauss_Function_Guc_AzName_Case0001 start---")
        self.Constant = Constant()
        logger.info("---show available_zone default value---")
        sql_result = executor.execut_db_sql(f'''show available_zone;''')
        logger.info(sql_result)
        self.assertIn("available_zone", sql_result)
        self.default_value = sql_result.split("\n")[-2].strip()
        logger.info("default value of available_zone in this machine is '%s'"
                    % self.default_value)

    def test_guc_az_name(self):
        logger.info("---modify available_zone to valid value---")
        logger.info("---modify available_zone to AZ10---")
        guc_result = executor.execute_gsguc('set',
                                            self.Constant.GSGUC_SUCCESS_MSG,
                                           "available_zone='AZ10'")
        self.assertTrue(guc_result)
        restart_status = executor.restart_db_cluster()
        self.assertTrue(restart_status)
        sql_result = executor.execut_db_sql(f'''show available_zone;''')
        logger.info(sql_result)
        self.assertIn("AZ10", sql_result)

        logger.info("---modify available_zone to 001---")
        guc_result = executor.execute_gsguc('set',
                                            self.Constant.GSGUC_SUCCESS_MSG,
                                           "available_zone='001'")
        self.assertTrue(guc_result)
        restart_status = executor.restart_db_cluster()
        self.assertTrue(restart_status)
        sql_result = executor.execut_db_sql(f'''show available_zone;''')
        logger.info(sql_result)
        self.assertIn("001", sql_result)

    def tearDown(self):
        logger.info("---tearDown: modify available_zone to default value---")
        sql_result = executor.execut_db_sql(f'''show available_zone;''')
        param_value = sql_result.split("\n")[-2].strip()
        if self.default_value != param_value:
            _ = executor.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG,
                                      "available_zone='%s'" %
                                       self.default_value)
            _ = executor.restart_db_cluster()
        status = executor.get_db_cluster_status()
        check_status = executor.execute_gsguc('check', self.default_value,
                                             'available_zone')
        self.assertTrue("Normal" in status)
        self.assertTrue(check_status)
        logger.info("---OpenGauss_Function_Guc_AzName_Case0001 finish---")
