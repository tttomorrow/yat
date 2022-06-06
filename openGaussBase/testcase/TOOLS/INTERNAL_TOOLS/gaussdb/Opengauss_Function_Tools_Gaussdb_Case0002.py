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
Case Name   : 使用gaussdb工具同时运行两个gaussdb进程
Description :
    1.初始化一个数据库&关闭正在运行的数据库
    2.查看进程，确定关闭成功
    3.启动第一个数据库
    4.启动第二个数据库
    5.查看进程，两个数据库是否都启动
Expect      :
    1.成功
    2.查看进程成功，数据库已关闭
    3.启动第一个数据库gaussdb进程成功
    4.启动第二个数据库gaussdb进程成功
    5.查看进程成功，两个数据库gaussdb进程都已启动
History     :
"""
import unittest
import os
import time
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread


class Gaussdbclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_Gaussdb_Case0002 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.primary_user_node = Node(node='PrimaryDbUser')
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.backup_path = os.path.join(self.parent_path, 'base_backup')

    def test_gaussdb(self):
        text = '----step1: 初始化一个数据库&关闭正在运行的数据库 expect:成功----'
        self.log.info(text)
        result = self.commonshpri.stop_db_cluster()
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_initdb -D {self.backup_path} " \
            f"-w \"{macro.PASSWD_INITIAL}\" " \
            f"--nodename='{self.primary_user_node.db_user}'"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.backup_path, result, '执行失败:' + text)

        text = '-step2: 查看进程，确定关闭成功 expect:查看进程成功，数据库已关闭-'
        self.log.info(text)
        cmd = f"ps ux | grep {self.parent_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('', result, '执行失败:' + text)

        start_thread = []
        text = '----step3: 启动第一个数据库 expect:启动第一个数据库gaussdb进程成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gaussdb  -D {macro.DB_INSTANCE_PATH} -p " \
            f"{self.primary_user_node.db_port} -M primary"
        self.log.info(cmd)
        start_thread.append(ComThread(
            self.common.get_sh_result,
            args=(self.primary_user_node, cmd)))

        text = '----step4:启动第二个数据库 expect:启动第二个数据库成功-'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gaussdb  -D  {self.backup_path} --single_node"
        self.log.info(cmd)
        start_thread.append(ComThread(
            self.common.get_sh_result,
            args=(self.primary_user_node, cmd)))
        for i in range(2):
            start_thread[i].setDaemon(True)
            start_thread[i].start()
        for i in range(2):
            start_thread[i].join(60)
            result = start_thread[i].get_result()
            self.log.info(result)

        text = '----step5: 查看进程，两个数据库是否都启动 ' \
               'expect:查看进程成功，两个数据库gaussdb进程都已启动----'
        self.log.info(text)
        cmd = f"ps ux"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertEqual(result.count('--single_node'), 2, '执行失败:' + text)
        self.assertEqual(result.count('-M primary'), 2, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = "ps ux | grep 'gaussdb -D'"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        pid1 = result.splitlines()[0].split(' ')[1]
        pid2 = result.splitlines()[1].split(' ')[1]
        cmd = f"kill -9 {pid1} ; kill -9 {pid2}; rm -rf {self.backup_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.commonshpri.start_db_cluster(True)
        self.log.info("-Opengauss_Function_Tools_Gaussdb_Case0002 end-")
