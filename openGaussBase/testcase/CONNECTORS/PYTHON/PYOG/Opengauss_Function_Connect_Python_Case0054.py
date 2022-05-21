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
Case Type   : python驱动pyog
Case Name   : openGauss模式连接数据库，定义操作符
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.定义操作符
    3.1定义数据类型person
    3.2建表插入，使用person类型
    3.3定义比较函数
    3.4定义操作符
    3.5使用操作符
    3.6删除比较函数、操作符、表、数据类型
    4.断开连接
    5.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功
    3.1回显CREATE TYPE
    3.2回显CREATE TABLE.*INSERT 0 1.*INSERT 0 1
    3.3回显CREATE FUNCTION
    3.4回显CREATE OPERATOR
    3.5回显t
    3.6删除表成功，删除操作符失败
    4.执行成功，db.state返回'closed'
    5.执行成功
History     :
"""
import os
import unittest

import py_opengauss
from py_opengauss.exceptions import FeatureError
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython54(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.type_name = 'person'
        self.t_name = 't_py_54'
        self.compare_func_name = 'person_age_smaller'
        self.operator = '<'
        text = '----Opengauss_Function_Connect_Python_Case0054 start----'
        self.LOG.info(text)

    def test_conn(self):
        text = '----step1: 配置pg_hba入口 expect: 成功----'
        self.LOG.info(text)
        host_cmd = "ifconfig -a|grep inet6 -a2|" \
                   "grep broadcast|awk '{print $2}'"
        self.host = os.popen(host_cmd).readlines()[0].strip()
        self.assertIsNotNone(self.host)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.pri_user.db_user} ' \
            f'{self.host}/32 sha256"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)

        text = '----step2: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.pri_user.db_user}:' \
            f'{self.pri_user.db_password}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        self.LOG.info(conn_info)
        self.db = py_opengauss.open(conn_info)
        self.assertEqual('idle', self.db.state, '执行失败：' + text)

        text = '----step3: 定义操作符 expect: 成功----'
        self.LOG.info(text)
        text = '----step3.1: 定义数据类型person expect: 成功----'
        self.LOG.info(text)
        cmd = f"create type {self.type_name} as (name varchar(10), age int);"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_TYPE_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step3.2: 建表插入，使用person类型 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table if exists {self.t_name};
            create table {self.t_name} (id serial, o {self.type_name});
            insert into {self.t_name} (o) values (row('Amy', 18));
            insert into {self.t_name} (o) values (row('Nico', 19));'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)
        self.LOG.info(sql_res)
        self.assertIsNone(sql_res, '执行失败：' + text)

        text = '----step3.3: 定义比较函数 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create or replace function {self.compare_func_name}\
            (left_o {self.type_name}, right_o {self.type_name}) \
            returns boolean as $$
            select (left_o).age < (right_o).age
            $$ language sql strict;'''
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_FUNCTION_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step3.4: 定义操作符 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create operator {self.operator} (procedure = " \
            f"{self.compare_func_name}, leftarg = {self.type_name}, " \
            f"rightarg = {self.type_name}, commutator = {self.operator});"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'CREATE OPERATOR', '执行失败：' + text)

        text = '----step3.5: 使用操作符 expect: 成功----'
        self.LOG.info(text)
        cmd = f"select (select o from {self.t_name} where id = 1) " \
            f"{self.operator} (select o from {self.t_name} where id = 2);"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertTrue(sql_res, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step3.6: 删除类型转换，转换函数 expect: 成功----'
        self.LOG.info(text)
        drop_cmd = f'drop table if exists {self.t_name};'
        self.LOG.info(drop_cmd)
        sql_res = self.db.execute(drop_cmd)

        cmd = f'''drop operator if exists {self.operator} \
            ({self.type_name}, {self.type_name});
            drop function if exists {self.compare_func_name};
            drop type if exists {self.type_name};'''
        self.LOG.info(cmd)
        with self.assertRaises(FeatureError):
            self.db.execute(cmd)

        text = '----step4: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0054 end----'
        self.LOG.info(text)
