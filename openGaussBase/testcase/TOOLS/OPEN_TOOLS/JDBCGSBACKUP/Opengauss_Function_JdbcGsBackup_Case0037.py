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
Case Name   : 创建约束触发器后，使用jdbcgsbackup -m dump导出指定数据库
Description :
        1.创建工具所在目录
        2.获取openGauss-tools-backup工具包
        3.解压工具包
        4.创建数据库
        5.在创建的库下建用户，建表
        6.配置主节点pg_hba.conf文件
        7.导出指定数据库
        8.删表
        9.导入
        10.查询导入数据
        11.清理环境
Expect      :
        1.创建成功
        2.获取成功
        3.解压成功
        4.创建成功
        5.创建成功
        6.配置成功
        7.导出成功
        8.删除成功
        9.导入报错
        10.数据正确
        11.清理环境完成
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
            '---Opengauss_Function_JdbcGsBackup_Case0037start---')
        self.constant = Constant()
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_tools')
        self.tb_name = "tb_jdbcgsbackup_case0037"
        self.tb_name_01 = "tb_jdbcgsbackup_case0037_01"
        self.func_name = "func_jdbcgsbackup_case0037"
        self.db_name = "db_jdbcgsbackup_case0037"
        self.user = "us_jdbcgsbackup_case0037"
        self.log.info('---备份pg_hba.conf文件---')
        cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}  " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')}"
        self.log.info(cmd)
        msg = self.Primary_Node.sh(cmd).result()
        self.log.info(msg)

    def test_tools_backup(self):
        text = '--step1:创建工具所在目录;expect:创建成功---'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Primary_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '--step2:获取openGauss-tools-backup工具包;expect:获取成功---'
        self.log.info(text)
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL}; '''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result, '执行失败:' + text)

        text = '---step3:解压工具包;expect:解压成功---'
        self.log.info(text)
        sql_cmd = f'''cd {self.package};
            tar -zxvf openGauss-tools-backup.tar.gz; '''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn('openGauss-tools-backup', result, '执行失败:' + text)

        text = '--step4:创建数据库;expect:创建成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '--step5:在创建的库下建用户，建表;expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';
            drop table if exists {self.tb_name};
            drop table if exists {self.tb_name_01};
            create table {self.tb_name}(id1 int, id2 int, id3 int);
            create table {self.tb_name_01}(id1 int, id2 int, id3 int);
            create or replace function {self.func_name}() returns trigger as
            \$\$
            declare
            begin
             insert into {self.tb_name_01} values(new.id1, new.id2, new.id3);
            return new;
            end
           \$\$ language plpgsql;
           create constraint trigger insert_trigger01 after insert on \
           {self.tb_name} for each row execute procedure {self.func_name}();
           insert into {self.tb_name} values(100,200,300);'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertTrue(self.constant.CREATE_ROLE_SUCCESS_MSG in sql_result
                        and self.constant.TABLE_CREATE_SUCCESS in sql_result,
                        '执行失败:' + text)

        text = 'step6:---配置主节点pg_hba.conf文件;expect:配置成功---'
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

        text = '---step7:导出指定数据库;expect:导出成功---'
        self.log.info(text)
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
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.jdbcgsbackup_success, msg,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], msg,
                         '执行失败:' + text)

        text = '--step8:删表;expect:删除成功--'
        self.log.info(text)
        sql_cmd = f'''drop table if exists {self.tb_name};\
            drop table if exists {self.tb_name_01};'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('DROP TABLE', sql_result, '执行失败:' + text)

        text = '---step9:导入;expect:导入报错---'
        self.log.info(text)
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
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(f'error executing sql: ALTER TABLE {self.tb_name} '
                      f'ADD CONSTRAINT insert_trigger01 TRIGGER', msg,
                      '执行失败:' + text)

        text = '---step10:查询表;expect:表不存在--'
        self.log.info(text)
        sql_cmd = f'''select count(*) from {self.tb_name};
            select count(*) from {self.tb_name_01};'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('ERROR', sql_result, '执行失败:' + text)

    def tearDown(self):
        text = '---step11:清理环境;expect:清理环境完成---'
        self.log.info(text)
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
            '---Opengauss_Function_JdbcGsBackup_Case0037finish---')
