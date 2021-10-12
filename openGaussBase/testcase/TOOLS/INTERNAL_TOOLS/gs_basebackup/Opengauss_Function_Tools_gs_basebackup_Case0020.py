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
Case Name   : 不自定义表空间，远程备份，默认参数
Description :
    1.创建备份目录
    /usr2/chenchen/basebackup/bak_h
    2.开始备份
    gs_basebackup -D /usr2/chenchen/basebackup/bak_h -Fp -Xstream
        -p 18333 -h ip -l gauss_21.bak -U sysadmin -W
    3.使用备份目录启动数据库
     关闭原数据库：gs_ctl stop -D /opt/openGauss_lu1208/cluster/dn1
     使用备份目录启动数据库： gs_ctl start -D /data/zhanglu/bak_h
Expect      :
    1.创建备份目录成功
    2.备份提示成功，备份目录下生成备份文件
    3.使用备份目录启动数据库失败
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
class GsBaseBackUpCase20(unittest.TestCase):
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
        self.T_NAME = 't_basebackup_20'
        self.T_Insert_Value = 'gs_basebackup_20'
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0020.bak'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0020 start----')

    def test_server_tools(self):
        self.LOG.info('----主备机创建备份目录----')
        mkdir_cmd = f'''if [ ! -d "{self.backup_bak_path}" ]
                        then
                            mkdir -p {self.backup_bak_path}
                        fi'''
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(primary_result)
        self.assertEqual(primary_result, '')
        standby1_result = self.Standby1_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(standby1_result)
        self.assertEqual(standby1_result, '')

        self.LOG.info('----主备机修改备份目录权限700，以免权限有误----')
        chmod_cmd = f"chmod 700 -R {self.backup_bak_path}"
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

        self.LOG.info('----获取主机ip----')
        get_ip_cmd = "ip addr|grep 'state UP' -A2|tail -n1|" \
                     "tr -s ' '|cut -d ' ' -f 3|cut -d '/' -f 1"
        self.LOG.info(get_ip_cmd)
        primary_ip = self.Primary_Root_Node.sh(get_ip_cmd).result()
        self.LOG.info(primary_ip)

        self.LOG.info('----备机执行备份----')
        gs_basebackup_cmd = f'gs_basebackup ' \
            f'-D {self.backup_bak_path} ' \
            f'-Fp ' \
            f'-Xstream ' \
            f'-p {self.Standby1_User_Node.db_port} ' \
            f'-h {primary_ip} ' \
            f'-l {self.gs_basebackup_bak_name} ' \
            f'-U {self.Standby1_User_Node.ssh_user} ' \
            f'-W'
        backup_cmd = f'''
            source {macro.DB_ENV_PATH}
            expect <<EOF
            set timeout 1200
            spawn {gs_basebackup_cmd}
            expect "*assword:"
            send "{self.Standby1_User_Node.ssh_password}\\n"
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
            f" {self.Primary_User_Node.ssh_user}@{primary_ip}:" \
            f"{self.backup_bak_path}"
        self.LOG.info(scp_cmd)
        scp_msg = self.Standby1_User_Node.sh(scp_cmd).result()
        self.LOG.info(scp_msg)
        self.assertNotIn('failed', scp_msg)

        self.LOG.info('----主机停止数据库----')
        is_stopped = Primary_SH.execute_gsctl(
            'stop', self.Constant.GS_CTL_STOP_SUCCESS_MSG)
        self.assertTrue(is_stopped)

        time.sleep(5)

        self.LOG.info('----主机使用备份目录启动数据库----')
        start_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl start -D {self.backup_bak_path} -M primary"
        self.LOG.info(start_cmd)
        start_msg = self.Primary_User_Node.sh(start_cmd).result()
        self.LOG.info(start_msg)
        self.assertIn(self.Constant.RESTART_SUCCESS_MSG, start_msg)

        self.LOG.info('----重建备机需主备连接正常----')
        result = Primary_SH.wait_cluster_connected(self.backup_bak_path)
        self.assertTrue(result)

        self.LOG.info('----重建备机----')
        build_msg_list = Primary_SH.get_standby_and_build()
        for msg in build_msg_list:
            self.assertIn(self.Constant.BUILD_SUCCESS_MSG, msg)

        self.LOG.info('----主机查询数据库状态确认是否启动成功----')
        query_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl query -D {self.backup_bak_path}"
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
            f"gs_ctl stop -D {self.backup_bak_path}"
        self.LOG.info(stop_cmd)
        stop_msg = self.Primary_User_Node.sh(stop_cmd).result()
        self.LOG.info(stop_msg)

        self.LOG.info('----删除备份文件----')
        rm_cmd = f'''rm -rf {self.backup_bak_path}'''
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
            '----Opengauss_Function_Tools_gs_basebackup_Case0020 end----')
