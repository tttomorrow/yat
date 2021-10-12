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
Case Name   : 修改track_activity_query_size为2048，观察预期结果；
Description :
    1、查询track_activity_query_size默认值；
    show track_activity_query_size;
    2、修改track_activity_query_size为2048，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "track_activity_query_size=2048"
    gs_om -t stop && gs_om -t start
    show track_activity_query_size;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为2048；
    3、DML无报错
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
        logger.info("------------------------Opengauss_Function_Guc_Run_Statistics_Case0009开始执行-----------------------------")
        self.Constant = Constant()

    def test_guc(self):
        logger.info("查询track_activity_query_size 期望：默认值1024")
        sql_cmd = commonsh.execut_db_sql('''show track_activity_query_size;''')
        logger.info(sql_cmd)
        self.assertEqual("1024", sql_cmd.split("\n")[-2].strip())

        logger.info("修改track_activity_query_size为2048，重启使其生效，期望：设置成功")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_activity_query_size=2048')
        self.assertTrue(result)

        logger.info("期望：重启后查询结果为2048")
        commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        sql_cmd = commonsh.execut_db_sql('''show track_activity_query_size;''')
        logger.info(sql_cmd)
        self.assertEqual("2048", sql_cmd.split("\n")[-2].strip())

        logger.info('执行DML 期望：执行成功')
        sql_cmd = commonsh.execut_db_sql('''
                                    begin
                                        for i in  0..1000 loop
                                            drop table if exists test cascade;
                                            create table test(c_int int);
                                            insert into test values(1),(2);
                                            update test set c_int = 5 where c_int = 1;
                                            delete from test where c_int = 2;
                                        end loop;
                                    end;
                                    select * from test;
                                    ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

        logger.info("恢复默认值")
        logger.info("删除表")
        sql_cmd = commonsh.execut_db_sql('''drop table test cascade;''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS,sql_cmd)
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_activity_query_size=1024')
        self.assertTrue(result)
        result = commonsh.restart_db_cluster()
        logger.info(result)
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd = commonsh.execut_db_sql('''show track_activity_query_size;''')
        if "1024" not in sql_cmd:
            commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_activity_query_size=1024')
            commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        logger.info("-------------------------Opengauss_Function_Guc_Run_Statistics_Case0009执行结束---------------------------")