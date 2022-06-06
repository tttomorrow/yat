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
Case Name   : 导入数据时不指定数据库也不指定脚本文件
Description :
    1.创建数据
    2.导出数据
    3.导入数据
    4.清理环境
Expect      :
    1.成功创建数据
    2.导出数据成功
    3.导入失败
    4.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Log = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Log.info("--Opengauss_Function_Tools_gs_restore_Case0031开始执行--")
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.root_user = Node('default')
        self.info = 'Mandatory to specify either ' \
                    'dbname or list option for gs_restore'

    def test_server_tools1(self):
        Log.info("--------------------创建表并插入数据--------------------")
        sql_cmd = f'''drop table if exists test;
            create table test (id  int,name char(20));
            insert into test values(1,'xixi'),(2,'haha'),(3,'hehe');
             '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)

        Log.info("----------------------创建角色-----------------------")
        sql_cmd = f'''create role manager identified \
        by '{macro.COMMON_PASSWD}';'''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
                       gsql -d {self.dbuser_node.db_name} \
                       -p {self.dbuser_node.db_port} -c "{sql_cmd}"
                       '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, msg)

        Log.info("----------------------创建表空间-----------------------")
        sql_cmd = f'''create tablespace ds_location1 relative \
            location 'tablespace/tablespace_1';
            alter tablespace ds_location1 rename to ds_location3;
            alter tablespace ds_location3 owner to manager;'''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, msg)

        Log.info("----------------------创建数据库-----------------------")
        sql_cmd = f'''create database test;
            create schema schema1;'''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg)

        Log.info("--------------------创建创建函数---------------------")
        sql_cmd = f'''create function func_increment_sql(i integer)
            returns integer
            as \$$
            begin
                    return i+1;
            end;
            \$$ language plpgsql;
                  '''
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, msg)

        Log.info("------------------------导出数据-------------------------")
        mkdir_cmd = f"mkdir /home/test_restore/ ;" \
            f"chmod -R 777 /home/test_restore/"
        Log.info(mkdir_cmd)
        msg = self.root_user.sh(mkdir_cmd).result()
        Log.info(msg)

        dunp_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_dump -p {self.dbuser_node.db_port} " \
            f"{self.dbuser_node.db_name} " \
            f"-f /home/test_restore/test2.tar -F t"
        Log.info(dunp_cmd)
        msg = self.dbuser_node.sh(dunp_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg)

        Log.info("-----导入时不指定数据库也不指定脚本文件-----")
        restore_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_restore  -p {self.dbuser_node.db_port} " \
            f" /home/test_restore/test2.tar -c "
        Log.info(restore_cmd)
        msg = self.dbuser_node.sh(restore_cmd).result()
        Log.info(msg)
        self.assertIn(self.info, msg)

    def tearDown(self):
        Log.info("------------------------清理环境-------------------------")
        sql_cmd = f'''drop table if exists test;
            drop tablespace if exists ds_location3;
            drop role if exists manager;
            drop database if exists test ;
            drop schema if exists schema1 cascade;
            drop function if exists func_increment_sql;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        rm_cmd = f"rm -rf /home/test_restore"
        Log.info(rm_cmd)
        msg = self.root_user.sh(rm_cmd).result()
        Log.info(msg)
        Log.info("--Opengauss_Function_Tools_gs_restore_Case0031执行结束--")
