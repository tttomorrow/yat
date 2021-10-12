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
Case Name   : 使用gs_guc set方法设置参数constraint_exclusion为on,观察预期结果
Description :
        1.查询constraint_exclusion默认值
        2.修改参数值为on并重启数据库
        3.查询该参数修改后的值
        4.创建表增加check约束（目前不支持创建继承表）
        5.使用select和explain select语句分别查询
        6.清理环境
Expect      :
        1.显示默认值为partition
        2.修改成功
        3.显示on
        4.表创建成功
        5.查询成功
        6.清理环境完成
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
            '-------Opengauss_Function_Guc_Queryplan_Case0077start--------')

    def test_constraint_exclusion(self):
        LOG.info('--步骤一：查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show constraint_exclusion;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤二：设置constraint_exclusion为on并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'constraint_exclusion =on')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤三：查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show constraint_exclusion;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('--步骤四：创建表增加表约束--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists 
            measurement_yy04mm02;
            create table measurement_yy04mm02 (logdate  date not null 
            CHECK (logdate >= DATE '2004-02-01' AND logdate
            < DATE '2004-03-01' ) );''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        LOG.info('--步骤五：查询--')
        sql_cmd = commonsh.execut_db_sql('''select count(*) from 
            measurement_yy04mm02 where logdate >= DATE '2006-01-01';
            explain select count(*) from measurement_yy04mm02 where
            logdate >= DATE '2006-01-01';
            ''')
        LOG.info(sql_cmd)
        self.assertIn('0', sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤六：清理环境--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists
            measurement_yy04mm02;
            ''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''show constraint_exclusion;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"constraint_exclusion='{self.res}'")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show constraint_exclusion;''')
        LOG.info(sql_cmd)
        LOG.info(
            '------Opengauss_Function_Guc_Queryplan_Case0077执行完成-----')
