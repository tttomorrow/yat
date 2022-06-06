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
Case Name   : 导入时参数-i和-t的使用
Description :
    1.创建数据
    2.导出数据
    3.导入时只导入指定表数据和索引
    4.清理环境
Expect      :
    1.创建数据成功
    2.导出数据成功
    3.test1.和test4的数据被导入
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
        self.log.info("--Opengauss_Function_Tools_gs_restore_Case0109开始执行--")
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
            create index  index1 on test1(id);
            create index  index2 on test2(id);
            create index  index3 on test3(id);
            create index  index4 on test4(id);
            create index  index5 on test5(id);
            ''', dbname=self.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd)

        self.log.info("----------------导出tar格式文件-----------------")
        dump_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_dump -p {self.dbuser_node.db_port} " \
            f" {self.db_name}  " \
            f"-f {macro.DB_INSTANCE_PATH}/test.tar -F t"
        self.log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg)

        self.log.info("--------------导入之前导出的数据并查看,----------------")
        restore_cmd = f"source {macro.DB_ENV_PATH} ;" \
            f"gs_restore -p {self.dbuser_node.db_port} " \
            f"-d  {self.db_name} " \
            f"{macro.DB_INSTANCE_PATH}/test.tar  " \
            f"-t test1 -t test4 -I index1 -I index2 ; " \
            f"gsql -p {self.dbuser_node.db_port} " \
            f"-d {self.db_name} -c " \
            f"'select * from test1;" \
            f"select * from test4;'"
        self.log.info(restore_cmd)
        restore_msg = self.dbuser_node.sh(restore_cmd).result()
        self.log.info(restore_msg)
        self.assertIn('table test1 complete data imported', restore_msg)
        self.assertIn('table test4 complete data imported', restore_msg)
        self.assertIn('6 rows', restore_msg)

    def tearDown(self):
        self.log.info("------------------清理环境------------------")
        sql_cmd = self.commonsh.execut_db_sql(f'drop database'
                                              f' {self.db_name};')
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf {macro.DB_INSTANCE_PATH}/test.tar"
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info("-Opengauss_Function_Tools_gs_restore_Case0109执行结束-")
