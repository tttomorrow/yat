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
Case Name   : 导入已列举的表定义、数据到脚本文件
Description :
    1.创建数据
    2.导出数据
    3.导入数据
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
        self.root_user = Node('default')
        self.commonsh = CommonSH('dbuser')

    def test_server_tools1(self):
        self.log.info("--Opengauss_Function_Tools_gs_restore_Case0054开始执行--")
        self.log.info("----------------------创建数据-----------------------")
        sql_cmd = self.commonsh.execut_db_sql(f'''create table test1 \
            (id int,name char(20));
            insert into test1 values(1,'xixi'),(2,'haha'),(3,'hehe');
            create table test2 (id  int,name char(20));
            insert into test2 values(12,'xixi'),(22,'haha'),(33,'hehe');
            create table test3(id  int,name char(20));
            insert into test3 values(123,'xiyxi'),(212,'hayha'),\
            (313,'heyhe');
            create table test4(id  int,name char(20));
            insert into test4 values(33,'xiao'),(296,'bai'),(783,'cai');
            create table test5(id  int,name char(20));
            insert into test5 values(7,'yang'),(29886,'bai'),(9,'lao');
            create schema schema1;
            create schema schema2;
            create schema schema3;
            alter  table  test1 set schema schema1;
            alter  table  test2 set schema schema2;
            alter  table  test3 set schema schema1;
            select * from schema2.test2;
            ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)

        self.log.info("----------------导出tar格式文件-----------------")
        mkdir_cmd = f"mkdir /home/test_restore/ ;" \
            f"chmod -R 777 /home/test_restore/"
        self.log.info(mkdir_cmd)
        mkdir_msg = self.root_user.sh(mkdir_cmd).result()
        self.log.info(mkdir_msg)
        dump_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_dump -p {self.dbuser_node.db_port} " \
            f"{self.dbuser_node.db_name} " \
            f"-f /home/test_restore/test2.tar -F t "
        self.log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg)

        self.log.info("--------------导入之前导出的数据----------------")
        restore_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_restore  -p {self.dbuser_node.db_port} " \
            f"-l /home/test_restore/test2.tar -n public -t test4  " \
            f"-n schema2 -t test2 -f /home/test_restore/test57 -c"
        self.log.info(restore_cmd)
        restore_msg = self.dbuser_node.sh(restore_cmd).result()
        self.log.info(restore_msg)
        self.assertIn(self.constant.RESTORE_SUCCESS_MSG, restore_msg)

        self.log.info("--------导入后查看脚本文件数据--------")
        cat_cmd = f'''source {macro.DB_ENV_PATH};
            cat /home/test_restore/test57
            '''
        self.log.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.assertIn('TABLE DATA public test4', cat_msg)
        self.assertIn('TABLE DATA schema2 test2', cat_msg)

    def tearDown(self):
        self.log.info("----------------------清理环境-----------------------")
        clean_cmd = self.commonsh.execut_db_sql(f'''drop table schema1.test1  \
            cascade;
            drop table schema2.test2  cascade;
            drop table test4  cascade;
            drop table test5  cascade;
            drop schema schema1 cascade;
            drop schema schema2 cascade;
            drop schema schema3 cascade;
            ''')
        self.log.info(clean_cmd)
        rm_cmd = f"rm -rf /home/test_restore"
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info("--Opengauss_Function_Tools_gs_restore_Case0054执行结束--")
