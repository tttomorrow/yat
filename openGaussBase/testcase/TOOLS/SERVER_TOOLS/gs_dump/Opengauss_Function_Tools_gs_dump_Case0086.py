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
Case Name   : 指定创建转储使用的角色名，不指定密码
Description :
    1.创建测试数据
    2.指定创建转储使用的角色名，不指定密码
    3.清理环境
Expect      :
    1.创建测试数据成功
    2.导出成功
    3.清理环境成功
History     :
    modified: by 5318639 2021/07/15 添加清理用户的语句
    modified: by 5318639 2021/10/13 优化用例，适配新版本
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----opengauss_function_tools_gs_dump_case0086start------')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.db_name = "db_dump0086"
        self.tb_name1 = "t_dump0086_1"
        self.tb_name2 = "t_dump0086_2"
        self.r_name = "r_dump0086"

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
            f'-c "{sql_cmd1}"'
        self.log.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1,
                      '执行成功' + text)
        text = '-------step1.2:在创建好的数据库中创建表并插入数据;expect:创建成功--------'
        self.log.info(text)
        sql_cmd2 = f''' 
            drop role if exists {self.r_name};
            create role {self.r_name} identified by \'{macro.COMMON_PASSWD}\';
            grant all privileges to {self.r_name};
            drop table  if exists {self.tb_name1};
            drop table  if exists {self.tb_name2};
            create table {self.tb_name1} (i int,d int );
            insert into {self.tb_name1} values(1,2),(2,3),(3,4);
            create table {self.tb_name2} (id int,dd int);
            insert into {self.tb_name2} values(11,22),(21,34),(31,45);
            '''
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd2}"'
        self.log.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        self.log.info(msg2)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, msg2,
                      '执行成功' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2, '执行成功' + text)
        text = '------step3:指定创建转储使用的角色名，不指定角色密码;expect:交互输入密码后导出成功------'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};
                    expect <<EOF
                    set timeout -1
                    spawn gs_dump -p {self.dbuser_node.db_port} \
                    {self.db_name} \
                    -F p\
                    -U {self.dbuser_node.ssh_user} \
                    -W {self.dbuser_node.ssh_password} \
                    --role={self.r_name}
                    expect "Password:"
                    send "{macro.COMMON_PASSWD}\r"
                    expect eof\n''' + "EOF"
        self.log.info(dump_cmd)
        dump_result = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(f'dump database {self.db_name} successfully',
                      dump_result, '执行失败:' + text)

    def tearDown(self):
        text = '-----------------step3:清理环境;expect:清理完成----------------'
        self.log.info(text)
        sql_cmd4 = f'drop database if exists {self.db_name};' \
            f'drop role {self.r_name};'
        excute_cmd4 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd4}";'
        self.log.info(excute_cmd4)
        msg4 = self.dbuser_node.sh(excute_cmd4).result()
        self.log.info(msg4)
        self.log.info(
            '----opengauss_function_tools_gs_dump_case0086finish----')
