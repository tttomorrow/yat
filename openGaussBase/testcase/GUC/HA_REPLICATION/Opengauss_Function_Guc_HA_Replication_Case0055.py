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
Case Name   : 使用gs_guc set方法在备机设置参数primary_slotname,观察预期结果
Description :
        1.查询primary_slotname参数默认值
        2.修改参数wal_level为logical
        3.重启数据库
        4.查询wal_level修改后的值
        5.主机上创建逻辑复制槽
        6.修改备机primary_slotname为slot55
        7.重启数据库
        8.查询备机primary_slotname参数值
        9.查询主备环境状态
        10.删除备机primary_slotname参数并重启数据库
        11.查询主备环境状态
        12.清理环境
        13.重建备机并查询数据库状态
Expect      :
        1.显示默认值为空
        2.wal_level参数设置成功
        3.重启数据库成功
        4.显示logical
        5.创建逻辑复制槽成功
        6.修改primary_slotname为slot55成功
        7.重启数据库成功
        8.备机primary_slotname参数值为slot55
        9.备机显示need repair
        10.删除成功
        11.主备环境状态正常
        12.清理环境成功
        13.重建备机完成，数据库状态normal
History     :
"""
import os
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')
constant = Constant()


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_HA_Replication_Case0055start-----')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.Standby1_Root_Node = Node('Standby1Root')
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.slot = os.path.join(self.DB_INSTANCE_PATH, 'postgresql.conf')

    def test_primary_slotname(self):
        self.log.info('--步骤一：查询primary_slotname参数默认值--')
        query_cmd = Primary_SH.execut_db_sql('show primary_slotname;')
        self.log.info(query_cmd)
        self.assertIn('', query_cmd)
        self.log.info('--步骤二：修改wal_level为logical--')
        mod_msg = Primary_SH.execute_gsguc('set',
                                           constant.GSGUC_SUCCESS_MSG,
                                           'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        self.log.info('--步骤三：重启数据库--')
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤四：查询修改后的参数值--')
        sql_cmd = Primary_SH.execut_db_sql('show wal_level;')
        self.log.info(sql_cmd)
        self.assertEqual('logical', sql_cmd.split('\n')[2].strip())
        self.log.info('--步骤五：主机上创建逻辑复制槽--')
        check_res = Primary_SH.execut_db_sql('select slot_name from '
                                             'pg_replication_slots;')
        self.log.info(check_res)
        if 'slot55' == check_res.split('\n')[-2].strip():
            del_cmd = Primary_SH.execut_db_sql('''select * from
                                 pg_drop_replication_slot('slot55');
                                 ''')
            self.log.info(del_cmd)
        create_cmd = Primary_SH.execut_db_sql('''select * from 
            pg_create_logical_replication_slot('slot55','mppdb_decoding');
            ''')
        self.log.info(create_cmd)
        self.assertIn('slot55', create_cmd)
        self.log.info('--步骤六：备机修改primary_slotname参数值为slot55--')
        self.log.info('--获取备机hostname--')
        check_cmd = 'hostname'
        self.log.info(check_cmd)
        hostname = self.Standby1_Root_Node.sh(check_cmd).result()
        self.log.info(hostname)
        mod_msg = self.standby_sh.execute_gsguc('set',
                                                constant.GSGUC_SUCCESS_MSG,
                                                "primary_slotname ='slot55'",
                                                node_name=f'{hostname}')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        self.log.info('--步骤七：重启数据库--')
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤八：查询备机primary_slotname参数值--')
        query_cmd = self.standby_sh.execut_db_sql('show primary_slotname;')
        self.log.info(query_cmd)
        self.assertEqual('slot55', query_cmd.split('\n')[2].strip())
        self.log.info('--步骤九：查询主备环境状态--')
        check_status = self.standby_sh.get_db_cluster_status('detail')
        self.log.info(check_status)
        self.assertIn('Standby Need repair', check_status)
        self.log.info('--步骤十：备机中删除primary_slotname参数值--')
        del_cmd = f"sed -i '/primary_slotname/d' {self.slot}"
        self.log.info(del_cmd)
        msg = self.standby_node.sh(del_cmd).result()
        self.log.info(msg)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def tearDown(self):
        self.log.info('--步骤十一：清理环境--')
        del_cmd = Primary_SH.execut_db_sql('''select * from
            pg_drop_replication_slot('slot55');
            ''')
        self.log.info(del_cmd)
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               constant.GSGUC_SUCCESS_MSG,
                                               'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        query_cmd = Primary_SH.execut_db_sql('show wal_level;')
        self.log.info(query_cmd)
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               constant.GSGUC_SUCCESS_MSG,
                                               "primary_slotname=''")
        self.log.info(restore_cmd)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        query_cmd = Primary_SH.execut_db_sql('show primary_slotname;')
        self.log.info(query_cmd)
        self.log.info('--步骤十三：重建备机--')
        build_msg_list = Primary_SH.get_standby_and_build()
        self.log.info(build_msg_list)
        self.log.info(
            '--Opengauss_Function_Guc_HA_Replication_Case0055finish----')
