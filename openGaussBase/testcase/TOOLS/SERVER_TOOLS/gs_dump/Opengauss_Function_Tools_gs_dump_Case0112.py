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
Case Name   : 备份/还原操作是否影响导出(gs_basebackup)
Description :
    1.会话1创建大量数据
    2.创建备份文件保存路径
    mkdir /data/qumin/backup;
    3.在会话1执行导出操作
    gs_dump database -p port -f /data/dump1;
    4.在会话1执行导出操作的同时在会话2执行备份操作
    gs_basebackup -D /data/backup;
    5.清理环境
    drop database database;
    rm -rf /data/dump1;
    rm -rf /data/dump2;
    rm -rf /data/backup;
Expect      :
    1.数据创建成功
    2.备份路径创建成功
    3.导出数据成功
    4.备份成功
    5.清理成功
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
            '-------Opengauss_Function_Tools_gs_dump_Case0112start------')
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
        self.gs_basebackup_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'gs_backup')
        self.db_name = "db_dump0112"
        self.tb_name = "t_dump0112"

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
        is_dir_exists_cmd = f'''if [ ! -d "{self.gs_basebackup_path}" ]
                                       then
                                           mkdir {self.gs_basebackup_path}
                                       fi'''
        self.log.info(is_dir_exists_cmd)
        result = self.Primary_Node1.sh(is_dir_exists_cmd).result()
        self.log.info(result)

        text = '-------step3:在会话1执行导出操作;expect:导出成功-------'
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

        text = '-----step4.在会话1执行导出操作的同时在会话2执行备份操作;expect:备份成功-----'
        self.log.info(text)
        gs_basebackup_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_basebackup ' \
            f'-D {self.gs_basebackup_path} ' \
            f'-p {self.Primary_Node2.db_port};'
        self.log.info(gs_basebackup_cmd)
        connect_thread2 = ComThread(
            self.com.get_sh_result,
            args=(self.Primary_Node2, gs_basebackup_cmd))
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
        self.assertIn(self.constant.gs_basebackup_success_msg,
                      thread2_result,
                      '执行失败:' + text)

    def tearDown(self):
        text = '--------------step5:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.dump_path1};' \
            f'rm -rf {self.dump_path2};' \
            f'rm -rf {self.gs_basebackup_path};'
        self.log.info(rm_cmd)
        result = self.Root_Node.sh(rm_cmd).result()
        self.log.info(result)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop database if exists  {self.db_name};')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_gs_dump_Case0112finish------')
