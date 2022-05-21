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
Case Name   : 导入时参数-e和-s的使用
Description :
    1.创建数据
    2.导出数据
    3.导入时只导入指定模式定义，发送SQL语句到数据库时如果出现错误，退出
    4.清理环境
Expect      :
    1.创建数据成功
    2.导出数据成功
    3.导入失败（提示模式已存在，然后退出）
    4.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.db_name = 'db_test_0107'

    def test_server_tools1(self):
        self.log.info("--Opengauss_Function_Tools_gs_restore_Case0107开始执行--")
        text = "----step1: 创建数据; expect: 创建成功----"
        self.log.info(text)
        sql = f'create database {self.db_name};'
        sql_cmd = self.commonsh.execut_db_sql(sql,
                                              dbname=self.dbuser_node.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql(f'''
            drop table if exists t_test_0107;
            create table t_test_0107 (id int,name char(20));
            insert into t_test_0107 values(1,'xixi'),(2,'haha'),(3,'hehe');
            drop schema if exists s_schema_0107;
            create schema s_schema_0107;
            create or replace function f_increment_sql_0107(i integer)
            returns integer
            as \$$
            begin
                return i+1;
            end;
            \$$ language plpgsql;
            ''', dbname=self.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = "----step2: 导出tar格式文件; expect: 导出成功----"
        dump_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_dump -p {self.dbuser_node.db_port} " \
            f" {self.db_name} " \
            f"-f {macro.DB_INSTANCE_PATH}/test.tar -F t"
        self.log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg,
                      '执行失败:' + text)

        text = "----step3: 导入之前导出的数据并查看; expect: 导入失败----"
        restore_cmd = f"source {macro.DB_ENV_PATH} ;" \
            f"gs_restore -p {self.dbuser_node.db_port} " \
            f"-d  {self.db_name}  " \
            f"{macro.DB_INSTANCE_PATH}/test.tar -s -e"
        self.log.info(restore_cmd)
        msg = self.dbuser_node.sh(restore_cmd).result()
        self.log.info(msg)
        self.assertIn('already exists', msg,
                      '执行失败:' + text)

    def tearDown(self):
        text = "----step4: 清理环境; expect: 清理环境成功"
        sql_cmd = self.commonsh.execut_db_sql(f'drop database'
                                              f' {self.db_name};')
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf {macro.DB_INSTANCE_PATH}/test.tar"
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info("-Opengauss_Function_Tools_gs_restore_Case0107执行结束-")
