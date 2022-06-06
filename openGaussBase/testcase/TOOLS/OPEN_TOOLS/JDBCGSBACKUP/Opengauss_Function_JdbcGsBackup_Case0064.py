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
Case Name   : 主节点导出过程中停止主节点，-h备节点
Description :
        1.创建工具所在目录
        2.获取工具安装包并解压
        3.创建数据库
        4.指定数据库下建用户，建表
        5.修改备节点pg_hba.conf文件
        6.主节点导出，-h备节点，导出过程停止主节点
        7.重启集群
        8.删除表后执行导入
        9.清理环境
Expect      :
        1.创建成功
        2.解压成功
        3.创建成功
        4.创建成功
        5.修改成功
        6.主节点导出，-h备节点，停止主节点，导出成功；停止主节点成功
        7.重启集群成功
        8.导入报错ERROR: cannot execute CREATE TABLE in a read-only transaction
        9.清理环境完成
"""
import os
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
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
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0064start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Standby_Node = Node('Standby1DbUser')
        self.com = Common()
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_tool')
        self.db_name = "db_jdbcgsbackup_0064"
        self.user = "u_jdbcgsbackup_0064"
        self.tb_name = "t_jdbcgsbackup_0064"
        text = '---备份备节点pg_hba.conf文件---'
        self.log.info(text)
        cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}  " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')}"
        self.log.info(cmd)
        msg = self.Standby_Node.sh(cmd).result()
        self.log.info(msg)

    def test_tools_backup(self):
        text = '----step1:创建工具所在目录;expect:创建成功----'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Primary_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '----step2:获取openGauss-tools-backup工具包并解压 ' \
               'expect:解压成功----'
        self.log.info(text)
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL};
            cd {self.package};
            tar -zxvf openGauss-tools-backup.tar.gz;'''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result, '执行失败:' + text)

        text = '-----step3:创建数据库;expect:创建成功----'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '---step4:创建测试用户,创建表;expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';
            drop table if  exists {self.tb_name};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values (generate_series(1,1000000));'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = '---step5:修改备节点pg_hba.con文件;expect:修改成功---'
        self.log.info(text)
        cmd = f"grep -nr '127.0.0.1/32' " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        line = self.Standby_Node.sh(
            cmd).result().splitlines()[0].split(':')[0]
        self.log.info(line)
        cmd = f'sed -i "{str(int(line)+1)} ihost   all     all ' \
              f'{self.Primary_Node.db_host}/32   sha256" ' \
              f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")}; ' \
              f'cat {os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")};'
        self.log.info(cmd)
        result = self.Standby_Node.sh(cmd).result()
        self.log.info(result)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertIn(f'{self.Primary_Node.db_host}/32   sha256', result,
                      '执行失败:' + text)

        text = '---step6:主节点导出时停止主节点，-h备节点;expect:导出成功---'
        self.log.info(text)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m dump \
            -d {self.db_name} \
            -h {self.Standby_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public'''
        self.log.info(sql_cmd)
        connect_thread1 = ComThread(
            self.com.get_sh_result, args=(Node('PrimaryDbUser'), sql_cmd))
        connect_thread1.setDaemon(True)
        connect_thread1.start()

        text = '---step6.1:停止主节点;expect:停止成功---'
        self.log.info(text)
        result = self.pri_sh.stop_db_instance()
        self.assertTrue(result, '执行失败:' + text)

        text = '---step6.2:获取step6结果;expect:导出成功---'
        self.log.info(text)
        connect_thread1.join(60 * 10)
        thread1_result = connect_thread1.get_result()
        self.log.info(thread1_result)
        self.assertIn(self.constant.jdbcgsbackup_success, thread1_result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], thread1_result,
                         '执行失败:' + text)

        text = '---step7:重启集群并检查数据库状态;expect:重启集群成功-- '
        self.log.info(text)
        result = self.pri_sh.restart_db_cluster()
        self.log.info(result)
        result = self.pri_sh.get_db_cluster_status('detail')
        self.log.info(result)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败:' + text)

        text = '---step8:删除表导入step6结果;expect:导入报错---'
        self.log.info(text)
        sql_cmd = f'''drop table {self.tb_name};'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m restore \
            -d {self.db_name} \
            -h {self.Standby_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public \
            -n public'''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR: cannot execute CREATE TABLE in a read-only '
                      'transaction', msg, '执行失败:' + text)

    def tearDown(self):
        text = 'step9:---清理环境;expect:清理环境完成---'
        self.log.info(text)
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
        self.Standby_Node.sh(cmd)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            drop user if exists {self.user} cascade;''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0064finish---')
