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
Case Name   : 使用gs_guc set方法设置参数cursor_tuple_fraction为0.5,观察预期结果
Description :
        1.查询cursor_tuple_fraction默认值
        2.修改参数值为0.5并重启数据库
        3.查询该参数修改后的值
        4.创建表并插入数据
        5.创建游标并获取游标前3行数据
        6.清理环境
Expect      :
        1.显示默认值为0.1
        2.修改成功
        3.显示0.5
        4.表创建成功
        5.游标创建成功
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
            '------Opengauss_Function_Guc_Queryplan_Case0079start------')

    def test_cursor_tuple_fraction(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show cursor_tuple_fraction;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:设置cursor_tuple_fraction为0.5并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'cursor_tuple_fraction =0.5')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show cursor_tuple_fraction;''')
        LOG.info(sql_cmd)
        self.assertEqual('0.5', sql_cmd.split('\n')[2].strip())
        LOG.info('--步骤4:创建表并插入数据--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_019;
            create table test_019(id int);
            insert into test_019 values(generate_series(1,100));
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤5:创建游标并抓取头3行到游标cursor1里--')
        sql_cmd = commonsh.execut_db_sql('''start transaction;
        cursor cursor1 for select * from test_019 ;
        fetch forward 3 from cursor1; 
        close cursor1;
        end;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.DECLEAR_CURSOR_SUCCESS_MSG, sql_cmd)
        self.assertIn('3 rows', sql_cmd)
        self.assertIn(self.constant.CLOSE_CURSOR_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_019;''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''show cursor_tuple_fraction;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"cursor_tuple_fraction={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show cursor_tuple_fraction;''')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0079执行完成------')
