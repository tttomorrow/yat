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
Case Type   : 系统内部使用工具
Case Name   : 使用gs_probackup backup命令添加远程相关参数，
              指定--remote-proto=<其他协议>，远程备份失败
Description :
    1.创建备份目录
    2.进行初始化
    3.创建测试用户
    4.配置主机pg_hba.conf文件
    5.配置备机pg_hba.conf文件
    6.添加远程实例
    7.将远程连接添加到pg_probackup.conf配置文件
    8.进行全量远程备份
    9.恢复环境
Expect      :
    1.创建备份目录成功
    2.初始化成功
    3.创建成功
    4.配置成功
    5.配置成功
    6.添加远程实例成功
    7.添加完成
    8.远端备份失败，显示remote: false信息，执行本地备份
    9.恢复环境完成
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Pri_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Pri_SH.get_node_num(), '单机环境不执行')
class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Standby_User_Node = Node('Standby1DbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.log = Logger()
        self.constant = Constant()
        self.re_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                    'app', 'bin')
        self.remote_lib = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                       'app', 'lib')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.gs_probackup_path = os.path.join(macro.DB_INSTANCE_PATH,
                                              'gs_probackup_testdir0158')
        self.us_name = "us_gs_probackup_0158"
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0158 start----')

    def test_server_tools(self):
        text = '--step1:创建备份目录;expect:创建成功----'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_path}" ]
                        then
                            mkdir -p {self.gs_probackup_path}
                        fi'''
        self.log.info(mkdir_cmd)
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.log.info(primary_result)
        self.assertEqual(primary_result, '', '执行失败:' + text)

        text = '--step2:进行初始化;expect:初始化成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_path};"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg,
                      '执行失败:' + text)

        text = '--step3:创建测试用户;expect:创建用户成功---'
        self.log.info(text)
        cre_cmd = Pri_SH.execut_db_sql(f"drop user if exists "
                                       f"{self.us_name};"
                                       f"create user {self.us_name} "
                                       f"password "
                                       f"'{macro.COMMON_PASSWD}';"
                                       f"alter role {self.us_name} "
                                       f"with replication sysadmin;")
        self.log.info(cre_cmd)
        self.assertIn('CREATE ROLE', cre_cmd, '执行失败:' + text)

        text = '--step4:配置主机pg_hba.conf文件;expect:配置成功---'
        self.log.info(text)
        set_cmd = f'''source {macro.DB_ENV_PATH};
            gs_guc reload -N  all -I all -h "host  \
            {self.Primary_User_Node.db_name}     {self.us_name} \
            {self.Primary_User_Node.db_host}/32   sha256";
            gs_guc reload -N all -I all -h "host  \
            {self.Primary_User_Node.db_name}     {self.us_name} \
            {self.Standby_User_Node.db_host}/32   sha256"'''
        self.log.info(set_cmd)
        msg = self.Primary_User_Node.sh(set_cmd).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"{self.Primary_User_Node.db_host}/32   sha256' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Standby_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step5:配置备机pg_hba.conf文件;expect:配置成功---'
        self.log.info(text)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"{self.Primary_User_Node.db_host}/32   sha256' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"{self.Standby_User_Node.db_host}/32   sha256' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Standby_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step6:添加远程实例;expect:添加成功----'
        self.log.info(text)
        add_cmd = f"source {macro.DB_ENV_PATH};" \
                  f"gs_probackup add-instance " \
                  f"-B {self.gs_probackup_path} " \
                  f"-D {macro.DB_INSTANCE_PATH} " \
                  f"--instance=test_0158 " \
                  f"--remote-user={self.Standby_User_Node.ssh_user} " \
                  f"--remote-host={self.Standby_User_Node.db_host} " \
                  f"--remote-port=22 " \
                  f"--remote-proto=tcp " \
                  f"--remote-path={self.re_path} " \
                  f"--remote-lib={self.remote_lib}"
        self.log.info(add_cmd)
        exec_msg = self.Primary_User_Node.sh(add_cmd).result()
        self.log.info(exec_msg)
        self.assertIn("'test_0158' " + self.constant.init_success, exec_msg,
                      '执行失败:' + text)

        text = '--step7:将远程连接添加到pg_probackup.conf配置文件;' \
               'expect:添加完成----'
        self.log.info(text)
        set_cmd = f"source {macro.DB_ENV_PATH};" \
                  f"gs_probackup set-config " \
                  f"-B {self.gs_probackup_path} " \
                  f"-D {macro.DB_INSTANCE_PATH} " \
                  f"--instance=test_0158 " \
                  f"--remote-user={self.Standby_User_Node.ssh_user} " \
                  f"--remote-host={self.Standby_User_Node.db_host} " \
                  f"--remote-port=22 " \
                  f"--remote-proto=tcp " \
                  f"--remote-path={self.re_path} " \
                  f"--remote-lib={self.remote_lib}"
        self.log.info(set_cmd)
        exec_msg = self.Primary_User_Node.sh(set_cmd).result()
        self.log.info(exec_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], exec_msg,
                         '执行失败:' + text)

        text = '--step8:进行全量远程备份;' \
               'expect:远端备份失败，显示remote: false信息，执行本地备份----'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup " \
                     f"-B {self.gs_probackup_path} " \
                     f"--instance=test_0158 " \
                     f"-b FULL " \
                     f"--remote-user={self.Standby_User_Node.ssh_user} " \
                     f"--remote-host={self.Standby_User_Node.db_host} " \
                     f"--remote-port=22 " \
                     f"--remote-proto=tcp " \
                     f"--remote-path={self.re_path} " \
                     f"--remote-lib={self.remote_lib} " \
                     f"-d {self.Primary_User_Node.db_name} " \
                     f"-U {self.us_name} " \
                     f"-W {macro.COMMON_PASSWD} " \
                     f"-p {self.Primary_User_Node.db_port}"
        self.log.info(backup_cmd)
        exec_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('remote: false', exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step9:恢复环境;expect:恢复环境完成--'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.gs_probackup_path}'
        self.log.info(rm_cmd)
        clear_msg = self.Primary_User_Node.sh(rm_cmd).result()
        self.log.info(clear_msg)
        sql_cmd = Pri_SH.execut_db_sql(f"drop user {self.us_name};")
        self.log.info(sql_cmd)
        self.log.info('恢复主机pg_hba.conf文件')
        restore_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_guc reload -N all -I all -h "host  \
                    {self.Primary_User_Node.db_name}  {self.us_name} \
                    {self.Primary_User_Node.db_host}/32";
                    gs_guc reload -N all -I all -h "host  \
                    {self.Primary_User_Node.db_name}  {self.us_name} \
                    {self.Standby_User_Node.db_host}/32"'''
        self.log.info(restore_cmd)
        msg = self.Primary_User_Node.sh(restore_cmd).result()
        self.log.info(msg)
        mod_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Primary_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('恢复备机pg_hba.conf文件')
        mod_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Standby_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0158 end----')
