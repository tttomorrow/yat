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
Case Type   : 拷贝数据
Case Name   : 反语法测试\copy file from table
Description :
    1.创建测试表并插入数据
    2.构造数据文件
    3.使用反语法copy file from table进行copy
    4.清理环境
Expect      :
    1.创建测试表并插入数据成功
    2.构造数据文件成功
    3.使用反语法copy file from table进行copy失败
    4.清理环境成功
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Log = Logger()


class CopyFile(unittest.TestCase):
    def setUp(self):
        Log.info('----Opengauss_Function_DML_Copy_Case0046开始执行----')
        self.user_node = Node('PrimaryDbUser')
        self.constant = Constant()

    def test_copy_file(self):
        Log.info('----创建测试表并对测试表插入数据----')
        sql_cmd = '''drop table if exists testzl;
            create table testzl(sk integer,id char(16),\
            name varchar(20),sq_ft integer);
            insert into testzl values (001,'sk1','tt',3332);
            insert into testzl values (001,'sk1','tt',3332);
            insert into testzl values (001,'sk1','tt',3332); 
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.user_node.db_name} -p \
            {self.user_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)

        Log.info('----创建数据文件----')
        mkdir_cmd = f'''mkdir {macro.DB_INSTANCE_PATH}/pg_copydir;
            touch {macro.DB_INSTANCE_PATH}/pg_copydir/testzl.dat;
            '''
        Log.info(mkdir_cmd)
        mkdir_msg = self.user_node.sh(mkdir_cmd).result()
        Log.info(mkdir_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], mkdir_msg)

        Log.info('----使用反语法\copy file from table进行copy----')
        copy_cmd = f'''\copy '{macro.DB_INSTANCE_PATH}/pg_copydir/testzl.dat'\
            from testzl;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.user_node.db_name} -p \
            {self.user_node.db_port} -c "{copy_cmd}"
            '''
        Log.info(excute_cmd)
        copy_msg = self.user_node.sh(excute_cmd).result()
        Log.info(copy_msg)
        self.assertIn('testzl: No such file or directory', copy_msg)

    def tearDown(self):
        Log.info('----------------清理环境-----------------------')
        sql_cmd = '''drop table if exists testzl;'''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.user_node.db_name} -p \
            {self.user_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, msg)
        rm_cmd = f'rm -rf {macro.DB_INSTANCE_PATH}/pg_copydir;'
        Log.info(rm_cmd)
        rm_msg = self.user_node.sh(rm_cmd).result()
        Log.info(rm_msg)
        Log.info('----Opengauss_Function_DML_Copy_Case0046执行完成----')
