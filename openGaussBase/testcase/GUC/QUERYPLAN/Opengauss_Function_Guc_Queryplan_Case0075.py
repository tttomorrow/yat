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
Case Name   : 使用gs_guc set方法设置参数default_statistics_target为20,
              观察预期结果
Description :
        1.查询default_statistics_target默认值
        2.修改参数值为20并重启数据库
        3.查询该参数修改后的值
        4.建表并通过系统表查询字段的attstattarget值
        5.ALTER TABLE SET STATISTICS的方法修改成20并查询
        6.恢复参数默认值
Expect      :
        1.显示默认值为100
        2.修改成功
        3.显示20
        4.attstattarget值为-1，表示的是该列的取样颗粒度是采用默认的值
        5.attstattarget值为20，使用自己手动定义的default_statistics_target值
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
            '-----Opengauss_Function_Guc_Queryplan_Case0075tart------')

    def test_default_statistics_target(self):
        LOG.info('--步骤一：查看默认值--')
        sql_cmd = commonsh.execut_db_sql(f'''show default_statistics_target;
        ''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤二：设置default_statistics_target为20并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'default_statistics_target =20')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤三：查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql(f'''show default_statistics_target;
        ''')
        LOG.info(sql_cmd)
        self.assertIn('20', sql_cmd)
        LOG.info('--步骤四： 建表--')
        sql_cmd = commonsh.execut_db_sql('''
            drop table if exists  tb15;
            create table tb15(id integer,name character varying,age integer);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        LOG.info('--步骤五： 查询pg_attribute系统表--')
        sql_cmd = commonsh.execut_db_sql('''select attrelid,attname,
            attstattarget  from pg_attribute where attrelid 
            =(select oid from pg_class  where relname='tb15' and attname='id');
            ''')
        LOG.info(sql_cmd)
        self.assertIn('-1', sql_cmd)
        LOG.info('--步骤六： 修改statistics成20查看attstattarget值--')
        sql_cmd = commonsh.execut_db_sql('''alter table tb15 alter column id
            set statistics 20;
            select attrelid,attname,attstattarget from pg_attribute where 
            attrelid =(select oid from pg_class  where relname='tb15')and 
            attname='id';''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.ALTER_TABLE_MSG, sql_cmd)
        self.assertIn('20', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤七： 清理环境并恢复参数默认值--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists  tb15;''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''show default_statistics_target;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"default_statistics_target"
                                         f"={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show default_statistics_target;''')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_Queryplan_Case0075执行完成---')
