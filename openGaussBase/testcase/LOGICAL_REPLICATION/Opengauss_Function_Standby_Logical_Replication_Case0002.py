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
Case Type   : 逻辑复制
Case Name   : 备机使用pg_recvlogical语句创建逻辑复制槽，合理报错
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.备机pg_hba.conf文件配置逻辑复制的用户白名单
        3.备机机创建逻辑复制槽
        4.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.pg_hba.conf 配置逻辑复制的用户白名单成功
        3.合理报错
        4.清理环境完成
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
            '--Opengauss_Function_Standby_Logical_Replication_Case0002start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.us_name = "us_logical_replication_case0002"
        self.slot_name = "slot_logical_replication_case0002"

    def test_standby_logical(self):
        text = '--step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect:修改成功--'
        self.log.info(text)
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
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step2:配置备机逻辑复制的用户;expect:配置成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f'''drop role if exists \
            {self.us_name};
            create role {self.us_name} with login password \
            '{macro.COMMON_PASSWD}';''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        sql_cmd = Primary_SH.execut_db_sql(f'''alter role {self.us_name} \
        with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.log.info(sql_cmd)
        self.log.info('配置备机')
        mod_msg = f"sed -i '$a\local    replication     {self.us_name}     " \
                  f"trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     {self.us_name}   " \
                  f"127.0.0.1/32   trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     {self.us_name}   " \
                  f"::1/128   trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:备机创建逻辑复制槽;expect:报错--'
        self.log.info(text)
        create_cmd = f"pg_recvlogical -d postgres " \
                     f"-U {self.us_name} " \
                     f"-S {self.slot_name} " \
                     f"-p {self.standby_node.db_port} " \
                     f"-P mppdb_decoding --create"
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                   expect <<EOF
                   set timeout 300
                   spawn {create_cmd}
                   expect "Password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        exec_msg = self.standby_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('FATAL', exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f'''drop role if exists \
            {self.us_name};''')
        self.log.info(sql_cmd)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
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
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Standby_Logical_Replication_Case0002finish-')
