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
Case Type   : 工具-GS_BASEBACKUP
Case Name   : 不自定义表空间，远程备份，开启进度报告，开启冗余模式，检查点模式设置为fast,t模式压缩备份
Description :
    1.执行备份：gs_basebackup -D /usr2/chenchen/basebackup/bak_Pvfast_wt
        -Ft -Xfetch -p 18333 -l gauss_15.bak -P -v -U sysadmin -w
    2.解压备份包：gs_tar -D /wyc/tmp/backup/tmp -F /wyc/tmp/backup/base.tar
    3.使用备份目录启动数据库
Expect      :
    1.备份提示成功，生成base.tar备份文件
    2.解压出base.tar
    3.使用备份目录启动数据库成功
History     :
"""

import os
import time
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class GsBaseBackUpCase23(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Primary_Root_Node = Node('PrimaryRoot')
        self.Standby1_User_Node = Node('Standby1DbUser')
        self.Standby1_Root_Node = Node('Standby1Root')
        self.LOG = Logger()
        self.Constant = Constant()
        self.backup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                            'gs_basebackup')
        self.tar_path = os.path.join(macro.DB_BACKUP_PATH,
                                     'gs_basebackup_tar')
        self.TAR_NAME = 'base.tar'
        self.T_NAME = 't_basebackup_23'
        self.T_Insert_Value = 'gs_basebackup_23'
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0023.bak'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0023 start----')

    def test_server_tools(self):
        self.LOG.info('----主备机创建备份目录----')
        mkdir_cmd = f'''if [ ! -d "{self.backup_bak_path}" ]
                        then
                            mkdir -p {self.backup_bak_path}
                        else
                            rm -rf {os.path.join(self.backup_bak_path,
                                                 '*')}
                        fi
                        if [ ! -d "{self.tar_path}" ]
                        then
                            mkdir -p {self.tar_path}
                        else
                            rm -rf {os.path.join(self.tar_path, '*')}
                        fi'''
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(primary_result)
        self.assertEqual(primary_result, '')
        standby1_result = self.Standby1_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(standby1_result)
        self.assertEqual(standby1_result, '')

        self.LOG.info('----主备机修改备份目录权限700，以免权限有误----')
        chmod_cmd = f"chmod 700 -R {self.backup_bak_path}; " \
            f"chmod 700 -R {self.tar_path}"
        self.LOG.info(chmod_cmd)
        primary_chmod_msg = self.Primary_Root_Node.sh(chmod_cmd).result()
        self.LOG.info(primary_chmod_msg)
        self.assertEqual(primary_chmod_msg, '')
        standby1_chmod_msg = self.Standby1_Root_Node.sh(chmod_cmd).result()
        self.LOG.info(standby1_chmod_msg)
        self.assertEqual(standby1_chmod_msg, '')

        self.LOG.info('----主备机查看备份目录----')
        ls_cmd = f"ls -l {os.path.dirname(self.backup_bak_path)}"
        self.LOG.info(ls_cmd)
        primary_ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(primary_ls_msg)
        standby1_ls_msg = self.Standby1_User_Node.sh(ls_cmd).result()
        self.LOG.info(standby1_ls_msg)

        self.LOG.info('----主机创建测试表---')
        sql_cmd = f"drop table if exists {self.T_NAME}; " \
            f"create table {self.T_NAME}(name varchar(20)); " \
            f"insert into {self.T_NAME} values ('{self.T_Insert_Value}')"
        self.LOG.info(sql_cmd)
        sql_result = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_result)

        self.LOG.info('----备机执行备份----')
        gs_basebackup_cmd = f'gs_basebackup ' \
            f'-D {self.backup_bak_path} ' \
            f'-Ft ' \
            f'-Xfetch ' \
            f'-p {self.Standby1_User_Node.db_port} ' \
            f'-h {self.Primary_User_Node.ssh_host} ' \
            f'-l {self.gs_basebackup_bak_name} ' \
            f'-U {self.Standby1_User_Node.ssh_user} ' \
            f'-c fast ' \
            f'-v ' \
            f'-W ' \
            f'-P'
        backup_cmd = f'''
            source {macro.DB_ENV_PATH}
            expect <<EOF
            set timeout 1200
            spawn {gs_basebackup_cmd}
            expect "*assword:"
            send "{self.Standby1_User_Node.ssh_password}\\n"
            expect "{self.Constant.gs_basebackup_success_msg}" 
            send_user "执行成功";exit
            expect eof\n''' + '''EOF'''
        self.LOG.info(backup_cmd)
        backup_msg = self.Standby1_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_msg)
        self.assertIn("执行成功", backup_msg)

        self.LOG.info('----scp备份文件到主机----')
        scp_cmd = f"scp -r {os.path.join(self.backup_bak_path, '*')}" \
            f" {self.Primary_User_Node.ssh_user}@" \
            f"{self.Primary_User_Node.ssh_host}:" \
            f"{self.backup_bak_path}"
        self.LOG.info(scp_cmd)
        scp_msg = self.Standby1_User_Node.sh(scp_cmd).result()
        self.LOG.info(scp_msg)
        self.assertNotIn('failed', scp_msg)

        self.LOG.info('----主备机查看备份目录----')
        ls_cmd = f"ls -l {self.backup_bak_path}"
        self.LOG.info(ls_cmd)
        primary_ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(primary_ls_msg)
        self.assertNotIn('total 0', primary_ls_msg)
        standby1_ls_msg = self.Standby1_User_Node.sh(ls_cmd).result()
        self.LOG.info(standby1_ls_msg)
        self.assertNotIn('total 0', standby1_ls_msg)

        self.LOG.info('----主机解压备份包----')
        command_var = os.path.join(self.backup_bak_path,
                                   self.TAR_NAME)
        tar_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_tar -D {self.tar_path} -F {command_var}"
        self.LOG.info(tar_cmd)
        tar_msg = self.Primary_User_Node.sh(tar_cmd).result()
        self.LOG.info(tar_msg)

        self.LOG.info('----主机停止数据库----')
        is_stopped = Primary_SH.execute_gsctl(
            'stop', self.Constant.GS_CTL_STOP_SUCCESS_MSG)
        self.assertTrue(is_stopped)

        time.sleep(5)

        self.LOG.info('----主机使用备份目录启动数据库----')
        start_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl start -D {self.tar_path} -M primary"
        self.LOG.info(start_cmd)
        start_msg = self.Primary_User_Node.sh(start_cmd).result()
        self.LOG.info(start_msg)
        self.assertIn(self.Constant.RESTART_SUCCESS_MSG, start_msg)

        self.LOG.info('----重建备机需主备连接正常----')
        result = Primary_SH.wait_cluster_connected(self.tar_path)
        self.assertTrue(result)

        self.LOG.info('----重建备机----')
        build_msg_list = Primary_SH.get_standby_and_build()
        for msg in build_msg_list:
            self.assertIn(self.Constant.BUILD_SUCCESS_MSG, msg)

        self.LOG.info('----主机查询数据库状态确认是否启动成功----')
        query_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl query -D {self.tar_path}"
        self.LOG.info(query_cmd)
        query_msg = self.Primary_User_Node.sh(query_cmd).result()
        self.LOG.info(query_msg)
        self.assertIn('db_state', query_msg)
        for arg in query_msg.splitlines():
            if 'db_state' in arg:
                self.assertIn('Normal', arg)

        self.LOG.info('----主机查询测试表是否存在----')
        sql_cmd = f"select * from {self.T_NAME};"
        self.LOG.info(sql_cmd)
        sql_msg = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_msg)
        self.assertIn(self.T_Insert_Value, sql_msg)

    def tearDown(self):
        self.LOG.info('----停止数据库----')
        stop_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl stop -D {self.tar_path}"
        self.LOG.info(stop_cmd)
        stop_msg = self.Primary_User_Node.sh(stop_cmd).result()
        self.LOG.info(stop_msg)

        self.LOG.info('----删除备份文件----')
        rm_cmd = f"rm -rf {self.backup_bak_path} {self.tar_path}"
        primary_result = self.Primary_User_Node.sh(rm_cmd).result()
        self.LOG.info(primary_result)
        standby1_result = self.Standby1_User_Node.sh(rm_cmd).result()
        self.LOG.info(standby1_result)

        self.LOG.info('----使用原目录启动数据库----')
        start_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_om -t restart"
        self.LOG.info(start_cmd)
        start_msg = self.Primary_User_Node.sh(start_cmd).result()
        self.LOG.info(start_msg)

        self.LOG.info('----重建备机需主备连接正常----')
        result = Primary_SH.wait_cluster_connected()
        self.LOG.info(result)

        self.LOG.info('----重建备机----')
        build_msg_list = Primary_SH.get_standby_and_build()
        self.LOG.info(build_msg_list)

        self.LOG.info('----删除测试表----')
        sql_cmd = f"drop table if exists {self.T_NAME}"
        self.LOG.info(sql_cmd)
        sql_msg = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_msg)

        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0023 end----')
