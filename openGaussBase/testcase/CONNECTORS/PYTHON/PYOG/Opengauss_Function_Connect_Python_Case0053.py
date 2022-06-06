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
Case Name   : openGauss模式连接数据库，定义数据类型转换
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建自定义类型
    4.创建转换函数
    5.定义类型转换
    6.使用
    7.删除类型，类型转换，转换函数
    8.断开连接
    9.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功，回显CREATE TYPE
    4.执行成功，回显CREATE FUNCTION
    5.执行成功，回显CREATE CAST
    6.执行成功，回显(3,amy)
    7.执行成功，回显DROP TABLE, DROP CAST, DROP FUNCTION, DROP TYPE
    8.执行成功，db.state返回'closed'
    9.执行成功
History     :
"""
import os
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython53(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.type_name = 'comtext'
        self.cast_func_name = 'boolean_to_numeric'
        self.t_name = 't_py_53'
        text = '----Opengauss_Function_Connect_Python_Case0053 start----'
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

        text = '----step3: 创建自定义类型 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create type {self.type_name} as (length int, content text);"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_TYPE_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step4: 创建转换函数 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create or replace function {self.cast_func_name} (text)\
            returns {self.type_name} as $$
                select char_length($1), $1;
            $$ language sql strict;'''
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_FUNCTION_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step5: 定义类型转换 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create cast (text as {self.type_name}) with function " \
            f"{self.cast_func_name}(text) as implicit;  "
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'CREATE CAST', '执行失败：' + text)

        text = '----step6: 使用 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name} (a {self.type_name});
            insert into {self.t_name} values ('amy'::text);
            select * from {self.t_name};'''
        result = []
        for c in cmd.splitlines():
            if c.strip():
                self.LOG.info(c)
                sql_res = self.db.prepare(c).first()
                self.LOG.info(sql_res)
                result.append(sql_res)
        expect = [self.constant.CREATE_TABLE_SUCCESS, 1, (3, 'amy')]
        self.assertEqual(result, expect, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step7: 删除表、类型转换、转换函数、自定义类型 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table if exists {self.t_name};
            drop cast if exists (text as {self.type_name});
            drop function if exists {self.cast_func_name};
            drop type if exists {self.type_name};'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step8: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0053 end----'
        self.LOG.info(text)
