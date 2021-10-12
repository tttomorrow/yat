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
Case Name   : 修改log_autovacuum_min_duration，观察其预期结果
Description :
            1、查询log_autovacuum_min_duration默认值；
            show log_autovacuum_min_duration；
            2、修改log_autovacuum_min_duration为0，重启使其生效，观察预期结果
            gs_guc set -D {cluster/dn1}  -c "log_autovacuum_min_duration=0"
            3、恢复默认值；
Expect      :
            1、显示默认值；
            2、修改成功并生效
            预期结果正常；
            3、恢复默认值成功；
History     :
"""
import os
import time
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class GuctestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Guc_Autovacuum_Case0009开始执行==")
        self.constant = Constant()
        self.db_user_node = Node('PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("查询log_autovacuum_min_duration 期望：默认值-1")
        sql_cmd = COMMONSH.execut_db_sql(
            '''show log_autovacuum_min_duration;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("-1", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改log_autovacuum_min_duration为0，"
                    "重启生效，期望设置成功")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       'log_autovacuum_min_duration=0')
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为0")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql(
            '''show log_autovacuum_min_duration;''')
        LOGGER.info(sql_cmd)
        self.assertEqual("0", sql_cmd.split("\n")[-2].strip())

        LOGGER.info('查询当前时间-DML前')
        result = self.db_user_node.sh(f'''date "+%Y-%m-%d %H:%M"''').result()
        LOGGER.info(result)
        self.assertTrue("ERROR" not in result, "bash" not in result)
        time_before = result

        LOGGER.info('增加重启操作切换pg_log')
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        LOGGER.info('做DML')
        sql_cmd = COMMONSH.execut_db_sql('''
                drop table if exists test cascade;
                create table test(c_int int);
                begin
                    for i in 0..800 loop
                        insert into test values(i);
                        update test set c_int = 66 where c_int = i;
                    end loop;
                end;
                select count(*) from test;
                ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info('查询当前时间-DML后')
        time.sleep(65)
        result = self.db_user_node.sh(f'''date "+%Y-%m-%d %H:%M"''').result()
        LOGGER.info(result)
        self.assertTrue("ERROR" not in result, "bash" not in result)
        time_after = result

        LOGGER.info("查看日志中产生autovacuum")
        LOGGER.info("在相应配置文件中查看校验配置")
        time.sleep(10)
        log_path = os.path.join(macro.PG_LOG_PATH,
                                macro.DN_NODE_NAME.split('/')[0])
        log_name = self.db_user_node.sh(f"find {log_path} -type f "
            f"\( -newermt '{time_before}' -a "
            f"-not -newermt '{time_after}' \)").result()
        LOGGER.info("最新日志文件" + log_name)
        self.assertIn("postgresql", log_name)

        catcmd = f'''cat {log_name} | grep autovacuum'''
        LOGGER.info(catcmd)
        result = self.db_user_node.sh(catcmd).result()
        LOGGER.info(result)
        self.assertIn("autovacuum", result)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql(
            '''drop table if exists test cascade;''')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       'log_autovacuum_min_duration=-1')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql(
            '''drop table if exists test cascade;''')
        LOGGER.info(sql_cmd)
        sql_cmd = COMMONSH.execut_db_sql(
            '''show log_autovacuum_min_duration;''')
        if "-1" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                  'log_autovacuum_min_duration=-1')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        result1 = COMMONSH.execute_gsguc('check', '-1',
                                        'log_autovacuum_min_duration')
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertTrue(result1)
        LOGGER.info("==Guc_Autovacuum_Case0009执行结束==")
