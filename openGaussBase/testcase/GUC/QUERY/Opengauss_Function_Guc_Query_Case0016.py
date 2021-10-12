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
Case Name   : 使用gs_guc set设置enable_stmt_track为off值
Description :
    1、查询enable_stmt_track默认值，show enable_stmt_track;
    2、使用gs_guc set方式修改为off,重启校验是否生效
       gs_guc set -D {cluster/dn1} -c "enable_stmt_track=off";
    3、查询statement_history表记录;
       create table stmt_tab(a int,b int);
       select * from statement_history where query like '%stmt_tab%';
    4、恢复默认值
Expect      :
    1、显示默认值，on;
    2、参数设置成功，重启数据库校验参数生效;
    3、创建表成功，查询表记录，无对应记录，未启用Full/Slow SQL捕获
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
        logger.info("======Opengauss_Function_Guc_Query_Case0016开始执行======")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.config_param = 'show enable_stmt_track;'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======步骤一：查询enable_stmt_track默认望，为on======")
        show_cmd1 = self.comsh.execut_db_sql(self.config_param)
        logger.info(show_cmd1)
        self.assertEqual('on', show_cmd1.splitlines()[-2].strip())

        logger.info("======步骤二：使用gs_guc set方式修改为off,重启校验是否生效======")
        set_cmd = self.comsh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_stmt_track = off')
        logger.info(set_cmd)
        self.comsh.restart_db_cluster()
        result = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)
        show_cmd2 = self.comsh.execut_db_sql(self.config_param)
        self.assertEqual('off', show_cmd2.splitlines()[-2].strip())

        logger.info("======步骤三：创建表，查询statement_history表记录======")
        sql_cmd = f'''create table stmt_tab(a int,b int);
            select * from statement_history where query like '%stmt_tab%';'''
        logger.info(sql_cmd)
        sql_re = self.comsh.execut_db_sql(sql_cmd, dbname='postgres')
        logger.info(sql_re)
        self.assertIn('(0 rows)', sql_re)

    def tearDown(self):
        logger.info("======清理环境，恢复默认值======")
        cmd2 = self.comsh.execut_db_sql(self.config_param)
        logger.info(cmd2)
        if 'on' != cmd2.splitlines()[-2].strip():
            self.comsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'enable_stmt_track = on')
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("======Opengauss_Function_Guc_Query_Case0016执行结束======")
