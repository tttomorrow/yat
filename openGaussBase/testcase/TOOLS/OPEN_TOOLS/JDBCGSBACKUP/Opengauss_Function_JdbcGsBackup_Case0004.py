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
Case Name   : 创建与表关联的序列，使用jdbcgsbackup -m dump导出以及导入
Description :
        1.创建工具所在目录
        2.获取openGauss-tools-backup工具包
        3.创建数据库，表，用户
        4.修改本机信任方式为sha256
        5.导出
        6.删表，删序列后执行导入
        7.查询表数据
        8.清理环境
Expect      :
        1.创建成功
        2.获取成功
        3.创建成功
        4.修改成功
        5.导出成功
        6.导入成功
        7.查询成功，数据一致
        8.清理环境完成
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
            '---Opengauss_Function_JdbcGsBackup_Case0004start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')
        self.tb_name = "t_03"
        self.db_name = "gs_db03"
        self.user = "us_03"
        self.seq = 's_04'
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

        self.log.info('---创建数据库；在创建的库下建用户，建表，建序列---')
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        self.log.info('---在创建的库下建用户，建表，建序列---')
        sql_cmd = f'''drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';
            drop table if exists {self.tb_name};
            create table {self.tb_name} (id int ,name varchar(20));
            insert into {self.tb_name} values (1,'aa'),(2,'bb');
            drop sequence if exists {self.seq};
            create sequence {self.seq} start with 1 increment by 1 no \
            minvalue no maxvalue cache 1;
            alter table {self.tb_name} alter column id set default \
            nextval('{self.seq}');
            insert into {self.tb_name} values \
            (nextval('{self.seq}'),'《本色》');'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result)
        self.assertIn(self.constant.CREATE_SEQUENCE_SUCCESS_MSG, sql_result)

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

        self.log.info('---导出指定数据库---')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar  \
            -d {self.db_name} \
            -m dump  \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U  {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public'''
        self.log.info(sql_cmd)
        msg = self.Root_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.jdbcgsbackup_success, msg)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], msg)

        self.log.info('--删表,删除序列后执行导入--')
        sql_cmd = f'''drop table if exists {self.tb_name} cascade;
            drop sequence if exists {self.seq}'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar  \
            -m restore  \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public \
            -n public'''
        self.log.info(sql_cmd)
        msg = self.Root_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.jdbcgsbackup_success, msg)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], msg)

        self.log.info('---验证导入成功--')
        sql_cmd = f'''insert into {self.tb_name} values \
            (nextval('s_04'),'《意向值》');
            select * from {self.tb_name} where id =2;'''
        excute_cmd = f'''source {self.DB_ENV_PATH};\
            gsql -d {self.db_name} \
            -p {self.Primary_Node.db_port} \
            -c "{sql_cmd}"'''
        self.log.info(excute_cmd)
        msg = self.Primary_Node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)
        msg_list = msg.splitlines()
        self.log.info(msg_list)
        self.assertEqual('2 | 《意向值》', msg_list[-2].strip())

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
            drop user if exists {self.user};''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0004finish---')
