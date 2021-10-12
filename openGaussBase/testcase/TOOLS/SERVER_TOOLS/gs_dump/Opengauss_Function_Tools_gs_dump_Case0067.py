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
Case Name   : 备份结果不包含依赖于指定对象的对象信息（--exclude-self）
Description :
    1.创建数据库testdump
    2.创建数据
    3.备份结果不包含依赖于指定对象的对象信息（--exclude-self）
    4.连接数据库，清理环境
Expect      :
    1.创建数据库testdump成功
    2.创建数据成功
    3.导出成功
    4.清理环境成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-----Opengauss_Function_Tools_gs_dump_Case0067start-----')
        self.dbusernode = Node('dbuser')
        self.constant = Constant()
        self.path = os.path.join(macro.DB_INSTANCE_PATH, 'dump_config')

    def test_server_tools(self):
        LOG.info('------------------1.连接数据库并创建数据库-----------------')
        sql_cmd1 = '''drop database if exists testdump;
            create database testdump;
            '''
        excute_cmd1 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbusernode.db_name}\
            -p {self.dbusernode.db_port} -c "{sql_cmd1}";
            '''
        LOG.info(excute_cmd1)
        msg1 = self.dbusernode.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, msg1)
        LOG.info('-------2.在创建好的数据库中创建模式，创建表\
        并插入数据并设置表的所属模式-------')
        sql_cmd2 = ''' drop schema if exists schema1;
            drop schema if exists schema2;
            create schema  schema1;
            create schema  schema2;
            drop table if  exists t1;
            drop table if  exists t2;
            create table t1 (id int);
            insert into t1 values(1),(2),(3);
            create table t2 (id int);
            insert into t2 values(8),(2),(5);
            alter table t1 set schema schema1;
            alter table t2 set schema schema2;
            drop view if exists view_t1;
            create view view_t1 as select * from schema1.t1 ;
            '''
        excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d testdump -p {self.dbusernode.db_port} -c "{sql_cmd2}";
            '''
        LOG.info(excute_cmd2)
        msg2 = self.dbusernode.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg2)


        LOG.info('-------------3.备份结果不包含指定对象自身的信息------------')
        excute_cmd3 = f'source {macro.DB_ENV_PATH} ;' \
            f'gs_dump ' \
            f'-p {self.dbusernode.db_port} testdump  ' \
            f'-F p  ' \
            f'--exclude-self ' \
            f'--include-depend-objs ' \
            f'-t  schema1.t1; '
        LOG.info(excute_cmd3)
        msg3 = self.dbusernode.sh(excute_cmd3).result()
        LOG.info(msg3)
        self.assertIn('DROP VIEW IF EXISTS', msg3)
        self.assertIn('CREATE VIEW view_t1', msg3)

    def tearDown(self):
        LOG.info('-----------------4.清理环境：删除数据库-----------------')
        sql_cmd4 = ''' drop database if exists testdump; '''
        excute_cmd4 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbusernode.db_name}\
            -p {self.dbusernode.db_port} -c "{sql_cmd4}";
            '''
        LOG.info(excute_cmd4)
        msg4 = self.dbusernode.sh(excute_cmd4).result()
        LOG.info(msg4)
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0067finish----')
