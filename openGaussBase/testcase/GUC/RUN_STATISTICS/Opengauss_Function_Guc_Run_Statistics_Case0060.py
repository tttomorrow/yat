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
Case Name   : 修改参数stats_temp_directory为没有权限的目录
Description :
    步骤1:查询stats_temp_directory默认值
    show stats_temp_directory;
    步骤2:使用root用户创建目录
    mkdir {cluster}/pg_stat_tmp1
    步骤3:方式二修改stats_temp_directory为pg_stat_tmp1，校验其预期结果
    gs_guc reload -N all -I all -c "stats_temp_directory=pg_stat_tmp1"
    show stats_temp_directory;
    步骤4:做简单DML
    步骤5:恢复默认值
Expect      :
    步骤1:显示默认值pg_stat_tmp
    步骤2:目录创建成功
    步骤3:参数修改成功，校验修改后参数值为pg_stat_tmp1
    步骤4:DML无报错，查询pg_stat_tmp1下无临时文件生成，日志报错无写入权限
    步骤5:恢复默认值成功
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0060"
                    "开始执行==")
        self.constant = Constant()
        self.user_node = Node("PrimaryDbUser")
        self.root_node = Node("PrimaryRoot")
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc(self):
        LOGGER.info("步骤1:查询stats_temp_directory 期望：默认值pg_stat_tmp")
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        LOGGER.info(sql_cmd)
        self.assertEqual("pg_stat_tmp", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:步骤2:使用root用户创建目录")
        sql_cmd = self.root_node.sh(f'''rm -rf \
            {macro.DB_INSTANCE_PATH}/pg_stat_tmp1;\
            mkdir {macro.DB_INSTANCE_PATH}/pg_stat_tmp1;
            chmod 700 {macro.DB_INSTANCE_PATH}/pg_stat_tmp1''').result()
        LOGGER.info(sql_cmd)
        self.assertNotIn("bash", sql_cmd)

        LOGGER.info("步骤3:修改stats_temp_directory为pg_stat_tmp1，重启，期望：设置成功")
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        "stats_temp_directory="
                                        "'pg_stat_tmp1'")
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为pg_stat_tmp1")
        status = COMMONSH.restart_db_cluster()
        self.assertTrue(status)
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        LOGGER.info(sql_cmd)
        self.assertEqual("pg_stat_tmp1", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤4:执行DML 期望：执行成功")
        sql_cmd = COMMONSH.execut_db_sql('''
            begin
                for i in  0..10 loop
                    drop table if exists test cascade;
                    create table test(c_int int);
                    insert into test values(1),(2);
                    update test set c_int = 5 where c_int = 1;
                    delete from test where c_int = 2;
                end loop;
            end;
            select * from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        sql_cmd = self.user_node.sh(f'''cd \
            {macro.DB_INSTANCE_PATH}/pg_stat_tmp1;\
            ls -l|grep "^-"| wc -l''').result()
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.PERMISSION_DENY_MSG, sql_cmd)
        sql_cmd = self.root_node.sh(f'''cd \
            {macro.DB_INSTANCE_PATH}/pg_stat_tmp1;\
            ls -l|grep "^-"| wc -l''').result()
        LOGGER.info(sql_cmd)
        self.assertEqual(int(sql_cmd), 0)

        LOGGER.info("步骤5:恢复默认值")
        sql_cmd = self.root_node.sh(f'''rm -rf \
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
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show stats_temp_directory;")
        if "pg_stat_tmp" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   "stats_temp_directory='pg_stat_tmp'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0060"
                    "执行结束==")
