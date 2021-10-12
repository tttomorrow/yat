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
Case Name   : 使用gs_guc set方法设置参数geqo_threshold为2,观察预期结果
Description :
        1.查询geqo_threshold默认值
        2.修改参数值为2并重启数据库
        3.查询该参数修改后的值
        4.建表并插入数据后查询，from后跟三项
        5.恢复参数默认值
Expect      :
        1.显示默认值为12
        2.修改成功
        3.修改后的值为2
        4.查询成功
        5.默认值恢复成功
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
            '-----Opengauss_Function_Guc_Queryplan_Case0063start-----')

    def test_geqo_threshold(self):
        LOG.info('--步骤一：查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show geqo_threshold;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤二：gs_guc set设置为2并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'geqo_threshold =2')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤三：查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('show geqo_threshold;')
        LOG.info(sql_cmd)
        self.assertIn('2', sql_cmd)
        LOG.info('--步骤四： 建表并插入数据后查询，from后跟三项--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_003;
            create table test_003(col_1 text ,col_2 text);
            insert into test_003 values('aa','bb');
            SELECT * FROM test_003 t1,test_003 t2,test_003 t3;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        sql_result_list = sql_cmd.splitlines()
        LOG.info(sql_result_list)
        self.assertEqual('aa    | bb    | aa    | bb    | aa    | bb',
                         sql_result_list[-2].strip())

    def tearDown(self):
        LOG.info('--步骤五：恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('drop table if exists test_003;')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show geqo_threshold;')
        LOG.info(sql_cmd)
        if sql_cmd.split('\n')[-2].strip() != self.res:
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'geqo_threshold={self.res}')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show geqo_threshold;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0063执行完成----')
