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
Case Name   : jdbcgsbackup -m dump导出指定数据库，省略-d选项，与用户名同名的
              数据库不存在，合理报错
Description :
        1.创建工具所在目录
        2.获取openGauss-tools-backup工具包
        3.postgres数据库下建表并创建用户
        4.修改本机信任方式为sha256
        5.省略-d选项，导出
        6.清理环境
Expect      :
        1.创建成功
        2.获取成功
        3.创建成功
        4.修改成功
        5.合理报错
        6.清理环境完成
              用例复制postgresql.jar包步骤;
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
            '---Opengauss_Function_JdbcGsBackup_Case0002start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.tb_name = "tb_jdbcgsbackup_case0002"
        self.user = "us_jdbcgsbackup_case0002"
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')
        self.pg_hba_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.pg_hba_path_bak = os.path.join(macro.DB_INSTANCE_PATH,
                                            'pg_hba.conf_t_bak')
        text = '---备份主节点pg_hba.conf文件---'
        self.log.info(text)
        cmd = f'''if [ -f "{self.pg_hba_path}" ]
                  then
                      cp {self.pg_hba_path} {self.pg_hba_path_bak}
                  else
                      echo 'ERROR: 执行失败:文件不存在，请检查'
                  fi
                '''
        self.log.info(cmd)
        msg = self.Primary_Node.sh(cmd).result()
        self.log.info(msg)

    def test_tools_backup(self):
        text = '---step1:创建工具所在目录;expect:创建成功--'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then 
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Root_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '--step2:获取openGauss-tools-backup工具包;expect获取完成---'
        self.log.info(text)
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL}; '''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result, '执行失败:' + text)
        self.log.info('---解压工具包---')
        sql_cmd = f'''cd {self.package};
            tar -zxvf openGauss-tools-backup.tar.gz; '''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn('openGauss-tools-backup', result)

        text = '--step3:postgres数据库下建表并创建用户;expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''drop table if exists {self.tb_name};
            create table {self.tb_name} (id int ,name varchar(10));
            insert into {self.tb_name} values (1,'aa'),(2,'bb');
            drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'postgres')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = '--step4:---修改信任方式为sha256;expect:修改成功---'
        self.log.info(text)
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
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '---step5:导出;expect:导出完成---'
        self.log.info(text)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;
            java -jar openGauss-tools-backup.jar  \
            -m dump  \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U  {self.user} \
            -P {macro.COMMON_PASSWD}
            '''
        self.log.info(sql_cmd)
        msg = self.Root_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(f'FATAL: database "{self.user}" does not exist', msg,
                      '执行失败:' + text)

    def tearDown(self):
        text = '---step6:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = f'''rm -rf {self.package};'''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        cmd = f'''if [ -f "{self.pg_hba_path_bak}" ]
                  then
                      if [ -f "{self.pg_hba_path}" ]
                      then
                          rm -rf {self.pg_hba_path}
                          mv {self.pg_hba_path_bak}  {self.pg_hba_path}
                      else
                          echo "原pg_hba.conf文件不存在"
                          mv {self.pg_hba_path_bak}  {self.pg_hba_path}
                      fi
                  else
                      echo 'ERROR: 执行失败:文件不存在，请检查'
                  fi'''
        self.log.info(cmd)
        msg = self.Primary_Node.sh(cmd).result()
        self.log.info(msg)
        sql_cmd = f'''drop table if exists {self.tb_name} cascade;
            drop user if exists {self.user} cascade;'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'postgres')
        self.log.info(sql_result)
        self.assertIn('DROP TABLE', sql_result, '执行失败:' + text)
        self.log.info('---Opengauss_Function_JdbcGsBackup_Case0002finish---')
