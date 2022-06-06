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
Case Name   : 管理员用户方式三修改参数track_thread_wait_status_interval为60,设置成功并生效
Description :
    步骤1:查询track_thread_wait_status_interval默认值
    show track_thread_wait_status_interval;
    步骤2:管理员用户guser方式三修改track_thread_wait_status_interval为60
    alter database testdb set track_thread_wait_status_interval to 60;
    show track_thread_wait_status_interval;
    步骤3:做简单DML
    步骤4:恢复默认值,清理环境
Expect      :
    步骤1:显示默认值30min
    步骤2:参数设置成功，校验修改后参数值为1h
    步骤3:DML无报错
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
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0063开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.user_node = Node("PrimaryDbUser")
        self.db_name = "testdb"
        self.param = "track_thread_wait_status_interval"

    def test_guc(self):
        LOGGER.info("步骤1:查询track_thread_wait_status_interval默认值 期望：默认值30min")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        LOGGER.info(sql_cmd)
        self.assertEqual("30min", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:管理员用户方式三修改track_thread_wait_status_interval为60")
        sql_cmd = COMMONSH.execut_db_sql(f"drop database "
            f"if exists {self.db_name};"
            f"create database {self.db_name};"
            f"alter database {self.db_name} set {self.param} to 60;")
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)

        sql_cmd = (f"show {self.param};")
        excute_cmd = f'''source {macro.DB_ENV_PATH};\
            gsql -d {self.db_name} \
            -U {self.user_node.db_user}\
            -p {self.user_node.db_port} \
            -W {macro.COMMON_PASSWD} \
            -c "{sql_cmd}"\
            '''
        LOGGER.info(excute_cmd)
        result = self.user_node.sh(excute_cmd).result()
        LOGGER.info(result)
        self.assertIn("1h\n", result)

        LOGGER.info("步骤3:执行DML 期望：执行成功")
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

        LOGGER.info("步骤4:恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"{self.param}='30min'")
        self.assertTrue(result)
        sql_cmd = COMMONSH.execut_db_sql(f"drop database {self.db_name};")
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd)

        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        COMMONSH.execut_db_sql(f"drop database if exists {self.db_name};")
        sql_cmd = COMMONSH.execut_db_sql(f"show {self.param};")
        if "30min" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"{self.param}='30min'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0063执行结束==")
