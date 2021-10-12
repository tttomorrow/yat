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
Case Type   : 备机支持逻辑复制
Case Name   : 备机使用pg_replication_slot_advance函数，合理报错
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        4.主机创建逻辑复制槽
        5.主机上查询逻辑复制槽
        6.备机使用pg_replication_slot_advance函数
        7.主机删除复制槽
        8.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.pg_hba.conf 配置逻辑复制的用户白名单成功
        4.主机创建逻辑复制槽成功
        5.显示slot_test018复制槽信息
        6.合理报错
        7.删除成功
        8.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Logical_Replication_Case0018start-----')
        self.constant = Constant()
        self.Standby_SH = CommonSH('Standby1DbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)

    def test_standby(self):
        self.log.info('--步骤1:修改wal_level为logical;enable_slot_log为on--')
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        self.log.info('--步骤2:重启数据库--')
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤3:配置逻辑复制的用户--')
        sql_cmd = Primary_SH.execut_db_sql(f'''drop role if exists rep;
            create role rep with login password '{macro.COMMON_PASSWD}';
            alter role rep with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        self.log.info('--步骤4:主机创建逻辑复制槽--')
        check_res = Primary_SH.execut_db_sql('select slot_name from '
                                             'pg_replication_slots;')
        self.log.info(check_res)
        if 'slot_test018' in check_res.split('\n')[-2].strip():
            del_cmd = Primary_SH.execut_db_sql("select * from "
                                               "pg_drop_replication_slot"
                                               "('slot_test018');")
            self.log.info(del_cmd)
        cre_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_create_logical_replication_slot"
                                           "('slot_test018', 'mppdb_decoding')"
                                           ";")
        self.log.info(cre_cmd)
        self.log.info('--步骤5:查询复制槽--')
        query_cmd = Primary_SH.execut_db_sql('select slot_name,plugin from'
                                             ' pg_get_replication_slots();')
        self.log.info(query_cmd)
        self.assertIn('slot_test018', query_cmd)
        self.log.info('--步骤6:备机使用pg_replication_slot_advance函数--')
        sql_cmd = self.Standby_SH.execut_db_sql("select * from "
                                                "pg_replication_slot_advance"
                                                "('slot_test018',NULL);")
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)
        self.log.info('--步骤7:主机删除复制槽--')
        del_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_drop_replication_slot"
                                           "('slot_test018');")
        self.log.info(del_cmd)
        self.assertIn('', del_cmd)

    def tearDown(self):
        self.log.info('--步骤8:清理环境--')
        sql_cmd = Primary_SH.execut_db_sql('''drop role if exists rep;''')
        self.log.info(sql_cmd)
        del_msg = f"sed -i '/replication     rep/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.primary_node.sh(del_msg).result()
        self.log.info(msg)
        del_msg = f"sed -i '/replication     rep/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.standby_node.sh(del_msg).result()
        self.log.info(msg)
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'enable_slot_log=off')
        self.log.info(restore_cmd)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '--Opengauss_Function_Logical_Replication_Case0018finish----')
