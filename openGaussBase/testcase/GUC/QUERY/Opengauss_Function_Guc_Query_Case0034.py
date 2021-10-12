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
Case Name   : 参数unique_sql_clean_ratio无效值测试
Description :
    1、查询参数默认值；
    show unique_sql_clean_ratio;
    show enable_auto_clean_unique_sql;
    2、修改unique_sql_clean_ratio为无效值，重启数据库，并校验其预期结果；
    list = [-1, 0.21, 'test', false, true, '', ' ', null, 21%, 20%, 15%, 10%]
    for num in list:
        gs_guc set -N all -I all -c "unique_sql_clean_ratio={num}"
        gs_om -t stop && gs_om -t start
        show unique_sql_clean_ratio;
    3、修改enable_auto_clean_unique_sql为无效值，重启数据库，并校验其预期结果；
    list = [0.21, 'test', '', ' ', null]
    for num in list:
        gs_guc set -N all -I all -c "enable_auto_clean_unique_sql={num}"
        gs_om -t stop && gs_om -t start
        show unique_sql_clean_ratio;
    4、恢复默认值；
    gs_guc set -N all -I all -c "enable_auto_clean_unique_sql=off"
    gs_guc set -N all -I all -c "unique_sql_clean_ratio=0"
    gs_om -t stop && gs_om -t start
Expect      :
    1、显示默认值；
    2、参数修改失败 重启失败 合理报错
    3、参数修改失败 重启失败 合理报错
    4、恢复默认值成功；
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
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0034 start==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_unique_sql(self):
        LOGGER.info("步骤1：查询参数默认值")
        result = COMMONSH.execut_db_sql("show unique_sql_clean_ratio")
        LOGGER.info(result)
        self.assertEqual("0.1", result.split("\n")[-2].strip())
        result = COMMONSH.execut_db_sql("show enable_auto_clean_unique_sql")
        LOGGER.info(result)
        self.assertEqual("off", result.split("\n")[-2].strip())

        LOGGER.info("步骤2：修改unique_sql_clean_ratio为无效值")
        temp_list = [-1, 0.21, "'test'", 'false', 'true', "''", "' '",
                     'null', '21%', '20%', '15%', '10%']
        for con in temp_list:
            result = COMMONSH.execute_gsguc("reload",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"unique_sql_clean_ratio={con}")
            LOGGER.info(result)
            self.assertFalse(result)
            result = COMMONSH.execut_db_sql("show unique_sql_clean_ratio")
            LOGGER.info(result)
            self.assertEqual("0.1", result.split("\n")[-2].strip())

        LOGGER.info("步骤3：修改enable_auto_clean_unique_sql为无效值")
        temp_list = [0.21, "'test'", "''", "' '", 'null']
        for con in temp_list:
            result = COMMONSH.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"enable_auto_clean_unique_sql"
                                            f"={con}")
            LOGGER.info(result)
            self.assertFalse(result)

    def tearDown(self):
        LOGGER.info("步骤4：恢复默认值")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"unique_sql_clean_ratio=0.1")
        LOGGER.info(result)
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"enable_auto_clean_unique_sql=off")
        LOGGER.info(result)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0034 finish=")
