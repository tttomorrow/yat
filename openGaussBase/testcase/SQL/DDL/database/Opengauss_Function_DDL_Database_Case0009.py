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
Case Type   : 基础功能
Case Name   : 修改数据库CONNECTION LIMIT
Description :
    1.创建数据库
    2.创建普通用户
    3.修改数据库连接数
    4.使用普通用户连接3个数据库，重复执行以下语句3次
Expect      :
    1.创建数据库成功
    2.创建用户成功
    3.修改数据库连接成功
    4.前两次执行成功，第三题无法连接提示too many
History     :
"""

import unittest
import time
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.ComThread import ComThread


class DdlDatabase(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_DDL_Database_Case0009.py 开始执行--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.db_primary_root_node = Node(node='PrimaryRoot')
        self.constant = Constant()
        self.dbname = 'database_case011'
        self.tblname = 'tbl_case011'
        self.username = 'user_case011'
        self.password = 'test@2345234'

    def test_ddldatabase(self):
        self.log.info('---------1.创建数据库---------------')
        sql = f"drop database if exists {self.dbname};" \
            f"create database {self.dbname} with  CONNECTION LIMIT=10;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('-----2.创建普通用户----------')
        sql = f"create user {self.username} with password '{self.password}';"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('-----------3.修改数据库连接数----------')
        sql = f"ALTER DATABASE {self.dbname} with CONNECTION LIMIT 2;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('---------4.使用普通用户连接3个数据库，重复执行以下语句3次-------')
        connect_thread = []
        for i in range(3):
            sql = 'select pg_sleep(15);'
            cmd = f'-U {self.username} -W {self.password}'
            connect_thread.append(ComThread(self.commonshpri.execut_db_sql,
                                            args=(sql, cmd, self.dbname)))
            connect_thread[i].setDaemon(True)
            connect_thread[i].start()
            time.sleep(2)
        for i in range(3):
            connect_thread[i].join(30)
            result = connect_thread[i].get_result()
            self.log.info(result)
            if i < 2:
                self.assertNotIn('too many', result)
            else:
                self.assertIn('too many', result)
        time.sleep(20)

    def tearDown(self):
        self.log.info('----------------环境清理----------')
        self.log.info('-----------删除数据库------------')
        sql = f"drop database if exists {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('----------------------删除用户----------------')
        sql = f"drop user if exists {self.username};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)

        self.log.info('--Opengauss_Function_DDL_Database_Case0009.py 执行结束--')
