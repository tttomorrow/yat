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
Case Name   : 修改track_io_timing为on，观察预期结果；
Description :
    1、查询track_io_timing默认值；
    show track_io_timing;
    2、修改track_io_timing为off，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "track_io_timing=on"
    gs_om -t stop && gs_om -t start
    show track_io_timing;
    3、重启后做DML 1000+
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验修改后系统参数值为on；
    3、DML无报错 查询当有一个会话进行大量事务时，pg_stat_database中的blk_read_time增大
    4、恢复默认值成功；
History     :
"""

import sys
import unittest
from yat.test import Node
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.ComThread import ComThread

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')

class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("------------------------Opengauss_Function_Guc_Run_Statistics_Case0005开始执行-----------------------------")
        self.Constant = Constant()
        self.userNode = Node('PrimaryDbUser')

    def test_guc(self):
        logger.info("查询track_io_timing 期望：默认值off")
        sql_cmd = commonsh.execut_db_sql('''show track_io_timing;''')
        logger.info(sql_cmd)
        self.assertEqual("off", sql_cmd.split("\n")[-2].strip())

        logger.info("修改track_io_timing为on，重启使其生效，期望：设置成功")
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_io_timing=on')
        self.assertTrue(result)

        logger.info("期望：重启后查询结果为on")
        commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        sql_cmd = commonsh.execut_db_sql('''show track_io_timing;''')
        logger.info(sql_cmd)
        self.assertEqual("on", sql_cmd.split("\n")[-2].strip())
        result = commonsh.execut_db_sql(f'''select blk_read_time from pg_stat_database where datname='{self.userNode.db_name}';''')
        logger.info(result)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], result)
        numBefore = result.split("\n")[-2].strip()

        logger.info('起线程执行DML 期望：执行成功')
        sql_cmd = '''
                    drop table test cascade;
                    create table test(c_int int);
                    insert into test (select * from generate_series(1,20000000));
                    select count(*) from test;
                    '''
        session = ComThread(commonsh.execut_db_sql, args=(sql_cmd, ''))
        session.setDaemon(True)
        session.start()
        result = commonsh.execut_db_sql('''select pg_sleep(0.5);''')
        logger.info(result)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], result)

        logger.info('查询blk_read_time增大')
        result = commonsh.execut_db_sql(f'''select blk_read_time from pg_stat_database where datname='{self.userNode.db_name}';''')
        logger.info(result)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], result)
        numAfter = result.split("\n")[-2].strip()
        self.assertGreater(float(numAfter), float(numBefore))

        session.join(30)
        result = session.get_result()
        logger.info(result)

        logger.info("恢复默认值")
        logger.info("删除表")
        sql_cmd = commonsh.execut_db_sql('''drop table test cascade;''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS,sql_cmd)
        result = commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_io_timing=off')
        self.assertTrue(result)
        result = commonsh.restart_db_cluster()
        logger.info(result)
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        logger.info("恢复默认值")
        sql_cmd = commonsh.execut_db_sql('''show track_io_timing;''')
        logger.info(sql_cmd)
        if "off" not in sql_cmd:
            commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'track_io_timing=off')
            commonsh.restart_db_cluster()
        status = commonsh.get_db_cluster_status()
        logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        logger.info("-------------------------Opengauss_Function_Guc_Run_Statistics_Case0005执行结束---------------------------")