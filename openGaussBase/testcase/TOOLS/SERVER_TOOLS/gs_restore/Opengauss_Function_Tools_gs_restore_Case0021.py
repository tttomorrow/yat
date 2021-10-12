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
Case Name   : 全量导出后，只导入数据，不导入定义到数据库(-a)
Description :
    1.创建表并插入数据
    2.导出数据
    3.导入之前导出的数据
    4.select查看表数据
    5.清理环境
Expect      :
    1.创建表并插入数据成功
    2.导出数据成功
    3.导入之前导出的数据成功
    4.select查看表数据成功
    5.清理环境成功
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
        Log.info("--Opengauss_Function_Tools_gs_restore_Case0021开始执行--")
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.root_user = Node('default')

    def test_server_tools1(self):
        Log.info("--------------------创建表并插入数据--------------------")
        sql_cmd = f'''
            create table test1 (id  int,name char(20));
            insert into test1 values(1,'xixi'),(2,'haha'),(3,'hehe');
            create table test2 (id  int,name char(20));
            insert into test2 values(12,'xixi'),(22,'haha'),(33,'hehe');
            create table test3(id  int,name char(20));
            insert into test3 values(123,'xiyxi'),(212,'hayha'),(313,'heyhe');
            create table test4(id  int,name char(20));
            insert into test4 values(33,'xiao'),(296,'bai'),(783,'cai');
            create table test5(id  int,name char(20));
            insert into test5 values(7,'yang'),(29886,'bai'),(9,'lao');
             '''
        excute_cmd = f'''
            source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)

        Log.info("------------------------导出数据-------------------------")
        check_cmd = f'''mkdir /home/test_restore/
                         chmod -R 777 /home/test_restore/'''
        Log.info(check_cmd)
        msg = self.root_user.sh(check_cmd).result()
        Log.info(msg)

        check_cmd = f'''source {macro.DB_ENV_PATH}
        gs_dump  -p {self.dbuser_node.db_port} {self.dbuser_node.db_name} \
        -f /home/test_restore/test2.sql -F c ;
        '''
        Log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg)

        Log.info("--------------导入之前导出的数据----------------")
        check_cmd = f'''source {macro.DB_ENV_PATH}
    gs_restore  -p {self.dbuser_node.db_port} -d {self.dbuser_node.db_name} \
    -W {self.dbuser_node.db_password}   /home/test_restore/test2.sql  -a
    '''
        Log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.RESTORE_SUCCESS_MSG, msg)

        Log.info("------------------------查看表数据-------------------------")
        sql_cmd = f'''
                    select * from  test1;
                    select * from  test2;
                    select * from  test3;
                    select * from  test4;
                    select * from  test5;
                    '''
        excute_cmd = f'''
           source {macro.DB_ENV_PATH} ;
           gsql -d {self.dbuser_node.db_name} -p {self.dbuser_node.db_port} \
           -c "{sql_cmd}"'''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn('(6 rows)', msg)

    def tearDown(self):
        Log.info("------------------------清理环境-------------------------")
        sql_cmd = f'''
                        drop table if exists test1 ;
                        drop table if exists test2 ;
                        drop table if exists test3 ;
                        drop table if exists test4 ;
                        drop table if exists test5 ;
                    '''
        excute_cmd = f'''
           source {macro.DB_ENV_PATH} ;
           gsql -d {self.dbuser_node.db_name} -p {self.dbuser_node.db_port} \
           -c "{sql_cmd}"'''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)

        check_cmd = f'''rm -rf /home/test_restore'''
        Log.info(check_cmd)
        msg = self.root_user.sh(check_cmd).result()
        Log.info(msg)
        Log.info('---Opengauss_Function_Tools_gs_restore_Case0021执行结束---')
