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
Case Name   : 管理员用户方式三修改参数track_functions为all,设置成功
Description :
    步骤1:查询track_functions默认值
    show track_functions;
    步骤2:管理员用户方式三修改track_functions为all
    alter database postgres set track_functions to 'all';
    show track_functions;
    步骤3:调用函数
    步骤4:恢复默认值,清理环境
Expect      :
    步骤1:显示默认值none
    步骤2:参数设置成功
    步骤3:调用函数无报错
    步骤4:恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0046"
            "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.user_node = Node("PrimaryDbUser")
        self.db_name = "testdb"

    def test_guc(self):
        LOGGER.info("步骤1:查询track_functions默认值 期望：默认值none")
        sql_cmd = COMMONSH.execut_db_sql("show track_functions;")
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertEqual("none", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("查询pg_stat_user_functions视图为空")
        sql_cmd = COMMONSH.execut_db_sql("select count(*) "
            "from pg_stat_user_functions;")
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertEqual(int(sql_cmd.splitlines()[-2].strip()), 0)

        LOGGER.info("步骤2:管理员用户方式三修改track_functions为all")
        sql_cmd = COMMONSH.execut_db_sql(f"drop database "
                                       f"if exists {self.db_name};"
                                       f"create database {self.db_name};"
                                       f"alter database {self.db_name} "
                                       f"set track_functions to 'all';")
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)

        sql_cmd = ("show track_functions;")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
                gsql -d {self.db_name} -U {self.user_node.db_user}\
                -p {self.user_node.db_port} \
                -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertIn("all\n", result)

        LOGGER.info("查询pg_stat_user_functions视图不为空")
        sql_cmd = ("select calls from pg_stat_user_functions "
                   "where funcname='syn_fun_001';")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
                gsql -d {self.db_name} -U {self.user_node.db_user}\
                -p {self.user_node.db_port} \
                -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result)
        num_before = result.splitlines()[-2].strip()
        LOGGER.info(num_before)

        LOGGER.info("步骤3:调用函数 期望：执行成功")
        sql_cmd = ('''drop function if exists \
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
            select pg_sleep(3);
            ''')
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
                gsql -d {self.db_name} -U {self.user_node.db_user}\
                -p {self.user_node.db_port} \
                -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result)

        LOGGER.info("查询pg_stat_user_functions视图不为空")
        sql_cmd = ("select calls from pg_stat_user_functions "
                   "where funcname='syn_fun_001';")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
                gsql -d {self.db_name} -U {self.user_node.db_user}\
                -p {self.user_node.db_port} \
                -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result)
        num_alter = result.splitlines()[-2].strip()
        LOGGER.info(num_alter)
        self.assertGreater(num_alter, num_before)

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
        sql_cmd = COMMONSH.execut_db_sql(f"drop database {self.db_name};")
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd)

        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        COMMONSH.execut_db_sql(f"drop database if exists {self.db_name};")
        COMMONSH.execute_gsguc("reload",
                              self.constant.GSGUC_SUCCESS_MSG,
                              "track_functions='none'")
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        result = COMMONSH.execut_db_sql("show track_functions;")
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertIn("none\n", result)
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0046"
            "执行结束==")
