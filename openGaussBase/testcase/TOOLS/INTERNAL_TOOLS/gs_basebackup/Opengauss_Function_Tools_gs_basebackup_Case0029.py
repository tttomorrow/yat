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
Case Type   : 工具-GS_BASEBACKUP
Case Name   : 自定义绝对路径表空间，远程备份，开启进度报告，开启冗余模式，检查点模式设置为fast，不出现输入密码提示
Description :
    1.创建备份目录
    2.创建表空间
    3.开始备份：gs_basebackup -D /home/function0136/gs_basebackup -p 30136 -T
        /data/function0126/cluster/tablespace_test1=
        /data/function0126/cluster/tablespace_test2
        -P -v -w -c fast -h ip
    4.使用备份目录启动数据库
Expect      :
    1.创建备份目录成功
    2.创建表空间成功
    3.备份提示成功，/data/function0136/cluster/tablespace_test3目录不为空
    4.使用备份目录启动数据库成功，并且数据与备份前一致
History     :
"""

import os
import time
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class GsBaseBackUpCase29(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Primary_Root_Node = Node('PrimaryRoot')
        self.Standby1_User_Node = Node('Standby1DbUser')
        self.Standby1_Root_Node = Node('Standby1Root')
        self.LOG = Logger()
        self.Constant = Constant()
        self.T_NAME = 't_basebackup_29'
        self.Old_TableSpace_Name = 'tablespace_old'
        self.Old_TableSpace_Path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tablespace_old')
        self.New_TableSpace_Path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tablespace_new')
        self.backup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                            'gs_basebackup')
        self.backup_bak_name = 'gs_basebackup_Case0029.bak'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0029 start----')

        text = '----获取主机hostname值----'
        self.LOG.info(text)
        self.host_name = self.Primary_User_Node.sh(
            'hostname').result().strip()

    def test_server_tools(self):
        text = '----step1.1: 主备机创建备份目录 expect: 成功----'
        self.LOG.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.backup_bak_path}" ]
                                then
                                    mkdir -p {self.backup_bak_path}
                                fi'''
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(primary_result)
        self.assertEqual(primary_result, '', '执行失败:' + text)
        standby1_result = self.Standby1_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(standby1_result)
        self.assertEqual(standby1_result, '', '执行失败:' + text)

        text = '----step1.2: 备机创建重定向目录 expect: 成功----'
        self.LOG.info(text)
        is_dir_exists_cmd = f'''if [ ! -d "{self.New_TableSpace_Path}" ]
                                        then
                                            mkdir -p {self.New_TableSpace_Path}
                                        fi'''
        result = self.Standby1_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '----step1.3: 主备机修改备份目录权限700，以免权限有误 expect: 成功----'
        self.LOG.info(text)
        chmod_cmd = f"chmod 700 -R {self.backup_bak_path}"
        self.LOG.info(chmod_cmd)
        primary_chmod_msg = self.Primary_Root_Node.sh(chmod_cmd).result()
        self.LOG.info(primary_chmod_msg)
        self.assertEqual(primary_chmod_msg, '', '执行失败:' + text)
        standby1_chmod_msg = self.Standby1_Root_Node.sh(chmod_cmd).result()
        self.LOG.info(standby1_chmod_msg)
        self.assertEqual(standby1_chmod_msg, '', '执行失败:' + text)

        text = '----step2.1: 主机创建表空间目录及重定向目录 expect: 成功----'
        self.LOG.info(text)
        is_dir_exists_cmd = f'''if [ ! -d "{self.Old_TableSpace_Path}" ]
                                then
                                    mkdir -p {self.Old_TableSpace_Path}
                                fi'''
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '----step2.2: 主备机查看备份目录 expect: 成功----'
        self.LOG.info(text)
        ls_cmd = f"ls -l {os.path.dirname(self.backup_bak_path)}"
        self.LOG.info(ls_cmd)
        primary_ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(primary_ls_msg)
        standby1_ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(standby1_ls_msg)

        text = '----step3.1: 主机创建测试表空间及表 expect: 成功----'
        self.LOG.info(text)
        sql_cmd = f"drop tablespace if exists {self.Old_TableSpace_Name};" \
            f"create tablespace {self.Old_TableSpace_Name} " \
            f"location '{self.Old_TableSpace_Path}';" \
            f"drop table if exists {self.T_NAME}; " \
            f"create table {self.T_NAME}(a int);" \
            f"insert into {self.T_NAME} values (generate_series(1,10000));"
        self.LOG.info(sql_cmd)
        sql_result = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_result)
        self.assertIn(self.Constant.TABLESPCE_CREATE_SUCCESS,
                      sql_result,
                      '执行失败:' + text)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS,
                      sql_result,
                      '执行失败:' + text)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG,
                      sql_result,
                      '执行失败:' + text)

        text = '----step3.2: 备机执行远程备份 expect: 成功----'
        self.LOG.info(text)
        gs_basebackup_cmd = f"gs_basebackup " \
            f"-D {self.backup_bak_path} " \
            f"-p {self.Primary_User_Node.db_port} " \
            f'-h {self.Primary_User_Node.ssh_host} ' \
            f"-T {self.Old_TableSpace_Path}={self.New_TableSpace_Path} " \
            f"-P " \
            f"-v " \
            f"-c fast " \
            f"-w"
        backup_cmd = f"source {macro.DB_ENV_PATH}; {gs_basebackup_cmd}"
        self.LOG.info(backup_cmd)
        backup_msg = self.Standby1_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_msg)
        self.assertIn(self.Constant.gs_basebackup_success_msg,
                      backup_msg,
                      '执行失败:' + text)

        text = '----step3.3: 查看重定向目录 expect: 成功----'
        self.LOG.info(text)
        ls_new_cmd = f"ls {self.New_TableSpace_Path}"
        self.LOG.info(ls_new_cmd)
        ls_new_result = self.Standby1_User_Node.sh(ls_new_cmd).result()
        self.LOG.info(ls_new_result)
        ls_old_cmd = f"ls {self.Old_TableSpace_Path}"
        self.LOG.info(ls_old_cmd)
        ls_old_result = self.Primary_User_Node.sh(ls_old_cmd).result()
        self.LOG.info(ls_old_result)
        self.assertEqual(ls_new_result, ls_old_result, '执行失败:' + text)

        text = '----step3.4: scp备份文件到主机 expect: 成功----'
        self.LOG.info(text)
        scp_cmd = f"scp -r {os.path.join(self.backup_bak_path, '*')}" \
            f" {self.Primary_User_Node.ssh_user}@" \
            f"{self.Primary_User_Node.ssh_host}:" \
            f"{self.backup_bak_path}"
        self.LOG.info(scp_cmd)
        scp_msg = self.Standby1_User_Node.sh(scp_cmd).result()
        self.LOG.info(scp_msg)
        self.assertNotIn('failed', scp_msg, '执行失败:' + text)

        text = '----step4.1: 停止数据库 expect: 成功----'
        self.LOG.info(text)
        is_stopped = Primary_SH.execute_gsctl(
            'stop', self.Constant.GS_CTL_STOP_SUCCESS_MSG)
        self.assertTrue(is_stopped, '执行失败:' + text)

        time.sleep(5)

        text = '----step4.2: 修改参数data_directory expect: 成功----'
        self.LOG.info(text)
        msg = Primary_SH.execute_gsguc(
            command='set',
            assert_flag=self.Constant.GSGUC_SUCCESS_MSG,
            param=f"data_directory='{self.backup_bak_path}'",
            node_name=self.host_name,
            dn_path=self.backup_bak_path)
        self.assertTrue(msg, '执行失败:' + text)

        text = '----step4.3: 使用备份目录启动数据库 expect: 成功----'
        self.LOG.info(text)
        start_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl start -D {self.backup_bak_path} -M primary"
        self.LOG.info(start_cmd)
        start_msg = self.Primary_User_Node.sh(start_cmd).result()
        self.LOG.info(start_msg)
        self.assertIn(self.Constant.RESTART_SUCCESS_MSG,
                      start_msg,
                      '执行失败:' + text)

        text = '----step4.4: 重建备机需主备连接正常 expect: 成功----'
        self.LOG.info(text)
        result = Primary_SH.wait_cluster_connected(self.backup_bak_path)
        self.assertTrue(result, '执行失败:' + text)

        text = '----step4.5: 重建备机 expect: 成功----'
        self.LOG.info(text)
        build_msg_list = Primary_SH.get_standby_and_build()
        for msg in build_msg_list:
            self.assertIn(self.Constant.BUILD_SUCCESS_MSG,
                          msg,
                          '执行失败:' + text)

        text = '----step4.6: 查询数据库状态确认是否启动成功 expect: 成功----'
        self.LOG.info(text)
        query_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl query -D {self.backup_bak_path}"
        self.LOG.info(query_cmd)
        query_msg = self.Primary_User_Node.sh(query_cmd).result()
        self.LOG.info(query_msg)
        self.assertIn('db_state', query_msg, '执行失败:' + text)
        for arg in query_msg.splitlines():
            if 'db_state' in arg:
                self.assertIn('Normal', arg, '执行失败:' + text)

        text = '----step4.7: 查询测试表是否存在 expect: 成功----'
        self.LOG.info(text)
        sql_cmd = f"select * from {self.T_NAME};"
        self.LOG.info(sql_cmd)
        sql_msg = Primary_SH.execut_db_sql(sql_cmd)
        self.assertIn('10000 rows', sql_msg, '执行失败:' + text)

    def tearDown(self):
        self.LOG.info('----step5: run_teardown expect: 成功----')
        self.LOG.info('----停止数据库----')
        stop_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_ctl stop -D {self.backup_bak_path}"
        self.LOG.info(stop_cmd)
        stop_msg = self.Primary_User_Node.sh(stop_cmd).result()
        self.LOG.info(stop_msg)

        self.LOG.info('----修改参数data_directory----')
        msg = Primary_SH.execute_gsguc(
            command='set',
            assert_flag=self.Constant.GSGUC_SUCCESS_MSG,
            param=f"data_directory='{macro.DB_INSTANCE_PATH}'")
        self.LOG.info(msg)

        self.LOG.info('----使用原目录启动数据库----')
        start_flag = Primary_SH.execute_gsctl(
            'start',
            self.Constant.RESTART_SUCCESS_MSG,
            '-M primary')
        self.LOG.info(start_flag)

        self.LOG.info('----重建备机需主备连接正常----')
        result = Primary_SH.wait_cluster_connected()
        self.LOG.info(result)

        self.LOG.info('----重建备机----')
        build_msg_list = Primary_SH.get_standby_and_build()
        self.LOG.info(build_msg_list)

        self.LOG.info('----删除测试表空间和表----')
        sql_cmd = f"drop table if exists {self.T_NAME}; " \
            f"drop tablespace if exists {self.Old_TableSpace_Name}"
        self.LOG.info(sql_cmd)
        sql_msg = Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_msg)

        self.LOG.info('----删除备份文件和表空间目录----')
        is_dir_exists_cmd = f"rm -rf {self.backup_bak_path} " \
            f"{self.New_TableSpace_Path} " \
            f"{self.Old_TableSpace_Path}"
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)
        result = self.Standby1_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)

        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0029 end----')
