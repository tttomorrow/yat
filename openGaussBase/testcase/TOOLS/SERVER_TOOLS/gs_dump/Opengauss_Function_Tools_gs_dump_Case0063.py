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
    1.创建测试数据
    2.导出数据需用AES128进行加密，不指定密钥
    3.清理环境
Expect      :
    1.创建测试数据成功
    2.输入密码后导出成功
    3.清理环境成功
History     :
    modified：2022/1/11 by 5318639 优化用例适配新代码
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
            '----opengauss_function_tools_gs_dump_case0063_start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.assert_msg = f'have been dumped'
        self.key = f'12345qazxs!'
        self.db_name = 'db_dump_0063'
        self.t_name = 't_dump_0063'

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

        text = '----step2:导出数据需用AES128进行加密，不指定密钥;expect:导出成功----'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};
                expect <<EOF
                set timeout -1
                spawn gs_dump -p {self.dbuser_node.db_port} \
                {self.db_name} --with-encryption=AES128
                expect "*Key:"
                send "{macro.GAUSSDB_INIT_USER_PASSWD}\n"
                expect eof\n''' + "EOF"
        self.log.info(dump_cmd)
        dump_result = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(self.assert_msg, dump_result, '执行失败:' + text)

    def tearDown(self):
        text = '----step3:清理环境;expect:清理成功----'
        self.log.info(text)
        sql_cmd4 = f'drop database if exists {self.db_name};'
        excute_cmd4 = f'''source {macro.DB_ENV_PATH} ;
                gsql -d {self.dbuser_node.db_name}\
                -p {self.dbuser_node.db_port} -c "{sql_cmd4}";
                '''
        self.log.info(excute_cmd4)
        msg4 = self.dbuser_node.sh(excute_cmd4).result()
        self.log.info(msg4)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, msg4,
                      '执行失败:' + text)
        self.log.info(
            '----opengauss_function_tools_gs_dump_case0063_finish----')
