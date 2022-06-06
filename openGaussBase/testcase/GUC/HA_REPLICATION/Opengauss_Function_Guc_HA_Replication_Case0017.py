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
Case Name   : 使用gs_guc set方法设置参数enable_stream_replication为off,
             观察预期结果
Description :
        1.查询enable_stream_replication默认值
        2.主机上建表并在备机上查询
        3.修改参数值为off并重启数据库
        4.主机上建表并在备机上查询
        5.删表并恢复参数默认值
Expect      :
        1.显示默认值为on
        2.建表成功，备机查询成功
        3.设置成功，查询显示参数值为off
        4.建表成功，备机上查询报错，off下主备数据不同步
        5.默认值恢复成功
History     :
"""
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0017start-----')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_enable_stream_replication(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = Primary_SH.execut_db_sql('show'
                                           ' enable_stream_replication;')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:主机上建表--')
        sql_cmd = '''drop table if exists test_017;
            create table test_017(id int);
            insert into  test_017 values(1);                              
            '''
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f'gsql -d {self.primary_node.db_name}' \
                     f' -p {self.primary_node.db_port}' \
                     f' -c "{sql_cmd}"'
        self.log.info(excute_cmd)
        msg = self.primary_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)
        self.log.info('--步骤3:备机查看表--')
        sql_cmd = self.standby_sh.execut_db_sql('''select * from test_017;''')
        self.log.info(sql_cmd)
        self.assertEqual('1', sql_cmd.split('\n')[2].strip())
        self.log.info('--步骤4:修改参数值为off并重启数据库--')
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_stream_replication =off')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤5:查询修改后的参数值--')
        sql_cmd = Primary_SH.execut_db_sql('show '
                                           'enable_stream_replication;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        self.log.info('--步骤6:主机上建表--')
        sql_cmd = '''drop table if exists test_017_b;
             create table test_017_b(id int);                               
             '''
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f'gsql -d {self.primary_node.db_name}' \
                     f' -p {self.primary_node.db_port}' \
                     f' -c "{sql_cmd}"'
        self.log.info(excute_cmd)
        msg = self.primary_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)
        self.log.info('--步骤7:备机查看表，报错--')
        sql_cmd = self.standby_sh.execut_db_sql('''select * from test_017_b;''')
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)

    def tearDown(self):
        self.log.info('--步骤8:清理环境--')
        sql_cmd = Primary_SH.execut_db_sql('''drop table if exists test_017;
            drop table if exists test_017_b;''')
        self.log.info(sql_cmd)
        sql_cmd = Primary_SH.execut_db_sql('show enable_stream_replication;')
        self.log.info(sql_cmd)
        if "on" != sql_cmd.split('\n')[-2].strip():
            mod_msg = Primary_SH.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'enable_stream_replication=on')
            self.log.info(mod_msg)
            restart_msg = Primary_SH.restart_db_cluster()
            self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = Primary_SH.execut_db_sql('show enable_stream_replication;')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0017finish---')
