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
Case Name   : 使用gs_guc set方法设置参数enable_analyze_check为off，观察预期结果
Description :
        1.查询enable_analyze_check默认值
        2.修改参数值为on并重启数据库
        3.建表，通过系统表查询reltuples和relpages字段值
        4.执行analyze操作
        5.通过系统表查询表上次手动统计时间及次数等信息
        6.删表并恢复参数默认值
Expect      :
        1.显示默认值为off(资料有误，已提issue)
        2.修改成功，显示on
        3.建表成功，pg_class表中的reltuples和relpages字段值均为0
        4.analyze成功
        5.查询成功，信息无误
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
            '------Opengauss_Function_Guc_Queryplan_Case0103start------')

    def test_enable_analyze_check(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show enable_analyze_check;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:gs_guc set设置enable_analyze_check为on并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'enable_analyze_check =on')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('show enable_analyze_check;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('--步骤4:建表后,通过系统表查询表并执行analyze语句--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_103;
            create table test_103 (id int);
            select relname, reltuples,relpages from pg_class where 
            relname ='test_103';
            analyze test_103(id);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn('0', sql_cmd)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤5:查询系统表--')
        sql_cmd = commonsh.execut_db_sql('''select last_analyze,analyze_count,
            relname from pg_stat_all_tables where relname ='test_103';
            ''')
        LOG.info(sql_cmd)
        self.assertIn('test_103', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('drop table if exists test_103;')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show enable_analyze_check;')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"enable_analyze_check={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show enable_analyze_check;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0103执行完成------')
