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
Case Type   : 服务端工具
Case Name   : 备份/还原操作是否影响导出(gs_probackup)
Description :
    1.会话1创建大量数据
    2.创建备份文件保存路径
    mkdir /data/probackup;
    3.初始化备份路径backup-path中的备份目录,该目录将存储已备份的内容
    gs_probackup init -B /data//probackup;
    4.在备份路径backup-path内初始化一个新的备份实例，并生成pg_probackup.conf配置文件,
    该文件保存了指定数据目录pgdata-path的gs_probackup设置
    gs_probackup add-instance -B /data/probackup
    -D /data/cluster/dn1 --instance=node
    5.在会话1执行导出操作
    gs_dump databasename -p port -f /data/dump1;
    6.在会话1执行导出操作的同时在会话2执行备份操作
    gs_probackup backup -B /data/probackup --instance=node -b full;
    7.再次在会话1执行导出操作
    gs_dump databasename -p 18987 -f /data/qumin/dump1;
    8.在会话2执行导出操作的同时在会话2执行还原操作
    gs_probackup restore -B /data/probackup --instance=node;
    9.清理环境
    drop database databasename;
    rm -rf /data/dump1;
    rm -rf /data/probackup;
Expect      :
    1.数据创建成功
    2.备份路径创建成功
    3.初始化备份路径成功
    4.初始化一个新的备份实例成功
    5.导出数据成功
    6.备份成功
    7.导出成功
    8.还原成功
    9.清理成功
