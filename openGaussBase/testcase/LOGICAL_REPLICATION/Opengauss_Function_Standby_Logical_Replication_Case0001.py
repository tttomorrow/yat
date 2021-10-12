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
Case Type   : 逻辑复制
Case Name   : 主机使用pg_recvlogical语句创建逻辑复制槽并删除逻辑复制槽
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        4.主机创建逻辑复制槽
        5.主机上查询逻辑复制槽
        6.主机删除复制槽
        7.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.pg_hba.conf 配置逻辑复制的用户白名单成功
        4.主机创建逻辑复制槽成功
        5.显示slot_test001复制槽信息
        6.删除复制槽成功
        7.清理环境完成
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
            '-Opengauss_Function_Standby_Logical_Replication_Case0001start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
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
        self.log.info('--步骤3:主机配置逻辑复制的用户--')
        sql_cmd = Primary_SH.execut_db_sql(f'''drop role if exists rep;
            create role rep with login password '{macro.COMMON_PASSWD}';
            alter role rep with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        mod_msg = f"sed -i '$a\local    replication     rep      trust' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     rep   127.0.0.1/32   " \
                  f"trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication     rep   ::1/128    " \
                  f"trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        self.log.info('--步骤4:主机创建逻辑复制槽--')
        create_cmd = f"pg_recvlogical -d postgres " \
                     f"-U rep " \
                     f"-S slot_test001 " \
                     f"-p {self.primary_node.db_port} " \
                     f"-P mppdb_decoding " \
                     f"--create"
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                   expect <<EOF
                   set timeout 300
                   spawn {create_cmd}
                   expect "Password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        exec_msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        self.log.info('--步骤5:查询复制槽--')
        query_cmd = Primary_SH.execut_db_sql('select slot_name,plugin from'
                                             ' pg_get_replication_slots();')
        self.log.info(query_cmd)
        self.assertIn('slot_test001', query_cmd)
        self.log.info('--步骤6:主机删除复制槽--')
        del_cmd = f"pg_recvlogical -d postgres " \
                  f"-U rep " \
                  f"-S slot_test001 " \
                  f"-p {self.primary_node.db_port} " \
                  f" --drop"
        self.log.info(del_cmd)
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                          expect <<EOF
                          set timeout 300
                          spawn {del_cmd}
                          expect "Password:"
                          send "{macro.COMMON_PASSWD}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        exec_msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], exec_msg)

    def tearDown(self):
        self.log.info('--步骤7:清理环境--')
        sql_cmd = Primary_SH.execut_db_sql('''drop role if exists rep;''')
        self.log.info(sql_cmd)
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
            '-Opengauss_Function_Standby_Logical_Replication_Case0001finish--')
