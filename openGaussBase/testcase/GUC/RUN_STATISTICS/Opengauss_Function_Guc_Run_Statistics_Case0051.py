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
Case Name   : 方式四修改参数track_activity_query_size为有效边界值,设置成功生效
Description :
    1.查询默认值
    show track_activity_query_size;
    2.方式四修改参数track_activity_query_size为有效边界值
    source env
    alter system set track_activity_query_size to 100;
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    alter system set track_activity_query_size to 101;
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    alter system set track_activity_query_size to 102400;
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    alter system set track_activity_query_size to 102399;
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    3.重启后做DML
    4.恢复默认值
    alter system set track_activity_query_size to 1024;
    gs_om -t stop && gs_om -t start
Expect      :
    1.默认值显示为1024
    2.设置成功生效,查询为设置值
    3.DML无报错
    4.恢复默认值
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0051"
            "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("步骤1:查询track_activity_query_size 期望：默认值1024")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("1024", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("步骤2:方式四修改参数track_activity_query_size为100")
        sql_cmd = COMMONSH.execut_db_sql("alter system "
            "set track_activity_query_size to 100;")
        self.assertIn("ALTER SYSTEM SET", sql_cmd)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("100", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("执行DML 期望：执行成功")
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
            select count(*) from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("方式四修改参数track_activity_query_size为101")
        sql_cmd = COMMONSH.execut_db_sql("alter system "
            "set track_activity_query_size to 101;")
        self.assertIn("ALTER SYSTEM SET", sql_cmd)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("101", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("执行DML 期望：执行成功")
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
            select count(*) from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("方式四修改参数track_activity_query_size为102400")
        sql_cmd = COMMONSH.execut_db_sql("alter system "
            "set track_activity_query_size to 102400;")
        self.assertIn("ALTER SYSTEM SET", sql_cmd)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("102400", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("执行DML 期望：执行成功")
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
            select count(*) from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("方式四修改参数track_activity_query_size为102399")
        sql_cmd = COMMONSH.execut_db_sql("alter system "
            "set track_activity_query_size to 102399;")
        self.assertIn("ALTER SYSTEM SET", sql_cmd)
        COMMONSH.restart_db_cluster()
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        LOGGER.info(sql_cmd)
        self.assertEqual("102399", sql_cmd.splitlines()[-2].strip())

        LOGGER.info("执行DML 期望：执行成功")
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
            select count(*) from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql("drop table test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)

        LOGGER.info("步骤3:恢复默认值")
        result = COMMONSH.execute_gsguc("reload",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       "track_activity_query_size=1024")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show track_activity_query_size;")
        if "1024" != sql_cmd.splitlines()[-2].strip():
            COMMONSH.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  "track_activity_query_size=1024")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Run_Statistics_Case0051"
            "执行结束==")