History     :
"""
import os
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-------Opengauss_Function_Tools_gs_dump_Case0113start------')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.Primary_Node1 = Node('PrimaryDbUser')
        self.Primary_Node2 = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.com = Common()
        self.dump_path1 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump1.sql')
        self.dump_path2 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump2.sql')
        self.gs_probackup_path1 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'gs_probackup113_01')
        self.gs_probackup_path2 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'gs_probackup113_02')
        self.db_name = "db_dump0113"
        self.tb_name = "t_dump0113"

    def test_tools_dump(self):
        text = '-------step1:创建测试数据;expect:创建成功--------'
        self.log.info(text)
        text = '----------step1.1:创建数据库;expect:创建成功-----------'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''
            drop database if exists {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        text = '-------step1.2:在创建的数据库中创建表和数据;expect:创建成功--------'
        self.log.info(text)
        sql_cmd = f'''drop table if  exists {self.tb_name};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values (generate_series(1,1000000));'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = '-------step2:创建备份路径;expect:创建成功-------'
        self.log.info(text)
        is_dir_exists_cmd1 = f'''if [ ! -d "{self.gs_probackup_path1}" ]
                                   then
                                       mkdir {self.gs_probackup_path1}
                                   fi'''
        self.log.info(is_dir_exists_cmd1)
        result1 = self.Primary_Node1.sh(is_dir_exists_cmd1).result()
        self.log.info(result1)
        self.log.info(text)
        is_dir_exists_cmd2 = f'''if [ ! -d "{self.gs_probackup_path2}" ]
                                           then
                                               mkdir {self.gs_probackup_path2}
                                           fi'''
        self.log.info(is_dir_exists_cmd2)
        result2 = self.Primary_Node1.sh(is_dir_exists_cmd2).result()
        self.log.info(result2)
        text = '-------step3:初始化备份路径backup-path中的备份目录;expect:导出成功-------'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup init -B {self.gs_probackup_path1};"
        self.log.info(init_cmd)
        init_msg = self.Primary_Node1.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        text = '-----step4:在备份路径backup-path内初始化一个新的备份实例，' \
               '并生成pg_probackup.conf配置文件;expect:备份成功-----'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance " \
            f"-B {self.gs_probackup_path1} " \
            f"-D {macro.DB_INSTANCE_PATH} " \
            f"--instance=probackup113; "
        self.log.info(init_cmd)
        init_msg = self.Primary_Node1.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn("'probackup113' " + self.constant.init_success,
                      init_msg)
        self.log.info('---------查看pg_probackup.conf配置文件--------')
        cat_cmd = f"cat {self.gs_probackup_path1}/backups/" \
            f"probackup113/pg_probackup.conf"
        self.log.info(cat_cmd)
        cat_msg = self.Primary_Node1.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.assertIn(f'pgdata = {macro.DB_INSTANCE_PATH}', cat_msg)

        text = '-----step5:在会话1执行导出操作;expect:备份成功-----'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name} \
            -p {self.Primary_Node1.db_port} \
            -f {self.dump_path1};
            '''
        self.log.info(dump_cmd)
        connect_thread1 = ComThread(
            self.com.get_sh_result, args=(self.Primary_Node1, dump_cmd))
        connect_thread1.setDaemon(True)
        connect_thread1.start()

        text = '-----step6:在会话1执行导出操作的同时在会话2执行备份操作;expect:备份成功-----'
        self.log.info(text)
        gs_probackup_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_probackup backup ' \
            f'-B {self.gs_probackup_path1} ' \
            f'--instance=probackup113 ' \
            f'-b full ' \
            f'-d {self.Primary_Node2.db_name} ' \
            f'-p {self.Primary_Node2.db_port} ;'
        self.log.info(gs_probackup_cmd)
        connect_thread2 = ComThread(
            self.com.get_sh_result,
            args=(self.Primary_Node2, gs_probackup_cmd))
        connect_thread2.setDaemon(True)
        connect_thread2.start()
        self.log.info('-----------获取session1结果-----------')
        connect_thread1.join(180)
        thread1_result = connect_thread1.get_result()
        self.log.info(thread1_result)
        self.assertIn(f'dump database {self.db_name} successfully',
                      thread1_result,
                      '执行失败:' + text)
        self.log.info('-----------获取session2结果-----------')
        connect_thread2.join(180)
        thread2_result = connect_thread2.get_result()
        self.log.info(thread2_result)
        self.assertIn('completed', thread2_result)
        self.backupid = thread2_result.splitlines()[-1].split()[2]
        self.log.info(self.backupid)
        self.log.info('备份ID为：' + self.backupid)
        self.assertIn('pg_stop backup() successfully executed',
                      thread2_result,
                      '执行失败:' + text)

        text = '---step7:再次在会话1执行导出操作;expect:导出成功---'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
                    gs_dump {self.db_name} \
                    -p {self.Primary_Node1.db_port} \
                    -f {self.dump_path2};
                    '''
        self.log.info(dump_cmd)
        connect_thread1 = ComThread(
            self.com.get_sh_result, args=(self.Primary_Node1, dump_cmd))
        connect_thread1.setDaemon(True)
        connect_thread1.start()

        text = '-----step8:在会话1执行导出操作的同时在会话2执行备份还原操作;expect:还原成功-----'
        self.log.info(text)
        gs_probackup_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_probackup restore ' \
            f'-B {self.gs_probackup_path1} ' \
            f'--instance=probackup113 ' \
            f'-D {self.gs_probackup_path2} ' \
            f'-d {self.Primary_Node2.db_name} ' \
            f'-p {self.Primary_Node2.db_port} ;'
        self.log.info(gs_probackup_cmd)
        connect_thread2 = ComThread(
            self.com.get_sh_result,
            args=(self.Primary_Node2, gs_probackup_cmd))
        connect_thread2.setDaemon(True)
        connect_thread2.start()
        self.log.info('-----------获取session1结果-----------')
        connect_thread1.join(180)
        thread1_result = connect_thread1.get_result()
        self.log.info(thread1_result)
        self.assertIn(f'dump database {self.db_name} successfully',
                      thread1_result,
                      '执行失败:' + text)
        self.log.info('-----------获取session2结果-----------')
        connect_thread2.join(120)
        thread2_result = connect_thread2.get_result()
        self.log.info(thread2_result)
        self.assertIn(f'Restore of backup {self.backupid} completed',
                      thread2_result, '执行失败:' + text)

    def tearDown(self):
        text = '--------------step9:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.dump_path1};' \
            f'rm -rf {self.dump_path2};' \
            f'rm -rf {self.gs_probackup_path1};' \
            f'rm -rf {self.gs_probackup_path2};'
        self.log.info(rm_cmd)
        result = self.Root_Node.sh(rm_cmd).result()
        self.log.info(result)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop database if exists  {self.db_name};')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_gs_dump_Case0113finish------')
