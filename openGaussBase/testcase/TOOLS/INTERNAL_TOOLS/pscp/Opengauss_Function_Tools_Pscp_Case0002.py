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
Case Name   : pscp工具复制本地文件至远程机器
Description :
    1.主节点创建文件并写入内容
    2.使用pscp -H将主节点文件复制到备节点，-H指定备1节点ip
    3.查看备机文件
    4.查看结果文件和错误结果文件
    5.清理环境
Expect      :
    1.创建成功
    2.复制成功
    3.复制成功，文件存在，内容正确
    4.文件为空
    5.清理环境完成
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
        self.log.info('-Opengauss_Function_Tools_Pscp_Case0002开始执行-')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.Standby_User_Node = Node('Standby1DbUser')
        self.IP1 = self.Standby_User_Node.db_host
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.pscp_path = os.path.join(self.parent_path, 'tool', 'script',
                                      'gspylib', 'pssh', 'bin')
        self.output_file = os.path.join(self.parent_path, 'output.log')
        self.generate_file = os.path.join(self.output_file, self.IP1)
        self.err_output_file = os.path.join(self.parent_path,
                                            'err_output.log')
        self.generate_err_file = os.path.join(self.err_output_file, self.IP1)
        self.file_path = os.path.join(self.parent_path, 'f_pscp_case0002')

    def test_pscp(self):
        text = '--step1:主节点创建文件并写入内容;expect:创建成功--'
        self.log.info(text)
        touch_cmd = f"rm -rf {self.file_path};" \
                    f"touch {self.file_path};" \
                    f"echo 'database' > {self.file_path}"
        self.log.info(touch_cmd)
        msg = self.PrimaryNode.sh(touch_cmd).result()
        self.log.info(msg)
        self.assertEqual('', msg, '执行失败:' + text)

        text = '--step2:使用pscp -H将主节点文件复制到备节点，-H指定备1' \
               '节点ip;expect:复制成功--'
        self.log.info(text)
        pscp_cmd = f" cd {self.pscp_path};" \
                   f"source {macro.DB_ENV_PATH};" \
                   f"python3 pscp -H {self.Standby_User_Node.db_host} " \
                   f"-t 3 " \
                   f"-p 2 " \
                   f"-o {self.output_file} " \
                   f"-e {self.err_output_file} " \
                   f"-i " \
                   f"{self.file_path} {self.parent_path};"
        self.log.info(pscp_cmd)
        msg = self.PrimaryNode.sh(pscp_cmd).result()
        self.log.info(msg)
        self.assertIn('SUCCESS', msg, '执行失败:' + text)

        text = '--step3:查看备机文件;expect:复制成功，文件存在，内容正确--'
        self.log.info(text)
        ls_cmd = f"ls {self.parent_path} | grep f_pscp_case0002;" \
                 f"cat {self.file_path}"
        self.log.info(ls_cmd)
        msg = self.Standby_User_Node.sh(ls_cmd).result()
        self.log.info(msg)
        self.assertTrue('f_pscp_case0002' in msg, '执行失败:' + text)
        self.assertIn('database', msg, '执行失败:' + text)

        text = '--step4:查看结果文件和错误结果文件;expect:文件为空--'
        self.log.info(text)
        cat_cmd = f"cat {self.generate_file};" \
                  f"cat {self.generate_err_file}"
        self.log.info(cat_cmd)
        msg = self.PrimaryNode.sh(cat_cmd).result()
        self.log.info(msg)
        self.assertEqual('', msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step5:清理环境;expect:清理环境成功--'
        self.log.info(text)
        rm_cmd = f"rm -rf {self.output_file};" \
                 f"rm -rf {self.err_output_file};" \
                 f"rm -rf {self.file_path}"
        self.log.info(rm_cmd)
        msg1 = self.PrimaryNode.sh(rm_cmd).result()
        self.log.info(msg1)
        rm_cmd = f"rm -rf {self.file_path}"
        self.log.info(rm_cmd)
        msg2 = self.Standby_User_Node.sh(rm_cmd).result()
        self.log.info(msg2)
        self.log.info('断言teardown执行成功')
        self.assertEqual('', msg1, '执行失败:' + text)
        self.assertEqual('', msg2, '执行失败:' + text)
        self.log.info('-Opengauss_Function_Tools_Pscp_Case0002执行完成-')
