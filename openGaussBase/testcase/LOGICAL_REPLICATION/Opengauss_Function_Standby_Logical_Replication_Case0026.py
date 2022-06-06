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
Case Name   : 逻辑复制pg_recvlogical -p 端口指定错误时，提示信息合理
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.配置逻辑复制的用户
        3.主机创建逻辑复制槽,端口为纯数字且端口错误
        4.端口为字符串(纯字母)
        5.端口为字符串(中文)
        6.端口为字符串(字母和数字)
        7.端口为字符串(字母,数字,特殊字符)
        8.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.配置成功
        3.合理报错，failed to connect Unknown
        4.合理报错，pg_recvlogical: invalid port number "abcd"
        5.合理报错，pg_recvlogical: invalid port number "中文"
        6.合理报错，pg_recvlogical: invalid port number "abcd123456"
        7.合理报错，ERROR: Failed to check input value: invalid token "&
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


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Standby_Logical_Replication_Case0026start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.us_name = "u_logical_replication_0026"
        self.slot_name = "slot_logical_replication_0026"

    def test_standby(self):
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
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step2:配置逻辑复制的用户;expect:设置成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop role if exists "
                                            f"{self.us_name};"
                                            f"create role {self.us_name} "
                                            f"with login password "
                                            f"'{macro.COMMON_PASSWD}';"
                                            f"alter role {self.us_name} "
                                            f"with replication sysadmin;")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
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

        text = '--step3:创建逻辑复制槽，端口为纯数字且错误--;expect:合理报错'
        self.log.info(text)
        create_cmd = f"pg_recvlogical -d postgres " \
                     f"-U {self.us_name} " \
                     f"-S {self.slot_name} " \
                     f"-p 51111111111111111111 " \
                     f"-P mppdb_decoding " \
                     f"--create"
        self.log.info(create_cmd)
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
        self.assertIn('failed to connect Unknown', exec_msg,
                      '执行失败:' + text)

        text = '--step4:创建逻辑复制槽，端口为字符串(纯字母)--;expect:合理报错'
        self.log.info(text)
        create_cmd = f"pg_recvlogical -d postgres " \
                     f"-U {self.us_name} " \
                     f"-S {self.slot_name} " \
                     f"-p abcd " \
                     f"-P mppdb_decoding " \
                     f"--create"
        self.log.info(create_cmd)
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
        self.assertIn('pg_recvlogical: invalid port number "abcd"', exec_msg,
                      '执行失败:' + text)

        text = '--step5:创建逻辑复制槽，端口为中文;expect:合理报错--'
        self.log.info(text)
        create_cmd = f"pg_recvlogical -d postgres " \
                     f"-U {self.us_name} " \
                     f"-S {self.slot_name} " \
                     f"-p 中文 " \
                     f"-P mppdb_decoding " \
                     f"--create"
        self.log.info(create_cmd)
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
        self.assertIn('pg_recvlogical: invalid port number "中文"', exec_msg,
                      '执行失败:' + text)

        text = '--step6:端口为字符串(字母和数字);expect:合理报错--'
        self.log.info(text)
        create_cmd = f"pg_recvlogical -d postgres " \
                     f"-U {self.us_name} " \
                     f"-S {self.slot_name} " \
                     f"-p abcd123456 " \
                     f"-P mppdb_decoding " \
                     f"--create"
        self.log.info(create_cmd)
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
        self.assertIn('pg_recvlogical: invalid port number "abcd123456"',
                      exec_msg, '执行失败:' + text)

        text = '--step7:创建逻辑复制槽，端口为字母,数字,特殊字符;' \
               'expect:合理报错--'
        self.log.info(text)
        create_cmd = f"pg_recvlogical -d postgres " \
                     f"-U {self.us_name} " \
                     f"-S {self.slot_name} " \
                     f"-p \'abcd123456&$%\' " \
                     f"-P mppdb_decoding " \
                     f"--create"
        self.log.info(create_cmd)
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
        self.assertIn('ERROR: Failed to check input value: invalid token',
                      exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step8:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop role if exists \
            {self.us_name};''')
        self.log.info(sql_cmd)
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
            '-Opengauss_Function_Standby_Logical_Replication_Case0026finish--')
