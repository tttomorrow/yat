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
Case Name   : pssh工具远程连接备机并输出备节点主机名
Description :
    1.pssh -H 添加所有参数，远程连接备节点并输出备节点主机名
    2.查看执行结果文件
    3.查看错误结果文件
    4.pssh -H 添加所有参数，远程连接备节点并输出备节点主机名,命令错误
    5.查看执行结果文件
    6.查看错误结果文件
    7.清理环境
Expect      :
    1.执行成功；屏幕显示备1节点主机名
    2.结果文件显示备节点主机名
    3.错误结果文件为空
    4.合理报错
    5.结果文件为空
    6.错误结果文件显示报错提示信息
    7.清理环境完成
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Tools_Pssh_Case0002开始执行-')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.Standby_User_Node = Node('Standby1DbUser')
        self.IP1 = self.Standby_User_Node.db_host
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.pssh_path = os.path.join(self.parent_path, 'tool', 'script',
                                      'gspylib', 'pssh', 'bin')
        self.output_file = os.path.join(self.parent_path, 'output.log')
        self.generate_file = os.path.join(self.output_file, self.IP1)
        self.err_output_file = os.path.join(self.parent_path, 'err_output.log')
        self.generate_err_file = os.path.join(self.err_output_file, self.IP1)
        self.expect_result = "bash: hostname123: command not found"

    def test_pssh(self):
        text = '--step1:pssh -H 添加所有参数，远程连接备节点并输出备节点' \
               '主机名;expect:执行成功；屏幕显示备1节点主机名--'
        self.log.info(text)
        cmd = 'hostname'
        check_hostname = self.Standby_User_Node.sh(cmd).result()
        self.log.info(check_hostname)
        pssh_cmd = f" cd {self.pssh_path};" \
                   f"source {macro.DB_ENV_PATH};" \
                   f"python3 pssh " \
                   f"-H {self.Standby_User_Node.db_host} " \
                   f"-t 5 " \
                   f"-p 2 " \
                   f"-o {self.output_file} " \
                   f"-e {self.err_output_file} " \
                   f"-P " \
                   f"-s " \
                   f"-i  'echo $HOSTNAME';"
        self.log.info(pssh_cmd)
        msg = self.PrimaryNode.sh(pssh_cmd).result()
        self.log.info(msg)
        self.assertEqual(check_hostname, msg.splitlines()[-1].strip(),
                         '执行失败:' + text)

        text = '--step2:查看执行结果文件;expect:结果文件显示备节点主机名--'
        self.log.info(text)
        cat_cmd = f"cat {self.generate_file}"
        self.log.info(cat_cmd)
        msg = self.PrimaryNode.sh(cat_cmd).result()
        self.log.info(msg)
        self.assertEqual(check_hostname, msg, '执行失败:' + text)

        text = '--step3:查看错误结果文件;expect:错误结果文件为空--'
        self.log.info(text)
        cat_cmd = f"cat {self.generate_err_file}"
        self.log.info(cat_cmd)
        msg = self.PrimaryNode.sh(cat_cmd).result()
        self.log.info(msg)
        self.assertEqual('', msg, '执行失败:' + text)

        text = '--step4:pssh -H 添加所有参数，远程连接备节点并输出备节点' \
               '主机名,命令错误;expect:合理报错--'
        self.log.info(text)
        pssh_cmd = f" cd {self.pssh_path};" \
                   f"source {macro.DB_ENV_PATH};" \
                   f"python3 pssh " \
                   f"-H {self.Standby_User_Node.db_host} " \
                   f"-t 5 " \
                   f"-p 2 " \
                   f"-o {self.output_file} " \
                   f"-e {self.err_output_file} " \
                   f"-P " \
                   f"-s " \
                   f"-i hostname123;"
        self.log.info(pssh_cmd)
        msg = self.PrimaryNode.sh(pssh_cmd).result()
        self.log.info(msg)
        self.assertTrue(self.expect_result in msg, '执行失败:' + text)

        text = '--step5:查看执行结果文件;expect:结果文件为空--'
        self.log.info(text)
        cat_cmd = f"cat {self.generate_file}"
        self.log.info(cat_cmd)
        msg = self.PrimaryNode.sh(cat_cmd).result()
        self.log.info(msg)
        self.assertEqual('', msg, '执行失败:' + text)

        text = '--step6:查看错误结果文件;expect:错误结果文件显示报错提示信息--'
        self.log.info(text)
        cat_cmd = f"cat {self.generate_err_file}"
        self.log.info(cat_cmd)
        msg = self.PrimaryNode.sh(cat_cmd).result()
        self.log.info(msg)
        self.assertTrue(self.expect_result in msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step7:清理环境;expect:清理环境完成--'
        self.log.info(text)
        rm_cmd = f"rm -rf {self.output_file};" \
                 f"rm -rf {self.err_output_file}"
        self.log.info(rm_cmd)
        msg = self.PrimaryNode.sh(rm_cmd).result()
        self.log.info(msg)
        self.log.info('断言teardown执行成功')
        self.assertEqual('', msg, '执行失败:' + text)
        self.log.info('-Opengauss_Function_Tools_Pssh_Case0002执行完成-')
