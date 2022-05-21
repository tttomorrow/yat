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
Case Name   : gs_dump导出文本格式的数据，使用gsql方式导入
Description :
    1.创建数据
    2.导出数据
    3.查看导出的数据是否正确
    4.清理环境
    5.导入之前导出的数据
    6.清理环境
Expect      :
    1.创建数据
    2.导出数据
    3.查看导出的数据是否正确
    4.清理环境
    5.导入之前导出的数据
    6.清理环境
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
        Log.info("---Opengauss_Function_Tools_gs_restore_Case0007开始执行---")
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.root_user = Node('default')

    def test_server_tools1(self):
        Log.info("--------------------步骤1.创建数据--------------------")
        Log.info("--------------------创建表并插入数据--------------------")
        sql_cmd = f'''drop table if exists test;
            create table test (id  int,name char(20));
            insert into test values(1,'xixi'),(2,'haha'),(3,'hehe');
             '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name}  \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)

        Log.info("----------------------创建角色-----------------------")
        sql_cmd = f'''drop role if exists manager;
            create role manager identified by '{macro.COMMON_PASSWD}';
            '''
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
            alter tablespace ds_location3 owner to manager;
            '''
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
            create schema schema1;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg)

        Log.info("----------------------创建创建函数-----------------------")
        sql_cmd = f'''drop function if exists func_increment_sql;
            create function func_increment_sql(i integer)
            returns integer
            as \$$
            begin
                    return i+1;
            end;
            \$$ language plpgsql;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, msg)

        Log.info("------------------------步骤2.导出数据-------------------------")
        mkdir_cmd = f'''mkdir /home/test_restore/
             chmod -R 777 /home/test_restore/'''
        Log.info(mkdir_cmd)
        mkdir_msg = self.root_user.sh(mkdir_cmd).result()
        Log.info(mkdir_msg)

        dump_cmd = f'''source {macro.DB_ENV_PATH};
            gs_dump -p {self.dbuser_node.db_port}\
            {self.dbuser_node.db_name} -f /home/test_restore/test2 -F p;
            '''
        Log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        Log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg)

        Log.info("-----步骤3.查看导出的数据是否正确-----")
        cat_cmd = f'''source {macro.DB_ENV_PATH}
            cat /home/test_restore/test2
            '''
        Log.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        Log.info(cat_msg)
        self.assertIn("CREATE TABLE test", cat_msg)
        self.assertIn("CREATE FUNCTION func_increment_sql", cat_msg)

        Log.info("----------------------步骤4.清理环境-------------------------")
        sql_cmd = f'''drop table test  CASCADE;
            drop tablespace ds_location3;
            drop role manager;
            drop database test ;
            drop schema schema1 cascade;
            drop function func_increment_sql;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.DROP_FUNCTION_SUCCESS_MSG, msg)

        Log.info("------------步骤5.导入之前导出的数据------------")
        restore_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -p {self.dbuser_node.db_port} \
            -d {self.dbuser_node.db_name}  \
            -f /home/test_restore/test2
            '''
        Log.info(restore_cmd)
        restore_msg = self.dbuser_node.sh(restore_cmd).result()
        Log.info(restore_msg)
        self.assertIn("total time", restore_msg)

    def tearDown(self):
        Log.info("------------------------步骤6.清理环境-------------------------")
        sql_cmd = f'''drop table if exists test;
            drop tablespace if exists ds_location3;
            drop role if exists manager;
            drop database if exists test ;
            drop schema if exists schema1 cascade;
            drop function if exists func_increment_sql;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        check_cmd = f"rm -rf /home/test_restore"
        Log.info(check_cmd)
        msg = self.root_user.sh(check_cmd).result()
        Log.info(msg)
        Log.info("--Opengauss_Function_Tools_gs_restore_Case0007执行结束--")
