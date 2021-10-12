"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : openGauss-tools-backup
Case Name   : JdbcGsBackup工具显示帮助信息
Description :
        1.创建工具所在目录
        2.获取openGauss-tools-backup工具包
        3.执行java -jar xxx --?；java -jar xxx -help
        4.清理环境
Expect      :
        1.创建成功
        2.获取成功
        3.显示工具用法及参数信息
        4.清理环境完成
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class ToolsBackup(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0001start---')
        self.constant = Constant()
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')

    def test_tools_backup(self):
        self.log.info('---创建工具所在目录---')
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Root_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '')

        self.log.info('---获取openGauss-tools-backup工具包---')
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL}; '''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result)

        self.log.info('---解压工具包---')
        sql_cmd = f'''cd {self.package};
            tar -zxvf openGauss-tools-backup.tar.gz;'''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn('openGauss-tools-backup', result)

        self.log.info('---使用--？或者-help查询工具用法---')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;
            java -jar openGauss-tools-backup.jar --?;'''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertTrue(result.find(
            'Usage: JdbcGsBackup -m dump|restore [-h hostname] [-p port] '
            '[-t (timing)] [-d database] [-U user] [-P password] '
            '[-f filename] [-o (schema only)] [-s schema[,schema...]] '
            '[-n schema[,schema...]] [-b batchsize]') > -1)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;
            java -jar openGauss-tools-backup.jar -help;'''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertTrue(result.find(
            'Usage: JdbcGsBackup -m dump|restore [-h hostname] [-p port] '
            '[-t (timing)] [-d database] [-U user] [-P password] '
            '[-f filename] [-o (schema only)] [-s schema[,schema...]] '
            '[-n schema[,schema...]] [-b batchsize]') > -1)

    def tearDown(self):
        self.log.info('---清理环境---')
        sql_cmd = f'''rm -rf {self.package};'''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0001finish---')
