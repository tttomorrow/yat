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
Case Name   : openGauss模式连接数据库，定义包
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建包头
    4.创建包体
    5.调用包定义存储过程
    6.查询
    7.删除表、存储过程、包
    8.断开连接
    9.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功，回显CREATE PACKAGE
    4.执行成功，回显CREATE PACKAGE BODY
    5.执行成功
    6.执行成功
    7.执行成功
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


class ConnPython49(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_49'
        self.proc_name = 'p_py_49'
        self.pkg_name = 'pkg_py_49'
        text = '----Opengauss_Function_Connect_Python_Case0049 start----'
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

        text = '----step3: 创建包头 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create or replace package {self.pkg_name} is
            var1 int:=1;
            var2 int:=2;
            procedure {self.proc_name}(var3 int);
            end {self.pkg_name};'''
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'CREATE PACKAGE', '执行失败：' + text)

        text = '----step4: 创建包体 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create or replace package body {self.pkg_name} is
            var4 int:=3;
            procedure {self.proc_name}(var3 int)
            is
            begin
                create table if not exists {self.t_name}(col1 int);
                insert into {self.t_name} values(var1);
                insert into {self.t_name} values(var3);
            end;
            begin
                var4:=9;
                {self.proc_name}(var4);
            end {self.pkg_name};'''
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'CREATE PACKAGE BODY', '执行失败：' + text)

        text = '----step5: 调用包定义存储过程 expect: 成功----'
        self.LOG.info(text)
        cmd = f"call {self.pkg_name}.{self.proc_name}(1);"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertTrue(not sql_res, '执行失败：' + text)

        text = '----step6: 查询 expect: 成功----'
        self.LOG.info(text)
        cmd = f"select * from {self.t_name};"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        expect = [(1,), (9,), (1,), (1,)]
        self.assertEqual(sql(), expect, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step7: 删除表、存储过程、包 expect: 成功----'
        self.LOG.info(text)
        cmd = f"drop table if exists {self.t_name}; " \
            f"drop procedure if exists {self.proc_name}; " \
            f"drop package {self.pkg_name};"
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step8: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0049 end----'
        self.LOG.info(text)
