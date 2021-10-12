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
Case Name   : 使用gs_guc set方法设置参数plan_cache_mode，观察预期结果
Description :
        1.查询plan_cache_mode默认值
        2.修改参数值为force_generic_plan并重启数据库
        3.查询该参数修改后的值
        4.建表并插入数据
        5.创建索引后使用analyze语句
        6.创建prepare语句后执行explain
        7.创建prepare语句后设置参数值为force_generic_plan
        8.创建prepare语句后设置参数值为默认值auto
        9.创建prepare语句后设置参数值为force_custom_plan
        10.恢复参数默认值
Expect      :
        1.显示默认值为auto
        2.修改成功
        3.显示force_generic_plan
        4.建表并插入数据成功
        5.创建索引后使用analyze语句成功
        6.创建prepare语句后执行explain成功
        7.设置成功
        8.设置成功
        9.设置成功
        10.默认值恢复成功
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
            '------Opengauss_Function_Guc_Queryplan_Case0119start------')

    def test_plan_cache_mode(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show plan_cache_mode;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:设置参数为force_custom_plan并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "plan_cache_mode ='force_custom_plan'")
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('show plan_cache_mode;')
        LOG.info(sql_cmd)
        self.assertIn('force_custom_plan', sql_cmd)
        LOG.info('--步骤4:建表并插入数据--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_strategy;
            create table test_strategy( a int);
            insert into test_strategy select 1 from 
            generate_series(1,1000)union all select 2;
             ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤5:创建索引后使用analyze语句---')
        sql_cmd = commonsh.execut_db_sql('''drop index  if exists 
            test_strategy_a_idx;
            create index test_strategy_a_idx on test_strategy(a);
            analyze test_strategy;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤6:创建prepare语句后执行explain--')
        sql_cmd = commonsh.execut_db_sql('''prepare test_strategy_pp(int) 
            as select count(*) from test_strategy where a=\$1;
            explain (costs off) execute  test_strategy_pp(2);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤7:创建prepare语句后设置参数值为force_generic_plan--')
        sql_cmd = commonsh.execut_db_sql('''prepare test_strategy_pp(int) 
            as select count(*) from test_strategy where a=\$1;
            set plan_cache_mode to force_generic_plan;
            explain (costs off) execute  test_strategy_pp(2);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤8:创建prepare语句后设置参数值为默认值auto--')
        sql_cmd = commonsh.execut_db_sql('''prepare test_strategy_pp(int) 
            as select count(*) from test_strategy where a=\$1;
            set plan_cache_mode to default;
            execute   test_strategy_pp(1);
            execute   test_strategy_pp(1);
            execute   test_strategy_pp(1);
            execute   test_strategy_pp(1);
            execute   test_strategy_pp(1);
            explain (costs off) execute  test_strategy_pp(2);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd)
        self.assertIn('1000', sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤9:创建prepare语句后设置参数值为force_custom_plan--')
        sql_cmd = commonsh.execut_db_sql('''prepare test_strategy_pp(int) 
            as select count(*) from test_strategy where a=\$1;
            set plan_cache_mode to force_custom_plan;
            explain (costs off) execute  test_strategy_pp(2);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤10:清理环境--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists 
            test_strategy cascade;
            ''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show plan_cache_mode;')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"plan_cache_mode={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        sql_cmd = commonsh.execut_db_sql('show plan_cache_mode;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0119执行完成------')
