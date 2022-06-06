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
Case Name   : 使用gs_probackup set-config命令指定--log-level-console=error、
              --log-level-file=verbose、
              --log-filename=gs_probackup-%Y-%m-%d_%H%M%S.log、
              --error-log-filename=gs_probackup_error.log、
              --log-directory=<绝对路径>
Description :
    1.创建备份目录和日志文件的目录
    2.进行初始化
    3.添加远程实例
    4.修改配置
    5.查看备份目录中的pg_probackup.conf配置文件的内容
    6.恢复环境
Expect      :
    1.创建成功
    2.初始化成功
    3.添加成功
    4.修改成功
    5.显示备份文件日志详情
    6.恢复环境完成
History     :
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
        self.gs_probackup_path = os.path.join(macro.DB_INSTANCE_PATH,
                                              'gs_probackup_testdir0198')
        self.gs_probackup_log = os.path.join(macro.DB_INSTANCE_PATH,
                                             'gs_probackup_log0198')
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0198 start----')

    def test_server_tools(self):
        text = '--step1:创建备份目录和日志文件的目录;expect:创建成功----'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_path}" ]
                        then
                            mkdir -p {self.gs_probackup_path}
                        fi'''
        self.log.info(mkdir_cmd)
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.log.info(primary_result)
        self.assertEqual(primary_result, '', '执行失败:' + text)
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_log}" ]
                        then
                            mkdir -p {self.gs_probackup_log}
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

        text = '--step3:添加远程实例;expect:添加成功----'
        self.log.info(text)
        add_cmd = f"source {macro.DB_ENV_PATH};" \
                  f"gs_probackup add-instance " \
                  f"-B {self.gs_probackup_path} " \
                  f"-D {macro.DB_INSTANCE_PATH} " \
                  f"--instance=test_0198 "
        self.log.info(add_cmd)
        exec_msg = self.Primary_User_Node.sh(add_cmd).result()
        self.log.info(exec_msg)
        self.assertIn("'test_0198' " + self.constant.init_success, exec_msg,
                      '执行失败:' + text)

        text = '--step4:修改配置;expect:修改成功----'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup set-config " \
                     f"-B {self.gs_probackup_path} " \
                     f"--instance=test_0198 " \
                     f"--log-level-console=error " \
                     f"--log-level-file=verbose " \
                     f"--log-filename=gs_probackup-%Y-%m-%d_%H%M%S.log " \
                     f"--error-log-filename='gs_probackup_error.log' " \
                     f"--log-directory={self.gs_probackup_log}"
        self.log.info(backup_cmd)
        exec_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.log.info(exec_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], exec_msg,
                         '执行失败:' + text)

        text = '--step5:查看备份目录中的pg_probackup.conf配置文件的内容;' \
               'expect:显示备份文件日志详情----'
        self.log.info(text)
        add_cmd = f"source {macro.DB_ENV_PATH};" \
                  f"gs_probackup show-config " \
                  f"-B {self.gs_probackup_path} " \
                  f"--instance=test_0198 "
        self.log.info(add_cmd)
        exec_msg = self.Primary_User_Node.sh(add_cmd).result()
        self.log.info(exec_msg)
        self.assertIn(f'log-directory = {self.gs_probackup_log}',
                      exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step6:恢复环境;expect:恢复环境完成--'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.gs_probackup_path};' \
                 f'rm -rf {self.gs_probackup_log}'
        self.log.info(rm_cmd)
        clear_msg = self.Primary_User_Node.sh(rm_cmd).result()
        self.log.info(clear_msg)
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0198 end----')
