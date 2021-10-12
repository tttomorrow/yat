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
Case Name   : 创建数据库修改LC_COLLATE，LC_CTYPE，CONNECTION LIMIT
Description :
    1.创建数据库
    2.切换到数据库test2中，创建表并插入数据
    3.使用管理员用户连接10个数据库，重复执行以下语句10次
    4.创建普通用户
    5.使用普通用户连接3个数据库，重复执行以下语句3次
    6.使用管理员用户连接1个，使用普通用户连接两个
    7.使用普通用户连接2个，使用管理员用户连接2个
    8.配置最大连接数为-1
    9.配置最大连接数为-2
Expect      :
    1.创建数据库成功
    2.创建表成功并插入数据成功
    3.连接成功，无报错
    4.创建用户成功
    5.执行第三次的时候报错，提示：gsql: FATAL:  too many connections for database "testdb"
    6.第三次连接报错
    7.连接成功，无报错
    8.创建数据库成功
    9.创建数据库失败
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
        self.log.info('--Opengauss_Function_DDL_Database_Case0011.py 开始执行---')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.db_primary_root_node = Node(node='PrimaryRoot')
        self.constant = Constant()
        self.dbname = 'database_case011'
        self.tblname = 'tbl_case011'
        self.username = 'user_case011'
        self.password = 'test@2345234'

    def test_basebackup(self):
        self.log.info('----------1.创建数据库-------------')
        sql = f"drop database if exists {self.dbname};" \
            f"create database {self.dbname} with LC_COLLATE='zh_CN.gbk'" \
            f" LC_CTYPE = 'zh_CN.gbk' CONNECTION LIMIT=2;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('----------2.切换到数据库test2中，创建表并插入数据----')
        sql = f"create table {self.tblname}(i char(20));"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)
        sql = f"insert into {self.tblname} values('你'),('啊'),('好');"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
        sql = f"select * from {self.tblname} order by i;"
        result = self.commonshpri.execut_db_sql(sql, dbname=self.dbname)
        self.log.info(result)
        result_list = result.strip().splitlines()
        self.assertIn('你', result_list[2])
        self.assertIn('好', result_list[3])
        self.assertIn('啊', result_list[4])
        time.sleep(2)

        self.log.info('-----3.使用管理员用户连接10个数据库，重复执行以下语句10次-----')
        connect_thread = []
        cmd = f'-U {self.db_primary_db_user.db_user} -W ' \
            f'{self.db_primary_db_user.db_password}'
        for i in range(10):
            connect_thread.append(
                ComThread(self.commonshpri.execut_db_sql,
                          args=('select pg_sleep(10);', cmd, self.dbname)))
            connect_thread[i].setDaemon(True)
            connect_thread[i].start()
            time.sleep(1)
        for i in range(10):
            connect_thread[i].join(60)
            result = connect_thread[i].get_result()
            self.log.info(result)
            self.assertNotIn('too many', result)

        self.log.info('----4.创建普通用户--------')
        result = self.commonshpri.execut_db_sql(
            f"create user {self.username} with password '{self.password}';")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info('-----------5.使用普通用户连接3个数据库，重复执行以下语句3次------')
        connect_thread = []
        for i in range(3):
            connect_thread.append(ComThread(self.commonshpri.execut_db_sql,
                                            args=('select pg_sleep(15);',
                    f'-U {self.username} -W {self.password}', self.dbname)))
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

        self.log.info('----6.使用管理员用户连接1个，使用普通用户连接两个-----')
        connect_thread = []
        for i in range(3):
            if i == 0:
                connect_thread.append(
                    ComThread(self.commonshpri.execut_db_sql, args=(
                        'select pg_sleep(15);', '', self.dbname)))
            else:
                connect_thread.append(ComThread(self.commonshpri.execut_db_sql,
                                                args=('select pg_sleep(15);',
                                    f'-U {self.username} -W {self.password}',
                                                      self.dbname)))
            connect_thread[i].setDaemon(True)
            connect_thread[i].start()
            time.sleep(1)
        for i in range(3):
            connect_thread[i].join(30)
            result = connect_thread[i].get_result()
            self.log.info(result)
            if i < 2:
                self.assertNotIn('too many', result)
            else:
                self.assertIn('too many', result)
        time.sleep(20)

        self.log.info('---------7.使用普通用户连接2个，使用管理员用户连接2个--------')
        connect_thread = []
        for i in range(4):
            if i < 2:
                connect_thread.append(ComThread(self.commonshpri.execut_db_sql,
                                                args=('select pg_sleep(15);',
                    f'-U {self.username} -W {self.password}', self.dbname)))
            else:
                connect_thread.append(
                    ComThread(self.commonshpri.execut_db_sql,
                              args=('select pg_sleep(15);', '', self.dbname)))
            connect_thread[i].setDaemon(True)
            connect_thread[i].start()
            time.sleep(1)
        for i in range(4):
            connect_thread[i].join(30)
            result = connect_thread[i].get_result()
            self.log.info(result)
            self.assertNotIn('too many', result)

        self.log.info('------------8.配置最大连接数为-1-----------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname} with CONNECTION LIMIT=-1;")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('---------------9.配置最大连接数为-2------------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname} with CONNECTION LIMIT=-2;")
        self.log.info(result)
        self.assertIn('ERROR:  invalid connection limit: -2', result)

    def tearDown(self):
        self.log.info('------------环境清理-------')
        self.log.info('----------------------删除数据库--------------------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};")
        self.log.info(result)
        self.log.info('----------------------删除用户-------------------')
        result = self.commonshpri.execut_db_sql(
            f"drop user if exists {self.username};")
        self.log.info(result)

        self.log.info('-Opengauss_Function_DDL_Database_Case0011.py 执行结束-')
