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
    2.导出数据成功
    3.清理环境成功
History     :
    modified：2022/1/10 by 5318639 优化用例适配新代码
"""
import os
import unittest

from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Tools_gs_dumpall_Case0033_start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.dumpall_path = os.path.join(macro.DB_INSTANCE_PATH, 'dumpall_qm')
        self.key = f'12345678@qaz'
        self.t_name = 't_dump_0033'

    def test_server_tools(self):
        text = '----step1:创建测试数据;expect:构造成功----'
        self.log.info(text)
        sql_cmd1 = f'''
            drop table if exists {self.t_name}; 
            create table {self.t_name} (id int ,name char(10));
            insert into {self.t_name} values (1,'aa'),(2,'bb');
            '''
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd1}"'
        self.log.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1, '执行失败:' + text)

        text = '----step2:导出数据需用AES128进行加密，指定密钥;expect:导出成功----'
        self.log.info(text)
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_dumpall -p {self.dbuser_node.db_port} ' \
            f'-f {self.dumpall_path} ' \
            f'--with-encryption=AES128 ' \
            f'--with-key={self.key};'
        self.log.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        self.log.info(msg2)
        self.assertIn(self.constant.gs_dumpall_success_msg, msg2,
                      '执行失败:' + text)

    def tearDown(self):
        text = '----step3:清理环境;expect:清理成功----'
        self.log.info(text)
        sql_cmd2 = f'drop table if exists {self.t_name};'
        clear_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd2}";'
        self.log.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        excute_cmd3 = f'rm -rf {self.dumpall_path};'
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, clear_msg,
                      '执行失败:' + text)
        self.assertEqual('', msg3, '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_gs_dumpall_Case0033_finish----')
