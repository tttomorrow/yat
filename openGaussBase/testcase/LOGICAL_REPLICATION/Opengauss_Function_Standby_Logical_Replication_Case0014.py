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
Case Name   : 主机创建逻辑复制槽，备机删除，合理报错
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        4.主机创建逻辑复制槽
        5.主机上查询逻辑复制槽
        6.备机删除复制槽
        7.主机删除复制槽
        8.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.pg_hba.conf 配置逻辑复制的用户白名单成功
        4.主机创建逻辑复制槽成功
        5.显示{self.slot_name}复制槽信息
        6.合理报错
        7.删除复制槽成功
        8.清理环境完成
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Pri_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Pri_SH.get_node_num(),
                 '单机环境不执行')
class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Logical_Replication_Case0014start-----')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.us_name = "us_logical_replication_case0014"
        self.slot_name = "slot_logical_replication_case0014"
        self.tb_name = "tb_logical_replication_case0014"
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)

    def test_primary_slotname(self):
        text = '--step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect:修改成功--'
        self.log.info(text)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)

        text = '--step2:重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:配置逻辑复制的用户;expect:配置成功--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f'''drop role if exists \
            {self.us_name};
            create role {self.us_name} with login password \
            '{macro.COMMON_PASSWD}';
            alter role {self.us_name} with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.log.info('--step2.1:配置主机--')
        mod_msg = f"sed -i '$a\local    replication     {self.us_name}      " \
                  f"trust'   {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     " \
                  f"{self.us_name}   127.0.0.1/32   trust'   {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication     " \
                  f"{self.us_name}   ::1/128    trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        self.log.info('--step2.2:配置备机--')
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
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step4:主机创建逻辑复制槽;expect:创建成功--'
        self.log.info(text)
        check_res = Pri_SH.execut_db_sql("select slot_name from "
                                         "pg_replication_slots;")
        self.log.info(check_res)
        if f'{self.slot_name}' in check_res.split('\n')[-2].strip():
            del_cmd = Pri_SH.execut_db_sql(f"select * from "
                                           f"pg_drop_replication_slot"
                                           f"('{self.slot_name}');")
            self.log.info(del_cmd)
        cre_cmd = Pri_SH.execut_db_sql(f"select * from "
                                       f"pg_create_logical_replication_slot"
                                       f"('{self.slot_name}', "
                                       f"'mppdb_decoding');")
        self.log.info(cre_cmd)
        text = '--step5:查询复制槽;expect:复制槽存在--'
        self.log.info(text)
        query_cmd = Pri_SH.execut_db_sql("select slot_name,plugin from "
                                         "pg_get_replication_slots();")
        self.log.info(query_cmd)
        self.assertIn(f'{self.slot_name}', query_cmd, '执行失败:' + text)

        text = '--step6:备机删除复制槽;expect:报错--'
        self.log.info(text)
        del_cmd = f"pg_recvlogical -d {self.standby_node.db_name} " \
                  f"-U {self.us_name} " \
                  f"-S {self.slot_name} " \
                  f"-p {self.standby_node.db_port} " \
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
        exec_msg = self.standby_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('FATAL', exec_msg, '执行失败:' + text)

        text = '--step7:主机删除复制槽;expect:删除成功--'
        self.log.info(text)
        del_cmd = Pri_SH.execut_db_sql(f"select * from "
                                       f"pg_drop_replication_slot"
                                       f"('{self.slot_name}');")
        self.log.info(del_cmd)
        self.assertIn('', del_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step8:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(
            f'''drop role if exists {self.us_name};''')
        self.log.info(sql_cmd)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.standby_node.sh(del_msg).result()
        self.log.info(msg)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.primary_node.sh(del_msg).result()
        self.log.info(msg)
        restore_cmd = Pri_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restore_cmd = Pri_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log=off')
        self.log.info(restore_cmd)

        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '--Opengauss_Function_Guc_HA_Replication_Case0014finish----')
