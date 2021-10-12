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
Case Name   : 使用gs_guc set方法设置参数vacuum_defer_cleanup_age为5000,
             观察预期结果
Description :
        1.查询vacuum_defer_cleanup_age默认值
        2.建表并插入数据
        3.删除39条数据后查询pg_stat_all_tables系统表
        4.执行vacuum操作
        5.修改参数值为5000并重启数据库
        6.恢复参数默认值
Expect      :
        1.显示默认值为0
        2.建表并插入数据成功
        3.删除数据成功，查询pg_stat_all_tables系统表，n_tup_del显示0
        4.vacuum命令执行成功
        5.设置成功，查询显示参数值为5000
        6.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

constant = Constant()


class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0021start-----')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_vacuum_defer_cleanup_age(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show vacuum_defer_cleanup_age;')
        self.log.info(sql_cmd)
        self.assertEqual('0', sql_cmd.split('\n')[2].strip())
        self.log.info('--步骤2:建表并插入数据--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists test_021;
            create table test_021 (id int);
            insert into test_021 values(generate_series(1,100));
            delete from test_021 where id <40;
            select relname,n_tup_del from pg_stat_all_tables where relname
            ='test_021';
            ''')
        self.log.info(sql_cmd)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn(constant.DELETE_SUCCESS_MSG, sql_cmd)
        self.assertIn('0', sql_cmd)
        self.log.info('--步骤3:执行vacuum操作--')
        sql_cmd = self.commonsh.execut_db_sql('''vacuum test_021;''')
        self.log.info(sql_cmd)
        self.assertIn(constant.VACUUM_SUCCESS_MSG, sql_cmd)
        self.log.info('--步骤4:修改参数值为5000并重启数据库--')
        mod_msg = self.commonsh.execute_gsguc('set',
                                              constant.GSGUC_SUCCESS_MSG,
                                              'vacuum_defer_cleanup_age =5000')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤5:查询修改后的参数值--')
        sql_cmd = self.commonsh.execut_db_sql('show vacuum_defer_cleanup_age;')
        self.log.info(sql_cmd)
        self.assertIn('5000', sql_cmd)

    def tearDown(self):
        self.log.info('--步骤6:清理环境--')
        sql_cmd = self.commonsh.execut_db_sql('drop table if exists test_021;')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql('show vacuum_defer_cleanup_age;')
        self.log.info(sql_cmd)
        if "0" != sql_cmd.split('\n')[-2].strip():
            mod_msg = self.commonsh.execute_gsguc('set',
                                                  constant.GSGUC_SUCCESS_MSG,
                                                  'vacuum_defer_cleanup_age=0')
            self.log.info(mod_msg)
            restart_msg = self.commonsh.restart_db_cluster()
            self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show vacuum_defer_cleanup_age;')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0021finish---')
