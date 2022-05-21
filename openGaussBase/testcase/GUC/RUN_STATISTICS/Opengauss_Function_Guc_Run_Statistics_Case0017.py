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
Case Name   : 修改enable_save_datachanged_timestamp为off，观察预期结果；
Description :
    1、查询enable_save_datachanged_timestamp默认值；
    show enable_save_datachanged_timestamp;
    2、修改enable_save_datachanged_timestamp为off，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "enable_save_datachanged_timestamp=off"
    gs_om -t stop && gs_om -t start
    show enable_save_datachanged_timestamp;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为off
    3、改变表的数据，再查询PG_STAT_SYS_TABLES看看对应表的last_data_changed有没有统计到时间戳
    4、恢复默认值成功；
History     :
"""

import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')


class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("------------------------Opengauss_Function_Guc_Run_Statistics_Case0017开始执行-----------------------------")
        self.Constant = Constant()

    def test_guc(self):
        logger.info("查询enable_save_datachanged_timestamp 期望：默认值on")
        sql_cmd = commonsh.execut_db_sql('''show enable_save_datachanged_timestamp;''')
        logger.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())

        logger.info("修改enable_save_datachanged_timestamp为off，重启使其生效，期望：设置成功")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'enable_save_datachanged_timestamp=off')
        self.assertTrue(result)

        logger.info("期望：重启后查询结果为off")
        commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        sql_cmd = commonsh.execut_db_sql('''show enable_save_datachanged_timestamp;''')
        logger.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())
        result = commonsh.execut_db_sql(f'''select last_data_changed from PG_STAT_SYS_TABLES where relname='test';''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], result)
        numBefore = result.split("\n")[-2].strip()

        logger.info('执行DML 期望：执行成功')
        sql_cmd = commonsh.execut_db_sql('''
                                    drop table if exists test cascade;
                                    create table test(c_int int);
                                    insert into test values(1),(2);
                                    update test set c_int = 5 where c_int = 1;
                                    delete from test where c_int = 2;
                                    select * from test;
                                    ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        logger.info('查询执行前后last_data_changed不变')
        result = commonsh.execut_db_sql(f'''select last_data_changed from PG_STAT_SYS_TABLES where relname='test';''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], result)
        numAfter = result.split("\n")[-2].strip()
        self.assertEqual(numAfter,numBefore)

        logger.info("恢复默认值")
        logger.info("删除表")
        sql_cmd = commonsh.execut_db_sql('''drop table test cascade;''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS,sql_cmd)
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'enable_save_datachanged_timestamp=on')
        self.assertTrue(result)
        result = commonsh.restart_db_cluster()
        logger.info(result)
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd = commonsh.execut_db_sql('''show enable_save_datachanged_timestamp;''')
        if "on" not in sql_cmd:
            commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'enable_save_datachanged_timestamp=on')
            commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        logger.info("-------------------------Opengauss_Function_Guc_Run_Statistics_Case0017执行结束---------------------------")