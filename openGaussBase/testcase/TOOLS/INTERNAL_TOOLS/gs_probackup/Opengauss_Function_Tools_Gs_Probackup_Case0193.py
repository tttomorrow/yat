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
Case Name   : 使用gs_probackup backup命令使用gs_probackup backup命令添加连接
              参数选项-d、-h（本机ip）、-p、-U（普通用户）、-W选项，
              端口不正确，合理报错
Description :
    1.创建备份目录
    2.进行初始化
    3.创建测试用户和数据库
    4.配置pg_hba.conf文件
    5.添加远程实例
    6.进行全量备份
    7.恢复环境
Expect      :
    1.创建成功
    2.初始化成功
    3.创建成功
    4.配置成功
    5.添加远程实例成功
    6.备份失败
    7.恢复环境完成
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.log = Logger()
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.gs_probackup_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH),
            'gs_probackup_testdir0193')
        self.us_name = "us_gs_probackup_0193"
        self.db_name = "db_gs_probackup_0193"
        self.log.info('-----os.path.basename(__file__)} start-----')

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

        text = '--step3:创建测试用户和数据库;expect:创建用户成功---'
        self.log.info(text)
        cre_cmd = self.pri_sh.execut_db_sql(f"drop user if exists "
                                            f"{self.us_name};"
                                            f"create user {self.us_name} "
                                            f"password "
                                            f"'{macro.COMMON_PASSWD}';"
                                            f"alter role {self.us_name} "
                                            f"with replication sysadmin;"
                                            f"drop database if exists "
                                            f"{self.db_name};"
                                            f"create database {self.db_name};")
        self.log.info(cre_cmd)
        self.assertTrue('CREATE ROLE' in cre_cmd and 'CREATE DATABASE'
                        in cre_cmd, '执行失败:' + text)

        text = '--step4:配置pg_hba.conf文件;expect:配置成功---'
        self.log.info(text)
        set_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_guc reload -N all -I all -h "host  \
            {self.db_name}  {self.us_name} \
            {self.Primary_User_Node.db_host}/32  sha256";'''
        self.log.info(set_cmd)
        msg = self.Primary_User_Node.sh(set_cmd).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"{self.Primary_User_Node.db_host}/32   sha256' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.Primary_User_Node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step5:添加远程实例;expect:添加成功----'
        self.log.info(text)
        add_cmd = f"source {macro.DB_ENV_PATH};" \
                  f"gs_probackup add-instance " \
                  f"-B {self.gs_probackup_path} " \
                  f"-D {macro.DB_INSTANCE_PATH} " \
                  f"--instance=test_0193 "
        self.log.info(add_cmd)
        exec_msg = self.Primary_User_Node.sh(add_cmd).result()
        self.log.info(exec_msg)
        self.assertIn("'test_0193' " + self.constant.init_success, exec_msg,
                      '执行失败:' + text)

        text = '--step6:进行全量备份;expect:备份失败----'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup " \
                     f"-B {self.gs_probackup_path} " \
                     f"--instance=test_0193 " \
                     f"-b FULL " \
                     f"-h {self.Primary_User_Node.db_host} " \
                     f"-d {self.db_name} " \
                     f"-U {self.us_name} " \
                     f"-W {macro.COMMON_PASSWD} " \
                     f"-p abc"
        self.log.info(backup_cmd)
        exec_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('invalid integer value "abc" ',
                      exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step7:恢复环境;expect:恢复环境完成--'
        self.log.info(text)
        rm_cmd = f"rm -rf {self.gs_probackup_path}"
        self.log.info(rm_cmd)
        clear_msg = self.Primary_User_Node.sh(rm_cmd).result()
        self.log.info(clear_msg)
        drop_cmd = self.pri_sh.execut_db_sql(f"drop user {self.us_name};"
                                             f"drop database if exists "
                                             f"{self.db_name}")
        self.log.info(drop_cmd)
        self.log.info('恢复pg_hba.conf文件')
        restore_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_guc reload -N all -I all -h "host  \
                    {self.db_name}  {self.us_name} \
                    {self.Primary_User_Node.db_host}/32";'''
        self.log.info(restore_cmd)
        guc_result = self.Primary_User_Node.sh(restore_cmd).result()
        self.log.info(guc_result)
        mod_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(mod_msg)
        sed_result = self.Primary_User_Node.sh(mod_msg).result()
        self.log.info(sed_result)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('断言teardown成功')
        self.assertEqual(len(clear_msg), 0, '执行失败:' + text)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, drop_cmd,
                      '执行失败:' + text)
        self.assertEqual(len(sed_result), 0, '执行失败:' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_result,
                      '执行失败:' + text)
        self.log.info('-----os.path.basename(__file__)} end-----')
