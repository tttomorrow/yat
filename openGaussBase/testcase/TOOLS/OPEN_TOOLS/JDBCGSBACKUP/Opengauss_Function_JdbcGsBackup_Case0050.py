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
Case Name   : jdbcgsbackup -m restore 添加-n选项指定模式与导出时指定模式长度
             不同，合理报错
Description :
        1.创建工具目录
        2.获取工具安装包并解压
        3.创建数据库
        4.指定数据库下创建测试用户;创建模式；建表并修改表的模式
        5.修改信任方式为sha256
        6.导出指定数据库
        7.删除表
        8.导入时-n的模式名与导出时-s后的模式名不匹配
        9.清理环境
Expect      :
        1.创建成功
        2.解压成功
        3.创建成功
        4.创建成功
        5.修改成功
        6.导出成功
        7.删除成功
        8.导入报错
        9.清理环境完成
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
            '---Opengauss_Function_JdbcGsBackup_Case0050start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_tool')
        self.db_name = "db_jdbcgsbackup0050"
        self.user = "u_jdbcgsbackup0050"
        self.tb_name = "t_jdbcgsbackup0050"
        self.tb_name_01 = "t_jdbcgsbackup0050_01"
        self.tb_name_02 = "t_jdbcgsbackup0050_02"
        self.sc_name = "sc_jdbcgsbackup0050"
        self.sc_name_01 = "sc_jdbcgsbackup0050_01"
        self.sc_name_02 = "sc_jdbcgsbackup0050_02"
        text = '---备份pg_hba.conf文件---'
        self.log.info(text)
        cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}  " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')}"
        self.log.info(cmd)
        msg = self.Primary_Node.sh(cmd).result()
        self.log.info(msg)

    def test_tools_backup(self):
        text = '---step1:创建工具所在目录;expect:创建成功---'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Primary_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '---step2:获取openGauss-tools-backup工具包并解压;' \
               'expect:解压成功---'
        self.log.info(text)
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL};
                            cd {self.package};
                            tar -zxvf openGauss-tools-backup.tar.gz;'''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result, '执行失败:' + text)

        text = '---step3:创建数据库;expect:创建成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '---step4:创建测试用户;创建模式；建表并修改表的模式;' \
               'expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';
            drop schema if exists {self.sc_name} cascade;
            drop schema if exists {self.sc_name_01} cascade;
            drop schema if exists {self.sc_name_02} cascade;
            create schema {self.sc_name};
            create schema {self.sc_name_01};
            create schema {self.sc_name_02};
            drop table if exists {self.tb_name};
            drop table if exists {self.tb_name_01};
            drop table if exists {self.tb_name_02};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values(1),(2),(3);
            create table {self.tb_name_01} (id int);
            insert into {self.tb_name_01} values(8),(2),(5);
            create table {self.tb_name_02} (id int);
            insert into {self.tb_name_02} values(9),(6),(3);
            alter table {self.tb_name} set schema {self.sc_name};
            alter table {self.tb_name_01} set schema {self.sc_name_01};
            alter table {self.tb_name_02} set schema {self.sc_name_02};'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = 'step5:---修改信任方式为sha256;expect:修改成功---'
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
        self.assertIn(f'{self.Primary_Node.db_host}/32   sha256', result,
                      '执行失败:' + text)

        text = '---step6:导出;expect:导出成功---'
        self.log.info(text)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m dump \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s {self.sc_name},{self.sc_name_01},{self.sc_name_02}'''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.jdbcgsbackup_success, msg,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], msg,
                         '执行失败:' + text)

        text = '---step7:删除表;expect:删除成功---'
        self.log.info(text)
        sql_cmd = f'''drop table {self.sc_name}.{self.tb_name};
            drop table {self.sc_name_01}.{self.tb_name_01};
            drop table {self.sc_name_02}.{self.tb_name_02};'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_result,
                      '执行失败:' + text)

        text = '---step8:导入时-n的模式名与导出时-s后的模式名不匹配;' \
               'expect:报错---'
        self.log.info(text)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m restore \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s {self.sc_name},{self.sc_name_01},{self.sc_name_02} \
            -n {self.sc_name}'''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('backup failed', msg)

        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m restore \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s {self.sc_name},{self.sc_name_01},{self.sc_name_02} \
            -n {self.sc_name},{self.sc_name_01}'''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('backup failed', msg)

    def tearDown(self):
        self.log.info('---清理环境---')
        sql_cmd = f'''rm -rf {self.package};'''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
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
            '---Opengauss_Function_JdbcGsBackup_Case0050finish---')
