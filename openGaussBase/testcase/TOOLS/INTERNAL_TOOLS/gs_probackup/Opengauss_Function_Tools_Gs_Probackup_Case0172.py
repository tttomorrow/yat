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
Case Type   : 系统工具gs_probackup
Case Name   : 远程模式下，执行增量备份,通过SSH连接对远程系统进行增量备份，
              指定--remote-proto=ssh、--remote-user、--remote-host、
              --remote-port、--remote-path<远程安装目录>
              --ssh-options选项，-d、-p、-U选项， -U指定普通用户
Description :
    1.在postgresql.conf文件中添加参数enable_cbm_tracking=on
    2.重启数据库
    3.进行初始化
    4.添加实例
    5.创建测试用户
    6.配置主机pg_hba.conf文件
    7.配置备机pg_hba.conf文件
    8.进行全量远程备份
    9.进行增量远程备份
    10.清理环境
Expect      :
    1.设置参数成功
    2.重启数据库成功
    3.初始化成功
    4.添加实例成功
    5.配置成功
    6.配置成功
    7.创建成功
    8.全量远程备份成功
    9.增量远程备份成功
    10.清理环境成功
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
                 '需主备环境，若为单机环境则不执行')
class Probackup(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Standby1_User_Node = Node('Standby1DbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.constant = Constant()
        self.gs_probackup_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH),
            'gs_probackup_testdir0172')
        self.re_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                    'app', 'bin')
        self.remote_lib = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                       'app', 'lib')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.conf_file = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        self.us_name = "us_gs_probackup_0172"
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0172 start----')

    def test_server_tools(self):
        text = '--step1:设置enable_cbm_tracking=on;expect:设置成功---'
        self.log.info(text)
        set_cmd = f"sed -i '$a\\enable_cbm_tracking=on' {self.conf_file}"
        self.log.info(set_cmd)
        msg = self.Primary_User_Node.sh(set_cmd).result()
        self.log.info(msg)

        text = '--step2:重启数据库;expect:重启数据库成功---'
        self.log.info(text)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:进行初始化;expect:初始化成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_path};"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg, '执行失败:' + text)

        text = '--step4:添加实例;expect:添加实例成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_path} " \
                   f"--instance=test_slave_backup0172 " \
                   f"-D {macro.DB_INSTANCE_PATH}"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn("'test_slave_backup0172' " + self.constant.init_success,
                      init_msg, '执行失败:' + text)

        text = '--step5:创建测试用户;expect:创建用户成功---'
        self.log.info(text)
        cre_cmd = Primary_SH.execut_db_sql(f"drop user if exists "
                                           f"{self.us_name};"
                                           f"create user {self.us_name} "
                                           f"password "
                                           f"'{macro.COMMON_PASSWD}';"
                                           f"alter role {self.us_name} "
                                           f"with replication sysadmin;")
        self.log.info(cre_cmd)
        self.assertIn('CREATE ROLE', cre_cmd, '执行失败:' + text)

        text = '--step6:配置主机pg_hba.conf文件;expect:配置成功---'
        self.log.info(text)
        set_cmd = f'''source {macro.DB_ENV_PATH};
            gs_guc reload -N all -I all -h "host  \
            {self.Primary_User_Node.db_name}  {self.us_name} \
            {self.Primary_User_Node.db_host}/32  sha256";
            gs_guc reload -N all -I all -h "host  \
            {self.Primary_User_Node.db_name}  {self.us_name} \
            {self.Standby1_User_Node.db_host}/32  sha256"'''
        self.log.info(set_cmd)
        msg = self.Primary_User_Node.sh(set_cmd).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"{self.Primary_User_Node.db_host}/32   sha256' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Standby1_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step7:配置备机pg_hba.conf文件;expect:配置成功---'
        self.log.info(text)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"{self.Primary_User_Node.db_host}/32   sha256' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"{self.Standby1_User_Node.db_host}/32   sha256' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Standby1_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step8:进行全量远程备份;expect:远端备份成功----'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup " \
                     f"-B {self.gs_probackup_path} " \
                     f"--instance=test_slave_backup0172 " \
                     f"-b FULL " \
                     f"--stream " \
                     f"--remote-user={self.Standby1_User_Node.ssh_user} " \
                     f"--remote-host={self.Standby1_User_Node.db_host} " \
                     f"--remote-port=22 " \
                     f"--remote-proto=ssh " \
                     f"--remote-path={self.re_path} " \
                     f"--remote-lib={self.remote_lib} " \
                     f"-d {self.Primary_User_Node.db_name} " \
                     f"-U {self.us_name} " \
                     f"-W {macro.COMMON_PASSWD} " \
                     f"-p {self.Primary_User_Node.db_port}"
        self.log.info(backup_cmd)
        exec_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('completed', exec_msg, '执行失败:' + text)

        text = '--step9:进行增量远程备份;expect:远端备份成功----'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup " \
                     f"-B {self.gs_probackup_path} " \
                     f"--instance=test_slave_backup0172 " \
                     f"-b PTRACK  " \
                     f"--remote-user={self.Standby1_User_Node.ssh_user} " \
                     f"--remote-host={self.Standby1_User_Node.db_host} " \
                     f"--remote-port=22 " \
                     f"--remote-proto=ssh " \
                     f"--remote-path={self.re_path} " \
                     f"--remote-lib={self.remote_lib} " \
                     f"--ssh-options='-o ServerAliveCountMax=5 " \
                     f"-o ServerAliveInterval=60' " \
                     f"-d {self.Primary_User_Node.db_name} " \
                     f"-U {self.us_name} " \
                     f"-W {macro.COMMON_PASSWD} " \
                     f"-p {self.Primary_User_Node.db_port}"
        self.log.info(backup_cmd)
        exec_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('completed', exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step10:清理环境;expect:清理环境完成---'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.gs_probackup_path}'
        self.log.info(clear_cmd)
        clear_msg = self.Primary_User_Node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        sql_cmd = Primary_SH.execut_db_sql(f"drop user {self.us_name};")
        self.log.info(sql_cmd)
        cmd = f"sed -i '/enable_cbm_tracking/d' {self.conf_file}"
        self.log.info(cmd)
        msg = self.Primary_User_Node.sh(cmd).result()
        self.log.info(msg)
        self.log.info('恢复主机pg_hba.conf文件')
        restore_cmd = f'''source {macro.DB_ENV_PATH};
            gs_guc reload -N all -I all -h "host  \
            {self.Primary_User_Node.db_name}  {self.us_name} \
            {self.Primary_User_Node.db_host}/32";
            gs_guc reload -N all -I all -h "host  \
            {self.Primary_User_Node.db_name}  {self.us_name} \
            {self.Standby1_User_Node.db_host}/32"'''
        self.log.info(restore_cmd)
        msg = self.Primary_User_Node.sh(restore_cmd).result()
        self.log.info(msg)
        mod_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Primary_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('恢复备机pg_hba.conf文件')
        mod_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Standby1_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0172 end----')
