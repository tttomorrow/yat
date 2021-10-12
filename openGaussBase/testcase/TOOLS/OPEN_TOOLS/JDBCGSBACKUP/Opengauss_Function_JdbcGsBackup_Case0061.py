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
Case Name   : failover后，新主节点执行导出/导入，-h指定新备节点
Description :
        1.执行failover
        2.新主节点创建工具所在目录
        3.获取openGauss-tools-backup工具包并解压
        4.新主节点创建数据库
        5.指定数据库下建表，建用户
        6.修改信任方式为sha256
        7.导出指定数据库
        8.删表
        9.导入
        10.清理环境
Expect      :
        1.failover成功
        2.创建成功
        3.解压成功
        4.创建成功
        5.创建成功
        6.修改成功
        7.导出成功
        8.删除成功
        9.导入报错ERROR: cannot execute CREATE TABLE in a read-only
        transaction
        10.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class ToolsBackup(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0061start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Standby_SH = CommonSH('Standby1DbUser')
        self.Primary_Node = Node('PrimaryDbUser')
        self.Standby_Node = Node('Standby1DbUser')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_tool')
        self.db_name = "db_jdbcgsbackup_0061"
        self.user = "u_jdbcgsbackup_0061"
        self.tb_name = "t_jdbcgsbackup_0061"

    def test_tools_backup(self):
        text = '-----step1:执行failover;expect:failover成功----'
        self.log.info(text)
        result = COMMONSH.stop_db_instance()
        self.log.info(result)
        self.assertIn("server stopped", result, '执行失败:' + text)
        result = self.Standby_SH.execute_gsctl('failover',
                                               'failover completed')
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        result = self.Standby_SH.exec_refresh_conf()
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        result = self.Standby_SH.restart_db_cluster()
        self.log.info(result)
        result = self.Standby_SH.get_db_cluster_status('detail')
        self.log.info(result)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败:' + text)

        text = '----step2:新主节点创建工具所在目录;expect:创建成功----'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Standby_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '',  '执行失败:' + text)

        text = '----step3:获取openGauss-tools-backup工具包并解压 ' \
               'expect:解压成功----'
        self.log.info(text)
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL};
            cd {self.package};
            tar -zxvf openGauss-tools-backup.tar.gz;'''
        self.log.info(sql_cmd)
        result = self.Standby_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result,  '执行失败:' + text)

        text = '----step4:创建数据库 expect:创建成功----'
        self.log.info(text)
        sql_cmd = self.Standby_SH.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '----step5:在指定数据库下创建测试用户和表;expect:创建成功----'
        self.log.info(text)
        sql_cmd = f'''drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';
            drop table if exists {self.tb_name};
            create table {self.db_name} (id int);
            insert into {self.db_name} values (generate_series(1,100));'''
        self.log.info(sql_cmd)
        sql_result = self.Standby_SH.execut_db_sql(sql=sql_cmd,
                                                   dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = '----step6:备份新备机pg_hba.conf文件并修改新主节点的认证方式;' \
               'expect:修改成功----'
        self.log.info(text)
        cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}  " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')}"
        self.log.info(cmd)
        msg = self.Primary_Node.sh(cmd).result()
        self.log.info(msg)
        cmd = f"grep -nr '127.0.0.1/32' " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        line = self.Primary_Node.sh(
            cmd).result().splitlines()[0].split(':')[0]
        self.log.info(line)
        cmd = f'sed -i "{str(int(line)+1)} ihost   all     all ' \
              f'{self.Standby_Node.db_host}/32   sha256" ' \
              f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")}; ' \
              f'cat {os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")};'
        self.log.info(cmd)
        result = self.Primary_Node.sh(cmd).result()
        self.log.info(result)
        self.assertIn(f'{self.Standby_Node.db_host}/32   sha256',  result,
                      '执行失败:' + text)

        text = '----step7:新主节点执行导出，-h指定新备节点;expect:导出成功----'
        self.log.info(text)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m dump \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public '''
        self.log.info(sql_cmd)
        msg = self.Standby_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.jdbcgsbackup_success, msg,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], msg,
                         '执行失败:' + text)

        text = '----step8:删表 expect:删表成功----'
        self.log.info(text)
        sql_cmd = f'''drop table if exists {self.tb_name};'''
        self.log.info(sql_cmd)
        sql_result = self.Standby_SH.execut_db_sql(sql=sql_cmd,
                                                   dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_result,
                      '执行失败:' + text)

        text = '----step9:导入,-h指定新备节点 expect:导入报错----'
        self.log.info(text)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m restore \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public \
            -n public '''
        self.log.info(sql_cmd)
        msg = self.Standby_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR: cannot execute CREATE TABLE in a read-only '
                      'transaction', msg, '执行失败:' + text)

    def tearDown(self):
        text = '----step10:清理环境 expect:清理环境完成----'
        self.log.info(text)
        sql_cmd = f'''rm -rf {self.package};'''
        self.log.info(sql_cmd)
        result = self.Standby_Node.sh(sql_cmd).result()
        self.log.info(result)
        cmd = f"rm -rf " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};" \
              f"mv " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')} " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        self.Primary_Node.sh(cmd)
        sql_cmd = self.Standby_SH.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            drop user if exists {self.user} cascade;''')
        self.log.info(sql_cmd)
        result = COMMONSH.execute_gsctl('switchover',
                                        'switchover completed')
        self.log.info(result)
        self.assertTrue(result)
        result = COMMONSH.exec_refresh_conf()
        self.log.info(result)
        self.assertTrue(result)
        result = COMMONSH.get_db_cluster_status('detail')
        self.log.info(result)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败:' + text)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0061finish---')
