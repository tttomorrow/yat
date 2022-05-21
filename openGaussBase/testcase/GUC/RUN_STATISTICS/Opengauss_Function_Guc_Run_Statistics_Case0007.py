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
Case Name   : 修改track_functions为on，观察预期结果；
Description :
    1、查询track_functions默认值；
    show track_functions;
    2、修改track_functions为all，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "track_functions=all"
    gs_om -t stop && gs_om -t start
    show track_functions;
    3、重启后做DML 1000+
    4、恢复默认值；
Expect      :
    1、显示默认值 查询PG_STAT_USER_FUNCTIONS视图为空；
    2、参数修改成功，校验修改后系统参数值为all；
    3、查询PG_STAT_USER_FUNCTIONS视图不为空 DML无报错
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
        logger.info("------------------------Opengauss_Function_Guc_Run_Statistics_Case0007开始执行-----------------------------")
        self.Constant = Constant()

    def test_guc(self):
        logger.info("查询track_functions 期望：默认值none")
        sql_cmd = commonsh.execut_db_sql('''show track_functions;''')
        logger.info(sql_cmd)
        self.assertEqual("none", sql_cmd.split("\n")[-2].strip())
        logger.info("查询PG_STAT_USER_FUNCTIONS视图为空")
        sql_cmd = commonsh.execut_db_sql('''select count(*) from PG_STAT_USER_FUNCTIONS;''')
        logger.info(sql_cmd)
        self.assertEqual( int(sql_cmd.split("\n")[-2].strip()),0)

        logger.info("修改track_functions为all，重启使其生效，期望：设置成功")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_functions=all')
        self.assertTrue(result)

        logger.info("期望：重启后查询结果为all")
        commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        sql_cmd = commonsh.execut_db_sql('''show track_functions;''')
        logger.info(sql_cmd)
        self.assertEqual("all", sql_cmd.split("\n")[-2].strip())

        logger.info('执行DML 期望：执行成功')
        sql_cmd = commonsh.execut_db_sql('''
                                    drop function if exists SYN_FUN_001(c int);
                                    create or replace function SYN_FUN_001(c int)return number
                                    as
                                    b int := c;
                                    begin
                                        for i in 1..c loop
                                            b:= b - 1;
                                        end loop;
                                        return b;
                                    end;
                                    select SYN_FUN_001(5);
                                    ''')
        logger.info(sql_cmd)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        logger.info("查询PG_STAT_USER_FUNCTIONS视图不为空")
        sql_cmd = commonsh.execut_db_sql('''select count(*) from PG_STAT_USER_FUNCTIONS;''')
        logger.info(sql_cmd)
        self.assertGreater( int(sql_cmd.split("\n")[-2].strip()),0)

        logger.info("恢复默认值")
        logger.info("删除表")
        sql_cmd = commonsh.execut_db_sql('''drop function SYN_FUN_001(c int);''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_FUNCTION_SUCCESS_MSG,sql_cmd)
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_functions=none')
        self.assertTrue(result)
        result = commonsh.restart_db_cluster()
        logger.info(result)
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd = commonsh.execut_db_sql('''show track_functions;''')
        if "none" not in sql_cmd:
            commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_functions=none')
            commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        logger.info("-------------------------Opengauss_Function_Guc_Run_Statistics_Case0007执行结束---------------------------")