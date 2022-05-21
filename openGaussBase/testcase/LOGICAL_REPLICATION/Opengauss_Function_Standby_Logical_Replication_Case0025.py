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
Case Type   : 备机支持逻辑复制
Case Name   : session1启动长事务，session2创建逻辑复制槽会超时退出
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        4.session1开始长事务
        5.session2创建逻辑复制槽
        6.获取step4&step5结果
        7.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.pg_hba.conf 配置逻辑复制的用户白名单成功
        4.事务执行中
        5.session1事务未结束，session2创建逻辑复制槽超时退出， timeout expired
        6.获取成功，创建复制槽超时退出；session1数据插入成功
        7.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Logical_Replication_Case0025start-----')
        self.constant = Constant()
        self.com = Common()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_node1 = Node('Standby1DbUser')
        self.root_node = Node('Standby1Root')
        self.us_name = "u_logical_replication_0025"
        self.tb_name = "tb_logical_replication_0025"
        self.slot_name = "slot_logical_replication_0025"
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)

    def test_standby_logical(self):
        text = '--step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect:修改成功--'
        self.log.info(text)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)

        text = '--step2:重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:配置逻辑复制的用户;expect:配置成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop role if exists \
            {self.us_name};
            create role {self.us_name} with login \
            password '{macro.COMMON_PASSWD}';
            alter role {self.us_name} with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertTrue(self.constant.CREATE_ROLE_SUCCESS_MSG in sql_cmd
                        and self.constant.ALTER_ROLE_SUCCESS_MSG in sql_cmd,
                        '执行失败:' + text)
        self.log.info('配置主机')
        mod_msg = f"sed -i '$a\local   replication  {self.us_name}   trust' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"127.0.0.1/32   trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication  {self.us_name}   " \
                  f"::1/128    trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        self.log.info('配置备机')
        mod_msg = f"sed -i '$a\local   replication  {self.us_name}   trust' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"127.0.0.1/32   trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication  {self.us_name}   " \
                  f"::1/128    trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step4:session1启动长事务;expect:开启成功--'
        self.log.info(text)
        sql_cmd = (f'''drop table if exists {self.tb_name};
            create table {self.tb_name}(c_int int);
                begin
                    for i in 0..50000 loop
                        insert into {self.tb_name} values(i);
                        update {self.tb_name} set c_int = 100 where c_int = i;
                    end loop;
                end;
                 ''')
        self.log.info(sql_cmd)
        thread_1 = ComThread(self.pri_sh.execut_db_sql, args=(sql_cmd,))
        thread_1.setDaemon(True)
        thread_1.start()

        text = '--step5:session2创建逻辑复制槽;expect:创建失败，超时退出--'
        self.log.info(text)
        check_res = self.pri_sh.execut_db_sql('select slot_name from '
                                              'pg_replication_slots;')
        self.log.info(check_res)
        if f'{self.slot_name}' in check_res.split('\n')[-2].strip():
            del_cmd = self.pri_sh.execut_db_sql(f"select * from "
                                                f"pg_drop_replication_slot"
                                                f"('{self.slot_name}');")
            self.log.info(del_cmd)
        sql_cmd = f"pg_recvlogical " \
                  f"-d {self.primary_node.db_name} " \
                  f"-S {self.slot_name} " \
                  f"-p {self.primary_node.db_port} " \
                  f"-P mppdb_decoding " \
                  f"-U {self.us_name} " \
                  f"--create"
        self.log.info(sql_cmd)
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                          expect <<EOF
                          set timeout 300
                          spawn {sql_cmd}
                          expect "Password:"
                          send "{macro.COMMON_PASSWD}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        thread_2 = ComThread(self.com.get_sh_result, args=(self.primary_node,
                                                           execute_cmd,))
        thread_2.setDaemon(True)
        thread_2.start()

        text = '--step6:获取step4&step5结果;expect:获取成功--'
        self.log.info(text)
        self.log.info('获取step4结果')
        thread_1.join(60 * 60)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)
        self.assertIn('CREATE TABLE', msg_result_1, '执行失败:' + text)
        self.log.info('获取step5结果')
        thread_2.join(60 * 60)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        self.assertIn('timeout expired', msg_result_2, '执行失败:' + text)

    def tearDown(self):
        text = '--step7:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};drop role if exists {self.us_name};''')
        self.log.info(sql_cmd)
        check_res = self.pri_sh.execut_db_sql('select slot_name from '
                                              'pg_replication_slots;')
        self.log.info(check_res)
        if f'{self.slot_name}' in check_res.split('\n')[-2].strip():
            del_cmd = self.pri_sh.execut_db_sql(f"select * from "
                                                f"pg_drop_replication_slot"
                                                f"('{self.slot_name}');")
            self.log.info(del_cmd)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.primary_node.sh(del_msg).result()
        self.log.info(msg)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.standby_node.sh(del_msg).result()
        self.log.info(msg)
        res_cmd = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'wal_level=hot_standby')
        self.log.info(res_cmd)
        res_cmd = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_slot_log=off')
        self.log.info(res_cmd)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '--Opengauss_Function_Logical_Replication_Case0025finish----')
