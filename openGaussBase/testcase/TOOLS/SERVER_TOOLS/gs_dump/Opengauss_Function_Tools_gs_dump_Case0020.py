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
Case Name   : 导出一个纯文本格式文件时设置压缩比级别
Description :
    1.创建测试数据
    2.导出一个纯文本格式文件时设置压缩比级别
    3.连接数据库，清理环境
Expect      :
    1.创建测试数据成功
    2.导出报错
    3.清理环境成功
History     :
    modified：2021/10/12 by 5318639 优化用例适配新代码
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
            '----Opengauss_Function_Tools_gs_dump_Case0020start-----')
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.dump_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump.sql')
        self.result_msg = 'Compress mode is not supported for plain text'
        self.db_name = "db_dump20"
        self.tb_name = "t_dump20"

    def test_server_tools(self):
        text = '-------step1:创建测试数据;expect:创建成功--------'
        self.log.info(text)
        text = '-------step1.1:连接数据库并创建数据库;expect:创建成功--------'
        self.log.info(text)
        sql_cmd1 = f'drop database if exists {self.db_name};' \
            f'create database {self.db_name};'
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd1}";'
        self.log.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1,
                      '执行成功' + text)
        text = '-------step1.2:在创建好的数据库中创建表并插入数据;expect:创建成功--------'
        self.log.info(text)
        sql_cmd2 = f'''drop table if exists {self.tb_name};
            create table {self.tb_name} (id int ,name char(10));
            insert into {self.tb_name} values (1,'aa'),(2,'bb');
            '''
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd2}";'
        self.log.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        self.log.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2, '执行成功' + text)
        text = '-------step2:导出一个纯文本格式文件时设置压缩比级别;expect:合理报错--------'
        self.log.info(text)
        dump_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_dump {self.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'--format=p ' \
            f'-f {self.dump_path}' \
            f' -Z 9;'
        self.log.info(dump_cmd)
        dump_result = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(f'{self.result_msg}', dump_result, '执行成功' + text)

    def tearDown(self):
        text = '-------step3:清理环境;expect:清理完成--------'
        self.log.info(text)
        clean_cmd = f'drop database if exists {self.db_name}; '
        excute_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{clean_cmd}";' \
            f'rm -rf {self.dump_path};'
        self.log.info(excute_cmd)
        clean_result = self.dbuser_node.sh(excute_cmd).result()
        self.log.info(clean_result)
        self.log.info(
            '-----Opengauss_Function_Tools_gs_dump_Case0020finish------')
