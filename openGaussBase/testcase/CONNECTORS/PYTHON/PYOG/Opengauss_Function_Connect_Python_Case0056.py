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
Case Name   : openGauss模式连接数据库，数值类型校验
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.数值类型校验
    3.1整数类型
    3.2任意精度型
    3.3序列整型
    3.4浮点类型
    3.5删除表
    4.断开连接
    5.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功
    3.1执行结果与gsql执行结果一致
    3.2执行结果与gsql执行结果一致
    3.3执行结果与gsql执行结果一致
    3.4执行结果与gsql执行结果一致
    3.5执行成功
    4.执行成功，db.state返回'closed'
    5.执行成功
History     :
"""
import os
import unittest
from decimal import Decimal

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython56(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_56'
        text = '----Opengauss_Function_Connect_Python_Case0056 start----'
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

        text = '----step3: 数值类型校验 expect: 成功----'
        self.LOG.info(text)
        text = '----step3.1: 整数类型 expect: 成功----'
        self.LOG.info(text)
        values = ('255', 32767, 2147483647, 2147483647, 9223372036854775807)
        cmd = f'''create table {self.t_name}_1(
                col1 tinyint, 
                col2 smallint,
                col3 integer,
                col4 binary_integer,
                col5 bigint
            );
            insert into {self.t_name}_1 values {values};
            select * from {self.t_name}_1;'''
        result = list()
        for c in cmd.split(';'):
            if c:
                self.LOG.info(c + ';')
                sql_res = self.db.prepare(c + ';').first()
                self.LOG.info(sql_res)
                result.append(sql_res)
        expect = [self.constant.CREATE_TABLE_SUCCESS, 1, values]
        self.LOG.info(result)
        self.assertEqual(result, expect, '执行失败：' + text)

        text = '----step3.2: 任意精度型 expect: 成功----'
        self.LOG.info(text)
        values = (Decimal('1.13'), Decimal('1.131'), Decimal('1.1315'))
        cmd = f'''create table {self.t_name}_2(
                col1 numeric(12,2), 
                col2 decimal(12,3),
                col3 number(12,4)
            );
            insert into {self.t_name}_2 values (1.131456, 1.131456, 1.131456);
            select * from {self.t_name}_2;'''
        result = list()
        for c in cmd.split(';'):
            if c:
                self.LOG.info(c + ';')
                sql_res = self.db.prepare(c + ';').first()
                self.LOG.info(sql_res)
                result.append(sql_res)
        expect = [self.constant.CREATE_TABLE_SUCCESS, 1, values]
        self.LOG.info(result)
        self.assertEqual(result, expect, '执行失败：' + text)

        text = '----step3.3: 序列整型 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_3(
                col1 smallserial, 
                col2 serial,
                col3 bigserial
            );
            insert into {self.t_name}_3 values (default);
            select * from {self.t_name}_3;'''
        result = list()
        for c in cmd.split(';'):
            if c:
                self.LOG.info(c + ';')
                sql_res = self.db.prepare(c + ';').first()
                self.LOG.info(sql_res)
                result.append(sql_res)
        expect = [self.constant.CREATE_TABLE_SUCCESS, 1, (1, 1, 1)]
        self.LOG.info(result)
        self.assertEqual(result, expect, '执行失败：' + text)

        text = '----step3.4: 浮点类型 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_4(
                col1 real, 
                col2 float4,
                col3 double precision,
                col4 float8,
                col5 float(3),
                col6 binary_double,
                col7 dec(10,4),
                col8 integer(10,3)
            );
            insert into {self.t_name}_4 values (1.131456, 1.131456, \
            1.131456, 1.131456, 1.131456, 1.131456, 1.131456, 1.131456);
            select * from {self.t_name}_4;'''
        result = list()
        for c in cmd.split(';'):
            if c:
                self.LOG.info(c + ';')
                sql_res = self.db.prepare(c + ';').first()
                self.LOG.info(sql_res)
                result.append(sql_res)
        values = (1.1314560174942017, 1.1314560174942017, 1.131456, 1.131456,
                  1.1314560174942017, 1.131456, Decimal('1.1315'),
                  Decimal('1.131'))
        expect = [self.constant.CREATE_TABLE_SUCCESS, 1, values]
        self.LOG.info(result)
        self.assertEqual(result, expect, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step3.5: 删除表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table if exists {self.t_name}_1 cascade;
            drop table if exists {self.t_name}_2 cascade;
            drop table if exists {self.t_name}_3 cascade;
            drop table if exists {self.t_name}_4 cascade;'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step4: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0056 end----'
        self.LOG.info(text)
