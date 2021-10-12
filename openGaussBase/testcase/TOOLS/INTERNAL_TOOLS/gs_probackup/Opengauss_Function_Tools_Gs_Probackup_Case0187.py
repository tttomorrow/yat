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
Case Type   : 系统内部使用工具
Case Name   : 使用gs_probackup backup命令添加连接参数选项-d、-h（本机ip）、
              -p、-U（初始用户），合理报错
Description :
    1.创建备份目录
    2.进行初始化
    3.获取主机ip
    4.在备份路径内初始化一个新的备份实例
    5.进行备份
    6.删除新建目录
Expect      :
    1.创建备份目录成功
    2.初始化成功
    3.获取主机ip成功
    4.初始化成功
    5.备份失败，ERROR: could not connect to database postgres:
    FATAL:  Forbid remote connection with trust method!
    6.删除成功
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


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.LOG = Logger()
        self.constant = Constant()
        self.remote_path = macro.DB_INSTANCE_PATH.replace('/dn1', '/app/bin')
        self.gs_probackup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                                  'testdir187')
        self.LOG.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0187 start----')

    def test_server_tools(self):
        self.LOG.info('---步骤1:创建备份目录----')
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_bak_path}" ]
                                then
                                    mkdir -p {self.gs_probackup_bak_path}
                                fi'''
        self.LOG.info(mkdir_cmd)
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.LOG.info(primary_result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], primary_result)
        self.LOG.info('---步骤2:进行初始化---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_bak_path};"
        self.LOG.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)
        self.LOG.info('---步骤3:获取主机ip---')
        get_ip_cmd = r"ip addr|grep 'state UP' -A2|tail -n1|" \
                     r"tr -s ' '|cut -d ' ' -f 3|cut -d '/' -f 1"
        self.LOG.info(get_ip_cmd)
        primary_ip = self.Primary_User_Node.sh(get_ip_cmd).result()
        self.LOG.info(primary_ip)
        self.LOG.info('---步骤4:在备份路径内初始化一个新的备份实例----')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_bak_path} " \
                   f"-D {macro.DB_INSTANCE_PATH} " \
                   f"--instance=test_187; "
        self.LOG.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.LOG.info(init_msg)
        self.assertIn("'test_187' " + self.constant.init_success, init_msg)
        self.LOG.info('---步骤5:进行备份----')
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup " \
                     f"-B {self.gs_probackup_bak_path} " \
                     f"--instance=test_187  " \
                     f"-b FULL  " \
                     f"-d postgres " \
                     f"-h {primary_ip} " \
                     f"-p {self.Primary_User_Node.db_port} " \
                     f"-U {self.Primary_User_Node.ssh_user}"
        self.LOG.info(backup_cmd)
        exec_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.LOG.info(exec_msg)
        self.assertIn('ERROR', exec_msg)

    def tearDown(self):
        self.LOG.info('---步骤6:删除新建目录---')
        clear_cmd = f'rm -rf {self.gs_probackup_bak_path}'
        self.LOG.info(clear_cmd)
        clear_msg = self.Primary_User_Node.sh(clear_cmd).result()
        self.LOG.info(clear_msg)

        self.LOG.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0187 end----')
