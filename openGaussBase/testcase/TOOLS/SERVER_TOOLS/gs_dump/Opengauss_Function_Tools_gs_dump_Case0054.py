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
Case Name   : 表个数大于100，使用表文件导出数据
Description :
    1.创建数据库test
    2.创建模式，创建表并插入数据，设置表的所属模式
    3.创建表文件
    4.表个数大于100，使用表文件导出数据
    5.连接数据库，清理环境
Expect      :
    1.创建数据库test成功
    2.创建模式成功,创建表并插入数据成功
    3.创建表文件
    4.导出成功
    5.清理环境成功
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
        LOG.info('-----Opengauss_Function_Tools_gs_dump_Case0054start-----')
        self.dbusernode = Node('dbuser')
        self.constant = Constant()
        touch_cmd = f'touch {macro.DB_INSTANCE_PATH}/dump_config;' \
            f'ls {macro.DB_INSTANCE_PATH};'
        LOG.info(touch_cmd)
        touch_msg1 = self.dbusernode.sh(touch_cmd).result()
        LOG.info(touch_msg1)

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
        sql_msg1 = self.dbusernode.sh(excute_cmd1).result()
        LOG.info(sql_msg1)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_msg1)
        LOG.info('-------2.在创建好的数据库中创建模式，创建表\
        并插入数据并设置表的所属模式-------')

        for i in range(1, 106):
            sql_cmd2 = f'drop schema if exists schema{i};' \
            f'create schema schema{i};'\
            f'create table schema{i}.table{i}(id int,name varchar(20));'
            excute_cmd2 = f'''source {macro.DB_ENV_PATH} ;
                gsql -d testdump -p {self.dbusernode.db_port} -c "{sql_cmd2}";
                '''
            LOG.info(excute_cmd2)
            sql_msg2 = self.dbusernode.sh(excute_cmd2).result()
            LOG.info(sql_msg2)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_msg2)
            LOG.info('-----------3.创建表文件-----------')
            cmd1 = f'echo "schema{i}.table{i}" >> ' \
                f'{macro.DB_INSTANCE_PATH}/dump_config; '
            LOG.info(cmd1)
            msg1 = self.dbusernode.sh(cmd1).result()
            LOG.info(msg1)
        cat_cmd = f'cat {macro.DB_INSTANCE_PATH}/dump_config;'
        LOG.info(cat_cmd)
        cat_msg = self.dbusernode.sh(cat_cmd).result()
        LOG.info(cat_msg)
        self.assertTrue(len(cat_msg.splitlines()) == 105)

        LOG.info('-------------4.表个数大于100，使用表文件导出数据------------')
        dump_cmd = f'source {macro.DB_ENV_PATH} ;' \
            f'gs_dump ' \
            f'-p {self.dbusernode.db_port} testdump  ' \
            f'-F p  ' \
            f'--include-table-file={macro.DB_INSTANCE_PATH}/dump_config ;'
        LOG.info(dump_cmd)
        dump_msg = self.dbusernode.sh(dump_cmd).result()
        LOG.info(dump_msg)
        self.assertTrue(dump_msg.count('CREATE TABLE') == 105)
        self.assertTrue(dump_msg.count('COPY') == 105)
        self.assertIn('dump database testdump successfully', dump_msg)

    def tearDown(self):
        LOG.info('-----------------5.清理环境：删除数据库-----------------')
        sql_cmd3 = ''' drop database if exists testdump; '''
        excute_cmd3 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbusernode.db_name}\
            -p {self.dbusernode.db_port} -c "{sql_cmd3}";
            rm -rf {macro.DB_INSTANCE_PATH}/dump_config
            '''
        LOG.info(excute_cmd3)
        sql_msg3 = self.dbusernode.sh(excute_cmd3).result()
        LOG.info(sql_msg3)
        LOG.info('----Opengauss_Function_Tools_gs_dump_Case0054finish----')
