"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 导入时参数-n和-s的使用
Description :
    1.创建数据
    2.导出数据
    3.导入时只导入列举的模式中的对象和模式
    4.清理环境
Expect      :
    1.创建数据成功
    2.导出数据成功
    3.导入数据成功
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
        self.db_name = 'db_test'

    def test_server_tools1(self):
        self.log.info("--Opengauss_Function_Tools_gs_restore_Case0112开始执行--")
        self.log.info("-----------------创建数据--------------")
        sql = f'create database {self.db_name};'
        sql_cmd = self.commonsh.execut_db_sql(sql,
                                              dbname=self.dbuser_node.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql(f'''create table test1 \
            (id int,name char(20));
            insert into test1 values(1,'xixi'),(2,'haha'),(3,'hehe');
            create table test2 (id  int,name char(20));
            insert into test2 values(12,'xixi'),(22,'haha'),(33,'hehe');
            create table test3(id  int,name char(20));
            insert into test3 values(123,'xiyxi'),(212,'hayha'),(313,'heyhe');
            create table test4(id  int,name char(20));
            insert into test4 values(33,'xiao'),(296,'bai'),(783,'cai');
            create table test5(id  int,name char(20));
            insert into test5 values(7,'yang'),(29886,'bai'),(9,'lao');
            create schema schema1;
            create schema schema2;
            create schema schema3;
            alter  table  test1 set schema schema1;
            alter  table  test2 set schema schema2;
            alter  table  test3 set schema schema3;
            ''', dbname=self.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd)

        self.log.info("----------------导出tar格式文件并清理环境-----------------")
        dump_cmd = f"source {macro.DB_ENV_PATH}; " \
            f" gs_dump -p {self.dbuser_node.db_port}  " \
            f"{self.db_name}  " \
            f"-f {macro.DB_INSTANCE_PATH}/test.tar -F t; " \
            f"gsql -p {self.dbuser_node.db_port} -d   " \
            f"{self.db_name} -c " \
            f"'drop table schema1.test1 ;" \
            f"drop table schema2.test2 ;" \
            f"drop table schema3.test3 ;" \
            f"drop table test4  cascade;" \
            f"drop table test5  cascade;" \
            f"drop schema schema1 cascade;" \
            f"drop schema schema2 cascade;" \
            f"drop schema schema3 cascade;'"
        self.log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, dump_msg)

        self.log.info("--------------导入之前导出的数据并查看----------------")
        restore_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_restore -p {self.dbuser_node.db_port} " \
            f"-d  {self.db_name} " \
            f"{macro.DB_INSTANCE_PATH}/test.tar -n schema1 " \
            f"-n schema2 -n schema4 -s; " \
            f"gsql -p {self.dbuser_node.db_port} -d  " \
            f"{self.db_name} -c " \
            f"'select * from schema1.test1;" \
            f"select * from schema2.test2; " \
            f"select * from schema3.test3;" \
            f"select * from test4;" \
            f"select * from test5;'"
        self.log.info(restore_cmd)
        restore_msg = self.dbuser_node.sh(restore_cmd).result()
        self.log.info(restore_msg)
        self.assertIn(self.constant.RESTORE_SUCCESS_MSG, restore_msg)
        self.assertIn('0 rows', restore_msg)
        self.assertIn('ERROR:  relation "test4" does not exist', restore_msg)
        
    def tearDown(self):
        self.log.info("------------------清理环境------------------")
        sql_cmd = self.commonsh.execut_db_sql(f'drop database'
                                              f' {self.db_name};')
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf {macro.DB_INSTANCE_PATH}/test.tar"
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info("-Opengauss_Function_Tools_gs_restore_Case0112执行结束-")
