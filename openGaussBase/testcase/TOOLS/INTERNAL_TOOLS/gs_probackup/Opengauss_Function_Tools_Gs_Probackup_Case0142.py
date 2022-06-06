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
Case Name   : 使用gs_probackup add-instance命令添加--remote-proto=none参数
Description :
    1.创建备份目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.查看是否生成pg_probackup.conf配置文件
    5.清理环境
Expect      :
    1.创建成功
    2.初始化成功
    3.初始化新的备份实例成功
    4.生成pg_probackup.conf配置文件，该文件保存了指定数据目录pgdata-path的
    gs_probackup设置
    5.清理环境完成
History     :
"""

import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Tools_Gs_Probackup_Case0142start-')
        self.constant = Constant()
        self.Primary_Node = Node('PrimaryDbUser')
        self.gs_probackup_path = os.path.join(macro.DB_INSTANCE_PATH,
                                              'gs_probackup_testdir0142')

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

        text = '-step3:在备份路径内初始化一个新的备份实例;' \
               'expect:初始化新的备份实例成功-'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance  " \
                   f"-B {self.gs_probackup_path} " \
                   f"-D {macro.DB_INSTANCE_PATH} " \
                   f"--instance=test_0142 " \
                   f"--remote-proto=none;"
        self.log.info(init_cmd)
        init_msg = self.Primary_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn("'test_0142' " + self.constant.init_success, init_msg,
                      '执行失败:' + text)

        text = '---step4:查看pg_probackup.conf配置文件;' \
               'expect:配置文件添加数据目录成功---'
        self.log.info(text)
        cat_cmd = f"cat {self.gs_probackup_path}/backups/" \
                  f"test_0142/pg_probackup.conf"
        self.log.info(cat_cmd)
        cat_msg = self.Primary_Node.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.assertIn(f'pgdata = {macro.DB_INSTANCE_PATH}', cat_msg,
                      '执行失败:' + text)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.gs_probackup_path}'
        self.log.info(clear_cmd)
        clear_msg = self.Primary_Node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.log.info('-Opengauss_Function_Tools_Gs_Probackup_Case0142finish-')
