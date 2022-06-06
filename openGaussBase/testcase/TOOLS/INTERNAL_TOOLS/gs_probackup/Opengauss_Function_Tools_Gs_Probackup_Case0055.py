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
Case Name   : 指定合并过期备份，要保留的备份副本数，指定--merge-expired、
              --retention-redundancy选项，执行备份
Description :
    1.创建备份目录
    2.进行初始化
    3.添加实例
    4.执行备份
    5.清理环境
Expect      :
    1.创建成功
    2.初始化成功
    3.添加成功
    4.备份成功
    5.清理环境完成
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
        self.log = Logger()
        self.log.info('--Opengauss_Function_Tools_Gs_Probackup_Case0055start-')
        self.constant = Constant()
        self.Primary_Node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.gs_probackup_path = os.path.join(macro.DB_INSTANCE_PATH,
                                              'gs_probackup_testdir0055')
        self.slot_name = "slot_gs_probackup_case0055"

    def test_system_internal_tools(self):
        text = '--step1:创建备份目录;expect:创建成功----'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_path}" ]
                        then
                            mkdir -p {self.gs_probackup_path}
                        fi'''
        primary_result = self.Primary_Node.sh(mkdir_cmd).result()
        self.log.info(primary_result)
        self.assertEqual(primary_result, '', '执行失败:' + text)

        text = '--step2:进行初始化;expect:初始化成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_path};"
        self.log.info(init_cmd)
        init_msg = self.Primary_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg,
                      '执行失败:' + text)

        text = '--step3:添加实例;expect:添加成功----'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_path} " \
                   f"-D {macro.DB_INSTANCE_PATH} " \
                   f"--instance=test_0055 "
        self.log.info(init_cmd)
        init_msg = self.Primary_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn("'test_0055' " + self.constant.init_success, init_msg,
                      '执行失败:' + text)

        text = '---step4:执行备份;expect:备份成功---'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_probackup backup -B {self.gs_probackup_path} " \
                     f"-b full  --stream  --instance=test_0055  " \
                     f"-p {self.Primary_Node.db_port} " \
                     f"-d postgres  " \
                     f"--merge-expired  " \
                     f"--retention-redundancy=10"
        self.log.info(backup_cmd)
        backup_msg = self.Primary_Node.sh(backup_cmd).result()
        self.log.info(backup_msg)
        self.assertIn('completed', backup_msg, '执行失败:' + text)

    def tearDown(self):
        text = '---step5:清理环境;清理环境完成---'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.gs_probackup_path}'
        self.log.info(clear_cmd)
        clear_msg = self.Primary_Node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.log.info('-Opengauss_Function_Tools_Gs_Probackup_Case0055finish-')
