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
Case Name   : 修改参数password_max_length为其他数据类型及超边界值，并校验其预期结果。
Description :
    1、查看password_max_length默认值 期望：32；
    show password_max_length;
    2、修改password_max_length为abc等，期望：合理报错
    gs_guc reload -D {cluster/dn1} -c "password_max_length='abc'";
    gs_guc reload -D {cluster/dn1} -c "password_max_length=-1";
    gs_guc reload -D {cluster/dn1} -c "password_max_length=1000";
    gs_guc reload -D {cluster/dn1} -c "password_max_length=''";
    gs_guc reload -D {cluster/dn1} -c "password_max_length=' '";
    gs_guc reload -D {cluster/dn1} -c "password_max_length=null";
    3、恢复默认值 无需恢复
Expect      :
    1、查看password_max_length默认值 期望：32；
    2、修改password_max_length为abc等，期望：合理报错
    3、恢复默认值 无需恢复
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")



class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0273"
            " start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc(self):
        LOGGER.info("步骤1：查询password_max_length 期望：默认值32")
        sql_cmd = COMMONSH.execut_db_sql("show password_max_length;")
        LOGGER.info(sql_cmd)
        self.assertEqual("32", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("步骤2:修改password_max_length为abc等，期望：修改失败，show参数为默认值")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "password_max_length='abc'")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show password_max_length;")
        LOGGER.info(sql_cmd)
        self.assertEqual("32", sql_cmd.split("\n")[-2].strip())
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "password_max_length=-1")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show password_max_length;")
        LOGGER.info(sql_cmd)
        self.assertEqual("32", sql_cmd.split("\n")[-2].strip())
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "password_max_length=1000")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show password_max_length;")
        LOGGER.info(sql_cmd)
        self.assertEqual("32", sql_cmd.split("\n")[-2].strip())
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "password_max_length=''")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show password_max_length;")
        LOGGER.info(sql_cmd)
        self.assertEqual("32", sql_cmd.split("\n")[-2].strip())
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "password_max_length=' '")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show password_max_length;")
        LOGGER.info(sql_cmd)
        self.assertEqual("32", sql_cmd.split("\n")[-2].strip())
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "password_max_length=null")
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql("show password_max_length;")
        LOGGER.info(sql_cmd)
        self.assertEqual("32", sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOGGER.info("步骤3:恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "password_max_length=32")
        LOGGER.info(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info(
            "==Opengauss_Function_Guc_Connectionauthentication_Case0273"
            " finish==")
