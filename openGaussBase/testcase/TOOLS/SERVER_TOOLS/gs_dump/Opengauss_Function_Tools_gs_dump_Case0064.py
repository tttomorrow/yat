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
Case Name   : 导出数据需用AES128进行加密，指定密钥
Description :
    1.创建测试数据
    2.导出数据需用AES128进行加密，指定密钥
    3.清理环境
Expect      :
    1.创建测试数据成功
    2.导出成功
    3.清理环境成功
History     :
    modified：2022/1/10 by 5318639 优化用例适配新代码
"""

import os
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----opengauss_function_tools_gs_dump_case0064_start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.dump_path = os.path.join((macro.DB_INSTANCE_PATH), 'dump_qm')
        self.key = f'12345qazxs!'
        self.db_name = 'db_dump_0064'
        self.t_name = 't_dump_0064'

    def test_server_tools(self):
        text = '----step1:创建测试数据;expect:创建成功----'
        self.log.info(text)
        text = '-----step1.1:连接数据库并创建数据库;expect:数据库创建成功-----'
        self.log.info(text)
        sql_cmd1 = f'drop database if exists {self.db_name};' \
            f'create database {self.db_name};'
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd1}"'
        self.log.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1,
                      '执行失败:' + text)
        text = '-----step1.2:在创建好的数据库中创建表插入数据;expect:数据库插入成功-----'
        self.log.info(text)
        sql_cmd2 = f''' 
                drop table  if exists {self.t_name};
                create table {self.t_name} (i int,d int );
                insert into {self.t_name} values(1,2),(2,3),(3,4);
                '''
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd2}"'
        self.log.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        self.log.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2, '执行失败:' + text)

        text = '----step2:转储数据需用AES128进行加密，指定密钥;expect:导出成功----'
        self.log.info(text)
        excute_cmd3 = f'source {macro.DB_ENV_PATH};' \
            f'gs_dump -p {self.dbuser_node.db_port} {self.db_name} ' \
            f'-F p ' \
            f'-f {self.dump_path} ' \
            f'--with-encryption=AES128 ' \
            f'--with-key={self.key};'
        self.log.info(excute_cmd3)
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        self.log.info(msg3)
        execute_cmd4 = f'du -h {self.dump_path};'
        msg4 = self.dbuser_node.sh(execute_cmd4).result()
        self.log.info(msg4)
        msg4_list = msg4.split()[0]
        self.assertTrue(float(msg4_list[:-1]) > 0)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg3, '执行失败:' + text)

    def tearDown(self):
        text = '----step3:清理环境;expect:清理成功----'
        self.log.info(text)
        sql_cmd5 = f'drop database if exists {self.db_name};'
        excute_cmd5 = f'''source {macro.DB_ENV_PATH} ;
                gsql -d {self.dbuser_node.db_name}\
                -p {self.dbuser_node.db_port} -c "{sql_cmd5}";
                '''
        self.log.info(excute_cmd5)
        msg5 = self.dbuser_node.sh(excute_cmd5).result()
        self.log.info(msg5)
        excute_cmd6 = f'rm -rf {self.dump_path};'
        msg6 = self.dbuser_node.sh(excute_cmd6).result()
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, msg5,
                      '执行失败:' + text)
        self.assertEqual('', msg6, '执行失败:' + text)
        self.log.info(
            '----opengauss_function_tools_gs_dump_case0064_finish----')
