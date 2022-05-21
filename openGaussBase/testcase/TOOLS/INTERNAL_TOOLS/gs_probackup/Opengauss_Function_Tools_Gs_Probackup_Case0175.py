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
Case Name   : 使用gs_probackup backup命令同时指定--remote-proto=ssh 、
             --remote-host=<ip>、--remote-port=<port>、
             --remote-user=<user>选项，远端主机以trust方式，合理报错
Description :
    1.进行初始化
    2.添加实例
    3.创建测试用户
    4.配置pg_hba.conf文件
    5.进行全量远程备份
    6.清理环境
Expect      :
    1.初始化成功
    2.添加实例成功
    3.创建成功
    4.配置成功
    5.全量远程备份失败FATAL:  Forbid remote connection with trust method
    6.清理环境成功
               方式变更，修改用例
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
            'gs_probackup_testdir0175')
        self.re_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                    'app', 'bin')
        self.remote_lib = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                       'app', 'lib')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.conf_file = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        self.us_name = "us_gs_probackup_0175"
        self.expect = "FATAL:  Forbid remote connection with trust method"
        self.log.info('-----{os.path.basename(__file__)} start-----')

    def test_server_tools(self):
        text = '--step1:进行初始化;expect:初始化成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_path};"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg, '执行失败:' + text)

        text = '--step2:添加实例;expect:添加实例成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_path} " \
                   f"--instance=test_slave_backup0175 " \
                   f"-D {macro.DB_INSTANCE_PATH}"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn("'test_slave_backup0175' " + self.constant.init_success,
                      init_msg, '执行失败:' + text)

        text = '--step3:创建测试用户;expect:创建用户成功---'
        self.log.info(text)
        cre_cmd = Primary_SH.execut_db_sql(f"drop user if exists "
                                           f"{self.us_name};"
                                           f"create user {self.us_name} "
                                           f"password "
                                           f"'{macro.COMMON_PASSWD}';"
                                           f"alter role {self.us_name} "
                                           f"with replication sysadmin;")
        self.log.info(cre_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, cre_cmd,
                      '执行失败:' + text)

        text = '--step4:配置pg_hba.conf文件;expect:配置成功---'
        self.log.info(text)
        guc_cmd = f'''source {macro.DB_ENV_PATH};
            gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
            {self.Primary_User_Node.db_name}  {self.us_name} \
            {self.Primary_User_Node.db_host}/32  sha256";
            gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
            {self.Primary_User_Node.db_name}  {self.us_name} \
            {self.Standby1_User_Node.db_host}/32  sha256"'''
        guc_res = self.Primary_User_Node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败:' + text)
        guc_cmd = f'''source {macro.DB_ENV_PATH};\
             gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
             {self.Primary_User_Node.db_name}  {self.us_name}  \
             {self.Primary_User_Node.db_host}/32  trust"'''
        self.log.info(guc_cmd)
        guc_res = self.Standby1_User_Node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败:' + text)

        text = '--step5:进行全量远程备份;expect:远端备份失败----'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup " \
                     f"-B {self.gs_probackup_path} " \
                     f"--instance=test_slave_backup0175 " \
                     f"-b FULL " \
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
        self.assertIn(self.expect, exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step6:清理环境;expect:清理环境完成---'
        self.log.info(text)
        clear_cmd = f"rm -rf {self.gs_probackup_path}"
        self.log.info(clear_cmd)
        clear_msg = self.Primary_User_Node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        drop_cmd = Primary_SH.execut_db_sql(f"drop user {self.us_name};")
        self.log.info(drop_cmd)
        self.log.info('恢复pg_hba.conf文件')
        guc_cmd1 = f'''source {macro.DB_ENV_PATH};\
        gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
       {self.Primary_User_Node.db_name}  {self.us_name} \
       {self.Primary_User_Node.db_host}/32";
        gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
        {self.Primary_User_Node.db_name}  {self.us_name} \
        {self.Standby1_User_Node.db_host}/32"'''
        guc_res1 = self.Primary_User_Node.sh(guc_cmd1).result()
        self.log.info(guc_res1)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res1,
                      '执行失败:' + text)
        guc_cmd2 = f'''source {macro.DB_ENV_PATH};\
        gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
        {self.Primary_User_Node.db_name}  \
        {self.us_name}  {self.Primary_User_Node.db_host}/32"'''
        self.log.info(guc_cmd2)
        guc_res2 = self.Standby1_User_Node.sh(guc_cmd2).result()
        self.log.info(guc_res2)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res2,
                      '执行失败:' + text)
        self.log.info('断言teardown成功')
        self.assertEqual(len(clear_msg), 0, '执行失败:' + text)
        self.assertTrue(self.constant.DROP_ROLE_SUCCESS_MSG in drop_cmd,
                        '执行失败:' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res1,
                      '执行失败:' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res2,
                      '执行失败:' + text)
        self.log.info('-----{os.path.basename(__file__)} end-----')
