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
Case Name   : 不自定义表空间，本地备份，开启进度报告，开启冗余模式，检查点模式设置为fast,
    不出现输入密码提示,t模式压缩备份,指定压缩级别9
Description :
    1、开始备份：gs_basebackup -D /usr2/chenchen/basebackup/bak_Pvfast_wt9 -Ft
        -Xfetch --compress=9 -p 18333 -l gauss_18.bak -P -v -U sysadmin -w
    2、解压1gzip -d base.tar.gz
    3、解压2：gs_tar -D /wyc/tmp/backup/tmp -F /wyc/tmp/backup/base.tar
    4、使用解压后的目录启动数据库
Expect      :
    1、备份提示成功，备份目录下生成备份文件
    2、解压出base.tar
    3、解压出openGauss数据目录
    4、使用备份目录启动数据库成功，并且数据与备份前一致
History     :
    2021-3-12 wuyuechuan说可能是wal_sender_timeout值太小导致网络波动时偶现失败，故用例开始执行时调大该值
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
class GsBaseBackUpCase17(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Primary_Root_Node = Node('PrimaryRoot')
        self.LOG = Logger()
        self.Constant = Constant()
        self.gs_basebackup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                                   'gs_basebackup')
        self.tar_path = os.path.join(macro.DB_BACKUP_PATH,
                                     'gs_basebackup_tar')
        self.TAR_NAME = 'base.tar'
        self.T_NAME = 't_basebackup_17'
        self.T_Insert_Value = 'gs_basebackup_17'
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0017.bak'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0017 start----')

        self.LOG.info('----调大wal_sender_timeout值----')
        gs_guc_flag = Primary_SH.execute_gsguc('reload',
                                               self.Constant.GSGUC_SUCCESS_MSG,
                                               'wal_sender_timeout=180s')
        self.assertTrue(gs_guc_flag)

    def test_server_tools(self):
        self.LOG.info('----创建备份目录----')
        mkdir_cmd = f'''if [ ! -d "{self.gs_basebackup_bak_path}" ]
                        then
                            mkdir -p {self.gs_basebackup_bak_path}
                        else
                            rm -rf {os.path.join(self.gs_basebackup_bak_path,
                                                 '*')}
                        fi
                        if [ ! -d "{self.tar_path}" ]
                        then
                            mkdir -p {self.tar_path}
                        else
                            rm -rf {os.path.join(self.tar_path, '*')}
                        fi'''
        mkdir_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(mkdir_result)
        self.assertEqual(mkdir_result, '')

        self.LOG.info('----修改备份/解压目录权限700，以免权限有误----')
        chmod_cmd = f"chmod 700 -R {self.gs_basebackup_bak_path}; " \
            f"chmod 700 -R {self.tar_path}"
        self.LOG.info(chmod_cmd)
        chmod_msg = self.Primary_Root_Node.sh(chmod_cmd).result()
        self.LOG.info(chmod_msg)
        self.assertEqual(chmod_msg, '')

        self.LOG.info('----查看备份/解压目录----')
        ls_cmd = f"ls -l {os.path.dirname(self.gs_basebackup_bak_path)}"
        self.LOG.info(ls_cmd)
        ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(ls_msg)

        self.LOG.info('----创建测试表---')
        sql_cmd = f"drop table if exists {self.T_NAME}; " \
            f"create table {self.T_NAME}(name varchar(20)); " \
            f"insert into {self.T_NAME} values ('{self.T_Insert_Value}')"
        self.LOG.info(sql_cmd)
        sql_result = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_result)

        self.LOG.info('----执行备份----')
        gs_basebackup_cmd = f"gs_basebackup " \
            f"-D {self.gs_basebackup_bak_path} " \
            f"-Ft " \
            f"-Xfetch " \
            f"--compress=9 " \
            f"-p {self.Primary_User_Node.db_port} " \
            f"-l {self.gs_basebackup_bak_name} " \
            f"-P " \
            f"-v " \
            f"-U {self.Primary_User_Node.ssh_user} " \
            f"-w"
        backup_cmd = f"source {macro.DB_ENV_PATH}; {gs_basebackup_cmd}"
        self.LOG.info(backup_cmd)
        backup_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_msg)
        self.assertIn(self.Constant.gs_basebackup_success_msg, backup_msg)

        self.LOG.info('----查看备份文件----')
        ls_cmd = f"ls -l {self.gs_basebackup_bak_path}"
        self.LOG.info(ls_cmd)
        ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(ls_msg)

        self.LOG.info('----解压出base.tar----')
        command_var = os.path.join(self.gs_basebackup_bak_path,
                                   self.TAR_NAME + '.gz')
        tar_cmd = f"gzip -d {command_var}"
        self.LOG.info(tar_cmd)
        tar_msg = self.Primary_User_Node.sh(tar_cmd).result()
        self.LOG.info(tar_msg)

        self.LOG.info('----解压出openGauss数据目录----')
        command_var = os.path.join(self.gs_basebackup_bak_path,
                                   self.TAR_NAME)
        tar_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_tar -D {self.tar_path} -F {command_var}"
        self.LOG.info(tar_cmd)
        tar_msg = self.Primary_User_Node.sh(tar_cmd).result()
        self.LOG.info(tar_msg)

        self.LOG.info('----停止数据库----')
        is_stopped = Primary_SH.execute_gsctl(
            'stop', self.Constant.GS_CTL_STOP_SUCCESS_MSG)
        self.assertTrue(is_stopped)

        time.sleep(5)

        self.LOG.info('----使用备份目录启动数据库----')
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

        self.LOG.info('----查询数据库状态确认是否启动成功----')
        query_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl query -D {self.tar_path}"
        self.LOG.info(query_cmd)
        query_msg = self.Primary_User_Node.sh(query_cmd).result()
        self.LOG.info(query_msg)
        self.assertIn('db_state', query_msg)
        for arg in query_msg.splitlines():
            if 'db_state' in arg:
                self.assertIn('Normal', arg)

        self.LOG.info('----查询测试表是否存在----')
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
        is_dir_exists_cmd = f'rm -rf {self.gs_basebackup_bak_path} ' \
            f'{self.tar_path}'
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)

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

        self.LOG.info('----还原wal_sender_timeout值----')
        gs_guc_msg = Primary_SH.execute_gsguc('reload',
                                              '',
                                              'wal_sender_timeout=6s',
                                              get_detail=True)
        self.LOG.info(gs_guc_msg)

        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0017 end----')
