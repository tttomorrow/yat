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
Case Name   : 方式二修改track_function为pl，校验其预期结果
Description :
    步骤1:查询track_function默认值
    show track_function;
    步骤2:方式二修改track_function为pl，校验其预期结果
    gs_guc reload -N all -I all -c "track_function=pl"
    show track_function;
    查询pg_stat_user_functions视图为空
    步骤3:调用函数
    步骤4:恢复默认值
Expect      :
    步骤1:显示默认值none
    步骤2:参数修改成功，校验修改后参数值为pl，查询pg_stat_user_functions为空
    步骤3:调用函数无报错 查询pg_stat_user_functions不为空
    步骤4:恢复默认值成功
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0044"
            "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("步骤1:查询track_function默认值 期望：默认值none")
        sql_cmd = COMMONSH.execut_db_sql("show track_functions;")
        LOGGER.info(sql_cmd)
        self.assertEqual("none", sql_cmd.splitlines()[-2].strip())
        LOGGER.info("查询pg_stat_user_functions视图为空")
        sql_cmd = COMMONSH.execut_db_sql("select count(*) "
            "from pg_stat_user_functions;")
        LOGGER.info(sql_cmd)
        self.assertEqual(int(sql_cmd.splitlines()[-2].strip()), 0)

        LOGGER.info("步骤2:方式二修改track_function为pl，重启生效 期望成功")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_functions=pl")
        self.assertTrue(result)
        LOGGER.info("期望：查询结果为pl")
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)
        sql_cmd = COMMONSH.execut_db_sql("show track_functions;")
        LOGGER.info(sql_cmd)
        self.assertEqual("pl", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤3:调用函数 期望：执行成功")
        sql_cmd = COMMONSH.execut_db_sql('''drop function if exists \
            syn_fun_001(c int);
            create or replace function syn_fun_001(c int)return number
            as
                b int := c;
            begin
                for i in 1..c loop
                    b:= b - 1;
                end loop;
                return b;
            end;
            select syn_fun_001(5);
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        LOGGER.info("查询pg_stat_user_functions视图不为空")
        sql_cmd = COMMONSH.execut_db_sql("select count(*) "
            "from pg_stat_user_functions;")
        LOGGER.info(sql_cmd)
        self.assertGreater(int(sql_cmd.splitlines()[-2].strip()), 0)

        LOGGER.info("步骤4:恢复默认值")
        LOGGER.info("删除函数")
        sql_cmd = COMMONSH.execut_db_sql("drop function if exists "
            "syn_fun_001(c int);")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd)
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_functions='none'")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_functions;")
        if "none" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_functions='none'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0044"
            "执行结束==")
