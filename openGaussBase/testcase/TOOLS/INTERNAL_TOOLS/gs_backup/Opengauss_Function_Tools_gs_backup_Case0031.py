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
Case Type   : 基础功能
Case Name   :主机执行gs_backup -l指定已存在文件进行恢复，日志存放文件是否会将信息写入
Description :
    1.在$GAUSSLOG路径下创建文件并写入内容（内容随意）
    2.指定参数-l执行gs_backup
    3.查看主机与备机对应目录，日志是否写入指定文件并覆盖文件内容
    4.删除新建文件
Expect      :
    1.文件创建成功，写入内容成功
    2.指定参数-l执行gs_backup成功
    3.查看主机与备机对应目录，日志未写入指定文件，而是产生了新的文件，未覆盖文件内容
    4.删除新建文件成功
History     :
"""
import unittest
import os
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
commonshpri = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == commonshpri.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class Backupclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_gs_backup_Case0031 start")
        self.constant = Constant()
        
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.backup_path = os.path.join(self.parent_path, 'base_backup')
        self.primary_user_node = Node(node='PrimaryDbUser')
        self.sta1_user_node = Node(node='Standby1DbUser')
        self.file_path = os.path.join(macro.GAUSSDB_LOG_PATH,
                                      'test_case0031.log')

        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_backup -t backup --backup-dir={self.backup_path} --all"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.constant.gs_backup_success, result)

    def test_backup0026(self):
        text = '--step1: 在$GAUSSLOG路径下创建文件并写入内容（内容随意） expect:文件创建成功，写入内容成功--'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"touch {self.file_path};" \
            f"echo 'test to test' > {self.file_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        text = '----step2: 指定参数-l执行gs_backup expect:指定参数-l执行gs_backup成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_backup -t restore --backup-dir={self.backup_path} " \
            f" -l {self.file_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.constant.gs_backup_restore_success, result,
                      '执行失败:' + text)

        text = '--step3:查看主机与备机对应目录，日志是否写入指定文件并覆盖文件内容 ' \
               'expect:查看主机与备机对应目录，日志未写入指定文件，而是产生了新的文件，未覆盖文件内容----'
        self.log.info(text)
        cmd = f"ls {macro.GAUSSDB_LOG_PATH};" \
            f"cat {self.file_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('gs_local', result, '执行失败:' + text)
        self.assertEqual(result.count('test_case0031'), 2, '执行失败:' + text)
        result = self.sta1_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('gs_local', result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"rm -rf {self.backup_path};" \
            f"rm -rf {self.file_path};" \
            f"rm -rf {os.path.join(macro.GAUSSDB_LOG_PATH, 'gs_local*')};" \
            f"rm -rf {os.path.join(macro.GAUSSDB_LOG_PATH, 'test_case0031*')}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        result = self.sta1_user_node.sh(cmd).result()
        self.log.info(result)
        self.log.info("-Opengauss_Function_Tools_gs_backup_Case0031 end-")
