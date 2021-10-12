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
Case Name   :  JdbcGsBackup -m xx，-s指定模式（自定义模式）,多个模式间使用
               其他符号分隔
Description :
        1.创建数据库
        2.指定数据库下建表，建用户
        3.修改表的schema
        4.修改信任方式为sha256
        4.导出指定数据库,添加-s选项,多个schema间使用分号分隔
        5.删表后执行导入
        6.查看导入表
        7.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.修改成功
        4.schema1导出成功，schema2和schema3未导出
        5.schema1导入成功
        6.schema1下的表导入成功，数据正确
        7.清理环境完成
History     :
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
            '---Opengauss_Function_JdbcGsBackup_Case0029start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')
        self.db_name = "gs_db03"
        self.user = "us_03"
        self.tb_name = "t_03"
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
        result = self.Primary_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '')
        self.log.info('---获取openGauss-tools-backup工具包---')
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL}; '''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result)
        self.log.info('---解压工具包---')
        sql_cmd = f'''cd {self.package};
            tar -zxvf openGauss-tools-backup.tar.gz; '''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)

        self.log.info('-----创建数据库----')
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        self.log.info('---在指定数据库下创建测试用户和schema---')
        sql_cmd = f'''drop schema if  exists schema1;
            drop schema if  exists schema2;
            drop schema if  exists schema3;
            create schema  schema1;
            create schema  schema2;
            create schema  schema3;
            drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, sql_result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result)

        self.log.info('---在指定数据库下在创建表并修改表的schema---')
        sql_cmd = '''drop table if  exists pgbackup_t1;
            drop table if  exists  pgbackup_t2;
            drop table if  exists  pgbackup_t3;
            create table pgbackup_t1 (id int);
            insert into pgbackup_t1 values(1),(2),(3);
            create table pgbackup_t2 (id int);
            insert into pgbackup_t2 values(8),(2),(5);
            create table pgbackup_t3 (id int);
            insert into pgbackup_t3 values(9),(6),(3);
            alter table pgbackup_t1 set schema schema1;
            alter table pgbackup_t2 set schema schema2;
            alter table pgbackup_t3 set schema schema3;'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result)
        self.assertIn(self.constant.ALTER_TABLE_MSG, sql_result)

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

        self.log.info('---导出，-s指定多个模式用分号分隔--')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m dump \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s schema1;schema2;schema3 '''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('bash: schema2: command not found' and
                      'bash: schema3: command not found',  msg)

        self.log.info('---删表后执行导入---')
        sql_cmd = f'''drop table schema1.pgbackup_t1;
            drop table schema2.pgbackup_t2;
            drop table schema3.pgbackup_t3;'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_result)
        self.log.info('---导入---')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m restore \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s schema1;schema2;schema3 \
            -n schema1;schema2;schema3 '''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('bash: schema2: command not found' and
                      'bash: schema3: command not found', msg)
        self.log.info('---查询schema1下的表---')
        sql_cmd = f'''select * from schema1.pgbackup_t1;'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('3 rows', sql_result)
        self.log.info('---查询schema2和schema3下的表---')
        sql_cmd = f'''select * from schema2.pgbackup_t2;
            select * from schema2.pgbackup_t2;'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('ERROR', sql_result)

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
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            drop user if exists {self.user} cascade;''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0029finish---')
