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
Case Name   :  JdbcGsBackup -m 命令无效性测试
Description :
        1.创建测试用户
        2.修改信任方式为sha256
        3.导出使用jdbcgsbackup -m dumpall
        4.jdbcgsbackup  -m 不加dump或者restore
        5.清理环境
Expect      :
        1.创建成功
        2.修改成功
        3.合理报错
        4.合理报错
        5.清理环境完成
              用例复制postgresql.jar包步骤
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
            '---Opengauss_Function_JdbcGsBackup_Case0009start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')
        self.user = "us_03"
        self.log.info('---备份pg_hba.conf文件---')
        cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}  " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')}"
        self.log.info(cmd)
        msg = self.Primary_Node.sh(cmd).result()
        self.log.info(msg)

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
            tar -zxvf openGauss-tools-backup.tar.gz; '''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn('openGauss-tools-backup', result)

        self.log.info('---创建测试用户---')
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop user if exists \
            {self.user};
            create user {self.user} password '{macro.COMMON_PASSWD}';''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)

        self.log.info('---修改信任方式为sha256---')
        cmd = f"grep -nr '127.0.0.1/32' " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        line = self.Primary_Node.sh(
            cmd).result().splitlines()[0].split(':')[0]
        self.log.info(line)
        cmd = f'sed -i "{str(int(line)+1)} ihost   all     all ' \
              f'{self.Primary_Node.db_host}/32   sha256" ' \
              f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")}; ' \
              f'cat {os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")};'
        self.log.info(cmd)
        result = self.Primary_Node.sh(cmd).result()
        self.log.info(result)

        self.log.info('---jdbcgsbackup -m dumpall命令---')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m dumpall  \
            -d {self.Primary_Node.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD}\
            -s public'''
        self.log.info(sql_cmd)
        msg = self.Root_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('failed: invalid mode: dumpall', msg)

        self.log.info('---jdbcgsbackup  -m 不加命令---')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar  \
            -d {self.Primary_Node.db_name} \
            -m  \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD}\
            -s public'''
        self.log.info(sql_cmd)
        msg = self.Root_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('invalid parameter', msg)

    def tearDown(self):
        self.log.info('---清理环境---')
        sql_cmd = f'''rm -rf {self.package};'''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        cmd = f"rm -rf " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};" \
              f"mv " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')} " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        self.Primary_Node.sh(cmd)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop user if exists \
            {self.user};''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0009finish---')
