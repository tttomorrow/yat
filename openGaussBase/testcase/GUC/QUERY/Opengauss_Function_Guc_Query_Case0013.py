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
Case Name   : 验证enable_stmt_track功能是否正常生效
Description :
    1、查询enable_stmt_track默认值，show enable_stmt_track;
       查询log_min_duration_statement默认值，show log_min_duration_statement;
    2、设置log_min_duration_statement为0
       gs_guc reload -D {cluster/dn1} -c "log_min_duration_statement=0";
    3、查询statement_history表记录;
       create table stmt_tab(a int,b int);
       drop table stmt_tab cascade;
       select * from statement_history where query like '%stmt_tab%';
    4、恢复log_min_duration_statement默认值
Expect      :
    1、显示默认值，on & 30min;
    2、参数设置成功，校验参数生效;
    3、创建表成功，查询表记录，有对应记录，启用Full/Slow SQL捕获
    4、恢复默认值成功;
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("======Opengauss_Function_Guc_Query_Case0013开始执行======")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.config_param1 = 'show enable_stmt_track;'
        self.config_param2 = 'show log_min_duration_statement;'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======步骤一：查询enable_stmt_track默认望，为on======")
        show_cmd1 = self.comsh.execut_db_sql(self.config_param1)
        logger.info(show_cmd1)
        self.assertEqual('on', show_cmd1.splitlines()[-2].strip())

        logger.info("======查询log_min_duration_statement默认望，为30min======")
        show_cmd2 = self.comsh.execut_db_sql(self.config_param2)
        logger.info(show_cmd2)
        self.assertEqual('30min', show_cmd2.splitlines()[-2].strip())

        logger.info("======步骤二：设置log_min_duration_statement为0,校验是否生效======")
        set_cmd = self.comsh.execute_gsguc('reload',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'log_min_duration_statement = 0')
        logger.info(set_cmd)
        show_cmd3 = self.comsh.execut_db_sql(self.config_param2)
        self.assertEqual('0', show_cmd3.splitlines()[-2].strip())

        logger.info("======步骤三：创建表，查询statement_history表记录======")
        sql_cmd = f'''create table stmt_tab(a int,b int);
            drop table stmt_tab cascade;
            select pg_sleep(60);
            select * from statement_history where query like '%stmt_tab%';'''
        logger.info(sql_cmd)
        sql_res = self.comsh.execut_db_sql(sql_cmd, dbname='postgres')
        logger.info(sql_res)
        self.assertIn('(2 rows)', sql_res)

    def tearDown(self):
        logger.info("======清理环境，恢复默认值======")
        cmd2 = self.comsh.execut_db_sql(self.config_param2)
        logger.info(cmd2)
        if '30min' != cmd2.splitlines()[-2].strip():
            self.comsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'log_min_duration_statement = 30min')
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("======Opengauss_Function_Guc_Query_Case0013执行结束======")
