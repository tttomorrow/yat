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
Case Name   : 执行初始化数据库命令gs_initdb：本地用户连接数据库时的认证方法为sha256
Description :
    1.执行命令：
    gs_initdb -D [初始化数据库目录] --nodename=single -W --auth=sha256,需要手动输入密码
    2.清理环境
    删除[初始化数据库目录]：rm -rf [初始化数据库目录]
Expect      :
    1.在[初始化数据库目录]下生成初始化后的文件,pg_hba.conf文件中，认证方法为sha256
    2.清理成功
History     :
"""
import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Initdb_Case0006开始执行----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.constant = Constant()
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH,
                                     'dir_gs_initdb_0006')
        self.pg_file = os.path.join(self.dir_path, macro.PG_HBA_FILE_NAME)

    def test_standby(self):
        text = '----删除初始化目录----'
        self.log.info(text)
        dir_cmd = f"rm -rf {self.dir_path};"
        exec_msg = self.primary_root_node.sh(dir_cmd).result()
        self.log.info(exec_msg)

        step_txt = '----step1:执行gs_initdb命令 expect:在[初始化数据库目录]下生成' \
                   '初始化后的文件,pg_hba.conf文件中，认证方法为sha256----'
        self.log.info(step_txt)
        initdb_cmd1 = f'gs_initdb -D {self.dir_path} --nodename=single -W' \
            f' --auth-host=sha256'
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                   expect <<EOF
                   set timeout 120
                   spawn {initdb_cmd1}
                   expect "Enter new system admin password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect "Enter it again:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        initdb_res = self.primary_node.sh(execute_cmd).result()
        self.log.info(initdb_res)
        self.assertIn(self.constant.initdb_success_msg, initdb_res,
                      '执行失败:' + step_txt)
        ls_msg = self.primary_node.sh(f'ls {self.dir_path}').result()
        self.log.info(ls_msg)
        self.assertTrue(
            macro.DB_PG_CONFIG_NAME in ls_msg and macro.PG_HBA_FILE_NAME
            in ls_msg, '执行失败:' + step_txt)
        pg_msg = self.primary_node.sh(
            f'cat {self.pg_file} |grep "^host";').result()
        self.log.info(pg_msg)
        self.assertTrue(pg_msg.count('sha256') >= 2, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----step2:清理环境----')
        text_1 = '----删除[初始化数据库目录] expect:成功----'
        self.log.info(text_1)
        del_msg = self.primary_root_node.sh(
            f'rm -rf {self.dir_path}').result()
        self.log.info(del_msg)
        self.assertEqual('', del_msg, '执行失败:' + text_1)
        self.log.info(
            '----Opengauss_Function_Gs_Initdb_Case0006执行完成----')
