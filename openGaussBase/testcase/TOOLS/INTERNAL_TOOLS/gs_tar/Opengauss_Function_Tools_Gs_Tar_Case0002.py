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
Case Name   : gs_basebackup指定压缩级别备份后使用gs_tar直接解压
Description :
    1.新建备份目录与解压目录
    2.指定压缩级别进行备份
    3.使用gs_tar进行解压
    4.使用解压目录启动数据库
    5.恢复数据库
Expect      :
    1.新建备份目录与解压目录成功
    2.指定压缩级别进行备份成功
    3.使用gs_tar进行解压成功
    4.使用解压目录启动数据库成功
    5.恢复数据库成功
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
        self.log.info("Opengauss_Function_Tools_Gs_Tar_Case0002 start")
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

    def test_tar0002(self):
        try:
            text = '----step1: 新建备份目录与解压目录 expect:新建备份目录与解压目录成功----'
            self.log.info(text)
            cmd = f"mkdir {self.backup_path}; mkdir {self.tar_path}"
            self.log.info(cmd)
            result = self.primary_user_node.sh(cmd).result()
            self.log.info(result)
            cmd = f"ls {self.parent_path}"
            result = self.primary_user_node.sh(cmd).result()
            self.log.info(result)
            self.assertIn('base_backup', result, '执行失败:' + text)
            self.assertIn('base_dn1', result, '执行失败:' + text)

            text = '----step2: 指定压缩级别进行备份 expect:指定压缩级别进行备份成功----'
            self.log.info(text)
            cmd = f"source {macro.DB_ENV_PATH};" \
                f"gs_basebackup -D {self.backup_path}  -Ft -X fetch -p " \
                f"{self.primary_user_node.db_port} -l " \
                f"gauss.bak -P -Z5 -v -U " \
                f"{self.primary_user_node.db_user} -w"
            self.log.info(cmd)
            result = self.primary_user_node.sh(cmd).result()
            self.log.info(result)
            self.assertIn(self.constant.gs_basebackup_success_msg, result,
                          '执行失败:' + text)

            text = '----step3: 使用gs_tar进行解压 expect:使用gs_tar进行解压成功----'
            self.log.info(text)
            cmd = f"source {macro.DB_ENV_PATH};" \
                f"gzip -d {os.path.join(self.backup_path, 'base.tar.gz')};" \
                f"gs_tar -D {self.tar_path}  " \
                f"-F {os.path.join(self.backup_path, 'base.tar')};"
            self.log.info(cmd)
            result = self.primary_user_node.sh(cmd).result()
            self.log.info(result)
            self.assertIn('', result, '执行失败:' + text)

            text = '----step4: 使用解压目录启动数据库 expect:使用解压目录启动数据库成功----'
            self.log.info(text)
            result = self.commonshpri.execute_gsctl(
                'stop', self.constant.GS_CTL_STOP_SUCCESS_MSG, '-t 300')
            self.assertTrue(result, '执行失败:' + text)
            cmd = f"chmod -R 700 {self.tar_path};" \
                f"source {macro.DB_ENV_PATH};" \
                f"gs_ctl start -D {self.tar_path} -M primary"
            self.log.info(cmd)
            result = self.primary_user_node.sh(cmd).result()
            self.log.info(result)
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result,
                          '执行失败:' + text)
        finally:
            text = '----step5: 恢复数据库 expect:恢复数据库成功----'
            self.log.info(text)
            cmd = f"source {macro.DB_ENV_PATH};" \
                f"gs_ctl stop -D {self.tar_path} -t 300"
            result = self.primary_user_node.sh(cmd).result()
            self.log.info(result)
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, result,
                          '执行失败:' + text)
            result = self.commonshpri.start_db_instance()
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result,
                          '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"rm -rf {self.backup_path}; rm -rf {self.tar_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.commonshpri.start_db_instance()
        self.log.info('-----------还原wal_sender_timeout------------------')
        self.commonshpri.execute_gsguc('reload',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f'wal_sender_timeout='
                                       f'{self.wal_sender_timeout}')

        self.log.info("-Opengauss_Function_Tools_Gs_Tar_Case0002 end-")
