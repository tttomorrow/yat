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
Case Name   : 关闭备数据库，指定参数--parameter执行gs_backup进行恢复,是否只恢复参数文件
Description :
    1.执行gs_backup对参数文件进行备份
    2.更改主备session_timeout参数的数值
    3.删除某个二进制文件
    4.连接数据库确认该参数是否已更改成功
    5.执行gs_backup对参数文件进行恢复
    6.查看主机与备机postgresql.conf文件，参数值是否恢复,查看二进制文件是否恢复（不做重启）
Expect      :
    1.执行gs_backup成功，提示信息为：Successfully backed up cluster files.
    2.更改主备session_timeout参数的数值成功
    3.删除二进制文件成功
    4.连接数据库确认该参数已更改成功
    5.执行gs_backup对参数文件进行恢复成功
    6.参数文件恢复成功，二进制文件恢复失败
History     :
"""
import unittest
import os
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class Backupclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_gs_backup_Case0025 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.backup_path = os.path.join(self.parent_path, 'base_backup')
        self.primary_user_node = Node(node='PrimaryDbUser')
        self.simple_path = "app/share/postgresql/postgresql.conf.sample"

        result = self.commonshpri.execut_db_sql('show session_timeout;')
        self.log.info(f"session_timeout is {result}")
        self.session_timeout = result.strip().splitlines()[-2]

    def test_backup0025(self):
        text = '----step1: 执行gs_backup对参数文件进行备份 expect:执行gs_backup成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_backup -t backup --backup-dir={self.backup_path} --all"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.constant.gs_backup_success, result,
                      '执行失败:' + text)

        text = '-step2: 更改主备session_timeout参数的数值 ' \
               'expect:更改主备session_timeout参数的数值成功-'
        self.log.info(text)
        result = self.commonshpri.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            'session_timeout=12min')
        self.assertTrue(result, '执行失败:' + text)

        text = '----step3: 删除某个二进制文件 expect:删除二进制文件成功----'
        self.log.info(text)
        cmd = f"cp {os.path.join(self.parent_path, self.simple_path)} " \
            f"{os.path.join(self.parent_path, 'test_case0025')};" \
            f"rm -rf {os.path.join(self.parent_path, self.simple_path)}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        text = '----step4: 连接数据库确认该参数是否已更改成功 expect:连接数据库确认该参数已更改成功----'
        self.log.info(text)
        result = self.commonshpri.execut_db_sql('show session_timeout;')
        self.log.info(result)
        self.assertIn("12min", result, '执行失败:' + text)

        text = '----step5: 执行gs_backup对参数文件进行恢复 ' \
               'expect:执行gs_backup对参数文件进行恢复成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_backup -t restore --backup-dir={self.backup_path} " \
            f"--parameter"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.constant.gs_backup_restore_success, result,
                      '执行失败:' + text)

        text = '--step6: 查看主机与备机postgresql.conf文件，参数值是否恢复,查看二进制文件是否恢复（不做重启） ' \
               'expect:参数文件恢复成功，二进制文件恢复失败----'
        self.log.info(text)
        cmd = f"cat " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'postgresql.conf')} " \
            f"| grep session_timeout"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(self.session_timeout, result, '执行失败:' + text)
        cmd = f"ls " \
            f"{os.path.join(self.parent_path, 'app/share/postgresql')} | " \
            f"grep postgresql.conf.sample"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertNotIn("postgresql.conf.sample", result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"mv {os.path.join(self.parent_path, 'test_case0025')} " \
            f"{os.path.join(self.parent_path, self.simple_path)};" \
            f"rm -rf {self.backup_path}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.log.info('-----------还原session_timeout------------------')
        self.commonshpri.execute_gsguc('reload',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f'session_timeout='
                                       f'{self.session_timeout}')
        self.log.info("-Opengauss_Function_Tools_gs_backup_Case0025 end-")
