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
Case Type   : openGauss-tools-backup
Case Name   : 初始用户使用JdbcGsBackup -m dump导出指定数据库，合理报错
Description :
        1.创建工具所在目录
        2.获取openGauss-tools-backup工具包
        3.解压工具包
        4.创建数据库
        5.在创建的库下建表
        6.初始用户导出指定数据库
        7.配置pg_hba文件白名单
        8.初始用户导出指定数据库
        9.清理环境
Expect      :
        1.创建成功
        2.获取成功
        3.解压成功
        4.成功
        5.创建成功
        6.合理报错,FATAL: Forbid remote connection with trust method!
        7.成功
        8.合理报错，FATAL: Forbid remote connection with initial user
        9.清理环境完成
              用例复制postgresql.jar包步骤;
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class ToolsBackup06(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.log.info('-----os.path.basename(__file__)} start-----')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')
        self.tb_name = "tb_jdbcgsbackup_0006"
        self.db_name = "db_jdbcgsbackup_0006"

    def test_tools_backup(self):
        text = '---step1:创建工具所在目录;expect:成功---'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Root_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '---step2:获取openGauss-tools-backup工具包;expect:成功---'
        self.log.info(text)
        sql_cmd = f"wget -P {self.package} {macro.PACKAGE_URL};"
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result)

        text = '---step3:解压工具包;expect:成功---'
        self.log.info(text)
        sql_cmd = f"cd {self.package};" \
                  f"tar -zxvf openGauss-tools-backup.tar.gz;"
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn('openGauss-tools-backup', result, '执行失败:' + text)

        text = '---step4:创建数据库;expect:成功------'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop database if exists "
                                            f"{self.db_name};"
                                            f"create database {self.db_name};")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '---step5:在创建的库下建表;expect:成功---'
        self.log.info(text)
        sql_cmd = f"drop table if exists {self.tb_name};" \
                  f"create table {self.tb_name} (id int ,name varchar(10));" \
                  f"insert into {self.tb_name} values (1,'aa'),(2,'bb');"
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)

        text = '---step6:初始用户导出指定数据库;expect:合理报错---'
        self.log.info(text)
        backup_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar  \
            -m dump \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U  {self.Primary_Node.ssh_user} \
            -P {self.Primary_Node.ssh_password} \
            -s public'''
        self.log.info(backup_cmd)
        backup_res = self.Root_Node.sh(backup_cmd).result()
        self.log.info(backup_res)
        self.assertIn('FATAL: Forbid remote connection with trust method!',
                      backup_res, '执行失败:' + text)

        text = '---step7:配置pg_hba文件白名单;expect:成功---'
        self.log.info(text)
        guc_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
            {self.db_name}  {self.Primary_Node.ssh_user}  \
            {self.Primary_Node.db_host}/32  sha256";'''
        self.log.info(guc_cmd)
        guc_res = self.Primary_Node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败:' + text)

        text = '---step8:初始用户导出指定数据库;expect:合理报错---'
        self.log.info(text)
        backup_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar  \
            -m dump \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U  {self.Primary_Node.ssh_user} \
            -P {self.Primary_Node.ssh_password} \
            -s public'''
        self.log.info(backup_cmd)
        backup_res = self.Root_Node.sh(backup_cmd).result()
        self.log.info(backup_res)
        self.assertIn('FATAL: Forbid remote connection with initial user',
                      backup_res, '执行失败:' + text)

    def tearDown(self):
        text = '---step9:清理环境;expect:成功---'
        self.log.info(text)
        rm_cmd = f"rm -rf {self.package};"
        self.log.info(rm_cmd)
        rm_result = self.Root_Node.sh(rm_cmd).result()
        self.log.info(rm_result)
        guc_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_guc reload -D {macro.DB_INSTANCE_PATH} -h "host  \
            {self.db_name}  {self.Primary_Node.ssh_user}  \
            {self.Primary_Node.db_host}/32";'''
        self.log.info(guc_cmd)
        guc_res = self.Primary_Node.sh(guc_cmd).result()
        self.log.info(guc_res)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop database if exists "
                                            f"{self.db_name};")
        self.log.info(sql_cmd)
        self.log.info('断言teardown成功')
        self.assertEqual(len(rm_result), 0, '执行失败:' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败:' + text)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.log.info('-----os.path.basename(__file__)} end-----')
