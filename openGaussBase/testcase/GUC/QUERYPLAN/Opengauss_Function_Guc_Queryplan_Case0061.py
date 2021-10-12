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
Case Name   : 使用gs_guc set方法设置参数geqo为off,观察预期结果
Description :
        1.查询geqo参数默认值
        2.修改参数值为off并重启数据库
        3.查询该参数修改后的值
        4.建表并插入数据
        5.使用左外连接查询
        6.恢复参数默认值
Expect      :
        1.显示默认值为on
        2.修改成功
        3.修改后的值为off
        4.建表且查询成功
        5.查询成功
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
            '----Opengauss_Function_Guc_Queryplan_Case0061start----')

    def test_geqo(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show geqo;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('--步骤2:使用设置gs_guc set设置geqo为off并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'geqo =off')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show geqo;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('--步骤4:建表并插入数据--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists a;
            drop table if exists b;
            create table a(aid int);
            create table b(bid int);
            insert into a values (1),(2),(3);
            insert into b values (2),(3),(4);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤5:使用左连接查询表--')
        sql_cmd = commonsh.execut_db_sql('''select * from a left join b 
            on(aid =bid);
            select * from a left join b on(aid =bid and bid =2);
            ''')
        LOG.info(sql_cmd)
        self.assertIn('2', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('''drop table a;
            drop table b;
            ''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''show geqo;''')
        LOG.info(sql_cmd)
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'geqo=on')
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show geqo;''')
        LOG.info(sql_cmd)
        LOG.info(
            '----Opengauss_Function_Guc_Queryplan_Case0061执行完成----')
