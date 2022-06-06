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
Case Name   : 导出数据需用AES128进行加密，不指定密钥
Description :
    1.创建数据
    2.导出数据需用AES128进行加密，不指定密钥
    3.清理环境
Expect      :
    1.创建数据成功
    2.输入密码导出成功
    3.清理环境成功
History     :
    modified：2022/1/21 by 5318639 优化用例断言
"""
import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Tools_gs_dumpall_Case0032_start----')
        self.dbuser_node = Node('dbuser')
        self.root_node = Node('default')
        self.constant = Constant()
        self.dumpall_file = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dumpall.sql')
        self.dumpall_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH))
        self.key = f'12345678@qaz'
        self.t_name = 't_dump_0032'

    def test_server_tools(self):
        text = '----step1:创建测试数据;expect:创建成功----'
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
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1,
                      '执行失败:' + text)

        text = '----step2:导出数据需用AES128进行加密，不指定密钥;expect:输入密码导出成功----'
        self.log.info(text)
        dumpall_cmd = f'''source {macro.DB_ENV_PATH};
                expect <<EOF
                set timeout -1
                spawn gs_dumpall -p {self.dbuser_node.db_port} \
                --with-encryption=AES128 -f {self.dumpall_file}
                expect "*Key:"
                send "{macro.GAUSSDB_INIT_USER_PASSWD}\n"
                expect eof\n''' + "EOF"
        self.log.info(dumpall_cmd)
        dumpall_result1 = self.dbuser_node.sh(dumpall_cmd).result()
        self.log.info(dumpall_result1)
        du_cmd = f'cd {self.dumpall_path};du -h {self.dumpall_file};'
        self.log.info(du_cmd)
        du_msg = self.dbuser_node.sh(du_cmd).result()
        self.log.info(du_msg)
        dumpall_result2 = float(du_msg.split()[0][:-1])
        self.log.info(dumpall_result2)
        self.assertGreater(dumpall_result2, 0, '执行失败:' + text)

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
        rm_cmd = f'rm -rf {self.dumpall_file};'
        rm_msg = self.root_node.sh(rm_cmd).result()
        self.assertEqual('', rm_msg, '执行失败:' + text)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, clear_msg,
                      '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_gs_dumpall_Case0032_finish----')
