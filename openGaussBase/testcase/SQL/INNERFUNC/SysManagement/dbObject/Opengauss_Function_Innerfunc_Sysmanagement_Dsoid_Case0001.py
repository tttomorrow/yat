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
Case Type   : 功能测试
Case Name   : 使用pg_database_size(oid)函数查询指定OID代表的数据库使用的磁盘
              空间。
Description :
    1.查询当前数据库self.node.db_name
    2.新建数据库
    3.在中查询新建的数据库
    4.连接新建的数据库查询自己
Expect      : 
    1.查询成功
    2.新建成功
    3.查询成功
    4.比在self.node.db_name中查询的值小
"""

import unittest
import os

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.db_name = "db_dsoid_case0001"
        self.constant = Constant()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')

    def test_dbsize(self):
        def query(dbname):
            cmd = f"""select pg_database_size(a.oid) from pg_database a 
                    where a.datname = {dbname};"""
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            size = int(msg.splitlines()[2].strip())
            return size

        text = '---step1:查询当前数据库使用的磁盘空间;expect:成功---'
        self.log.info(text)
        size0 = query('current_catalog')
        self.assertTrue(0 < size0 < 9223372036854775807)

        text = '----step2:新建数据库并通过其它数据库查询其大小;expect:成功-----'
        self.log.info(text)
        db_create = f"""drop database if exists {self.db_name};
                        create database {self.db_name} encoding = 'utf-8';"""
        msg1 = self.commonsh.execut_db_sql(db_create)
        self.log.info(msg1)
        self.assertTrue(self.constant.CREATE_DATABASE_SUCCESS in msg1,
                        '执行失败:' + text)
        size1 = query('current_catalog')
        self.assertTrue(0 < size1 < 9223372036854775807)

        text = '---step3:连接上新建的数据库查询自己;expect:成功-----'
        self.log.info(text)
        cmd2 = f'''select pg_database_size(a.oid) from pg_database a where \
        a.datname = current_catalog;'''
        msg2 = self.commonsh.execut_db_sql(sql=cmd2, dbname=self.db_name)
        self.log.info(msg2)
        size2 = int(msg2.splitlines()[2].strip())
        self.assertTrue(size2 < size1)

    def tearDown(self):
        text = '---step4:删除数据库;expect:成功----'
        self.log.info(text)
        db_drop = f"""drop database if exists {self.db_name};"""
        result = self.commonsh.execut_db_sql(db_drop)
        self.log.info(db_drop)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, result,
                      '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
