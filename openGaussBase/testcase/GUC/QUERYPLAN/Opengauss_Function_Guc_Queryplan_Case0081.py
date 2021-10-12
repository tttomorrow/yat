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
Case Name   : 使用gs_guc set方法设置参数from_collapse_limit为1,观察预期结果
Description :
        1.查询from_collapse_limit默认值
        2.修改参数值为1并重启数据库
        3.查询该参数修改后的值
        4.创建表并插入数据后使用子查询
        5.清理环境
Expect      :
        1.显示默认值为8
        2.修改成功
        3.显示1
        4.创建表并插入数据且查询成功
        5.清理环境完成
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
            '------Opengauss_Function_Guc_Queryplan_Case0081start------')

    def test_from_collapse_limit(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show from_collapse_limit;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:gs_guc set设置from_collapse_limit为1并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'from_collapse_limit =1')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show from_collapse_limit;''')
        LOG.info(sql_cmd)
        self.assertIn('1', sql_cmd)
        LOG.info('--步骤4:创建表并插入数据后使用子查询--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists department;
            create table department(
            id int primary key      not null,
            dept           char(50) not null,
            emp_id         int      not null
            );
            insert into department (id, dept, emp_id) values 
            (1, 'it billing', 1 );
            insert into department (id, dept, emp_id) values
            (2, 'engineering', 2 );
            insert into department (id, dept, emp_id) values
            (3, 'finance', 7 );
            explain select * from department,(select * from department limit 2)
            where department.id =2;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤5:清理环境--')
        sql_cmd = commonsh.execut_db_sql(
            ''' drop table if exists department;''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show from_collapse_limit;')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"from_collapse_limit={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show from_collapse_limit;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0081执行完成------')
