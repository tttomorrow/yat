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
Case Name   : 备份文件已存在，导出文本格式的文件是否导出成功
Description :
    1.连接数据库：
    2.创建数据
    3.退出数据库
    4.source环境变量
    5.备份文件已存在，导出文本格式的文件是否导出成功
    6.连接数据库，清理环境
Expect      :
    1.数据库连接成功
    2.创建数据成功
    3.退出数据库
    4.source环境变量
    5.备份文件已存在，导出文本格式的文件失败
    6.清理环境成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0031start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('----------------连接数据库并创建数据库----------------')
        sql_cmd1 = '''  drop table  if exists t1;
                        drop table  if exists t2;
                        create table t1 (i int,d int );
                        insert into t1 values(1,2),(2,3),(3,4);
                        create table t2 (id int,dd int);
                        insert into t2 values(11,22),(21,34),(31,45);
                                        '''
        excute_cmd1 = f'''      source {macro.DB_ENV_PATH} ;
                            gsql -d {self.dbuser_node.db_name}\
                            -p {self.dbuser_node.db_port} -c "{sql_cmd1}"
                                                '''
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1)
        LOG.info('-----以文本格式导出（文件不存在）-----')
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
                gs_dumpall -p {self.dbuser_node.db_port}\
                 -f {macro.DB_INSTANCE_PATH}/dumpall_qm --dont-overwrite-file;
                              '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.gs_dumpall_success_msg, msg2)
        execute_cmd3 = f'''du -h {macro.DB_INSTANCE_PATH}/dumpall_qm;'''
        msg3 = self.dbuser_node.sh(execute_cmd3).result()
        LOG.info(msg3)
        msg3_list = msg3.split()[0]
        self.assertTrue(float(msg3_list[:-1]) > 0)
        LOG.info('-----备份文件已存在，导出文本格式的文件是否导出成功-----')
        excute_cmd4 = f'''source {macro.DB_ENV_PATH} ;
            gs_dumpall -p {self.dbuser_node.db_port}\
            -f {macro.DB_INSTANCE_PATH}/dumpall_qm --dont-overwrite-file;
                                '''
        LOG.info(excute_cmd4)
        msg4 = self.dbuser_node.sh(excute_cmd4).result()
        LOG.info(msg4)
        self.assertIn('Dumpall File specified already exists', msg4)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd5 = '''  
            drop table if exists t1; 
            drop table if exists t2; 
                          '''
        excute_cmd5 = f'''source {macro.DB_ENV_PATH} ;
                        gsql -d {self.dbuser_node.db_name}\
                        -p {self.dbuser_node.db_port} -c "{sql_cmd5}";
                        rm -rf {macro.DB_INSTANCE_PATH}/dumpall_qm;
                                          '''
        LOG.info(excute_cmd5)
        msg5 = self.dbuser_node.sh(excute_cmd5).result()
        LOG.info(msg5)
        LOG.info('----Opengauss_Function_Tools_gs_dumpall_Case0031finish----')
