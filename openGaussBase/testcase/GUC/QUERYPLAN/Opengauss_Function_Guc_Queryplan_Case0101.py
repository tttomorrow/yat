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
Case Name   : 使用gs_guc set方法设置参数autoanalyze为on,观察预期结果
Description :
        1.查询autoanalyze默认值
        2.默认值off下建表并手动执行analyze
        3.查询系统表pg_stat_all_tables中autoanalyze_count，last_autoanalyze
        等字段值
        4.修改参数值为on并重启数据库
        5.查询该参数修改后的值
        6.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.建表成功且analyze执行成功
        3.查询成功，默认值off下，表未被自动分析
        4.修改成功
        5.显示on
        6.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class QueryPlan(unittest.TestCase):

    def setUp(self):
        self.constant = Constant()
        LOG.info(
            '------Opengauss_Function_Guc_Queryplan_Case0101start------')

    def test_autoanalyze(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show autoanalyze;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:建表后,通过系统表查询表并执行analyze语句--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_101;
            create table test_101 (id int);
            select relname, reltuples,relpages from pg_class where 
            relname ='test_101';
            analyze test_101(id);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn('0', sql_cmd)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤3:查询系统表--')
        sql_cmd = commonsh.execut_db_sql('''select last_analyze,analyze_count,
            relname,last_autoanalyze,autovacuum_count from  pg_stat_all_tables 
            where relname='test_101';
            ''')
        LOG.info(sql_cmd)
        self.assertIn('0', sql_cmd)
        LOG.info('--步骤4:gs_guc set设置autoanalyze为on并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'autoanalyze =on')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤5:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('show autoanalyze;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('drop table if exists test_101;')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show autoanalyze;')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"autoanalyze={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show autoanalyze;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0101执行完成------')
