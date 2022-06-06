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
Case Name   : 方式三修改stats_temp_directory为pg_stat_tmp1
Description :
   步骤1:查询stats_temp_directory默认值
    show stats_temp_directory;
    步骤2:数据库用户创建目录
    mkdir {cluster/dn1}/pg_stat_tmp1
    步骤3:方式三修改stats_temp_directory为pg_stat_tmp1，校验结果
    alter database postgres set stats_temp_directory to pg_stat_tmp1;
    show stats_temp_directory;
    步骤4:恢复默认值,清理环境
Expect      :
    步骤1:显示默认值pg_stat_tmp
    步骤2:创建目录成功
    步骤3:参数设置失败合理报错，校验修改后参数值为pg_stat_tmp
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0055"
            "开始执行==")
        self.constant = Constant()
        self.user_node = Node("PrimaryDbUser")
        self.db_name = "testdb"
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc(self):
        LOGGER.info("步骤1:查询stats_temp_directory 期望：默认值pg_stat_tmp")
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        LOGGER.info(sql_cmd)
        self.assertEqual("pg_stat_tmp", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:数据库用户创建目录")
        sql_cmd = self.user_node.sh(f'''rm -rf \
            {macro.DB_INSTANCE_PATH}/pg_stat_tmp1;\
            mkdir {macro.DB_INSTANCE_PATH}/pg_stat_tmp1;''').result()
        LOGGER.info(sql_cmd)
        self.assertNotIn("bash", sql_cmd)

        LOGGER.info("步骤3:修改stats_temp_directory为pg_stat_tmp1，重启，期望：设置失败")
        sql_cmd = COMMONSH.execut_db_sql(f"drop database "
            f"if exists {self.db_name};"
            f"create database {self.db_name};"
            f"alter database {self.db_name} "
            f"set stats_temp_directory to 'pg_stat_tmp1';")
        self.assertNotIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        self.assertIn("ERROR", sql_cmd)

        LOGGER.info("步骤4:期望：重启后查询结果为pg_stat_tmp")
        sql_cmd = ("show stats_temp_directory;")
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.db_name} -U {self.user_node.db_user} \
            -p {self.user_node.db_port} \
            -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOGGER.info(msg)
        self.assertEqual("pg_stat_tmp", msg.splitlines()[-2].strip())

        LOGGER.info("步骤4:恢复默认值")
        sql_cmd = self.user_node.sh(f'''rm -rf \
            {macro.DB_INSTANCE_PATH}/pg_stat_tmp1''').result()
        LOGGER.info(sql_cmd)
        self.assertNotIn("bash", sql_cmd)
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "stats_temp_directory="
                                       "'pg_stat_tmp'")
        self.assertTrue(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        COMMONSH.execut_db_sql(f"drop database if exists {self.db_name};")
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        if "pg_stat_tmp" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "stats_temp_directory='pg_stat_tmp'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0055"
            "执行结束==")
