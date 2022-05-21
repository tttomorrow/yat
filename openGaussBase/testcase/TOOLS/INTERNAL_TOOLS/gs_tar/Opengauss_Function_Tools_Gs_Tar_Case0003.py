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
Case Name   : gs_tar解压目录已存在但不为空
Description :
    1.新建备份目录与解压目录,在解压目录下创建空文件
    2.进行备份
    3.使用gs_tar进行解压
Expect      :
    1.新建备份目录与解压目录成功
    2.进行备份成功
    3.解压失败
History     :
"""
import unittest
import os
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class Tarclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_Gs_Tar_Case0003 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.backup_path = os.path.join(self.parent_path, 'base_backup')
        self.tar_path = os.path.join(self.parent_path, 'base_dn1')
        self.primary_user_node = Node(node='PrimaryDbUser')

        result = self.commonshpri.execut_db_sql('show wal_sender_timeout;')
        self.log.info(f"wal_sender_timeout is {result}")
        self.wal_sender_timeout = result.strip().splitlines()[-2]

        self.log.info('-----------修改wal_sender_timeout------------------')
        result = self.commonshpri.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            'wal_sender_timeout=12s')
        self.assertTrue(result)

    def test_tar0003(self):
        text = '-step1: 新建备份目录与解压目录,在解压目录下创建空文件 expect:新建备份目录与解压目录成功--'
        self.log.info(text)
        cmd = f"mkdir {self.backup_path}; " \
            f"mkdir -p {os.path.join(self.tar_path, 'test')}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        cmd = f"ls {self.parent_path}"
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('base_backup', result, '执行失败:' + text)
        self.assertIn('base_dn1', result, '执行失败:' + text)

        text = '----step2: 进行备份 expect:进行备份成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_basebackup -D {self.backup_path}  -Ft -X fetch -p " \
            f"{self.primary_user_node.db_port} -l gauss.bak -P -v -U " \
            f"{self.primary_user_node.db_user} -w"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.constant.gs_basebackup_success_msg, result,
                      '执行失败:' + text)

        text = '----step3: 使用gs_tar进行解压 expect:使用gs_tar进行解压成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_tar -D {self.tar_path}  " \
            f"-F {os.path.join(self.backup_path, 'base.tar')};"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('no empty', result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"rm -rf {self.backup_path}; rm -rf {self.tar_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.log.info('-----------还原wal_sender_timeout------------------')
        self.commonshpri.execute_gsguc('reload',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f'wal_sender_timeout='
                                       f'{self.wal_sender_timeout}')

        self.log.info("-Opengauss_Function_Tools_Gs_Tar_Case0003 end-")
