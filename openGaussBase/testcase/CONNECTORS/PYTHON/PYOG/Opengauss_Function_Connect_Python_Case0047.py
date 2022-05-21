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
Case Name   : openGauss模式连接数据库，定义存储过程
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.建表
    4.创建存储过程
    5.调用存储过程
    6.删除表、存储过程
    7.断开连接
    8.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3~6.执行成功
    7.执行成功，db.state返回'closed'
    8.执行成功
History     :
"""
import os
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython47(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_47'
        self.p_name = 'p_py_47'
        text = '----Opengauss_Function_Connect_Python_Case0047 start----'
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

        text = '----step3: 建表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table if exists {self.t_name};
            create table {self.t_name}(
                t_id int,
                t_name varchar(20) not null default ''
            );'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)
        self.assertIsNone(sql_res, '执行失败：' + text)

        text = '----step4: 创建存储过程 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create or replace procedure {self.p_name}\
            (a int, b varchar(20))  as 
            declare 
                id int := a;
                name varchar(20) := b;
            begin
                insert into {self.t_name} values(id, name); 
            end;'''
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res,
                         self.constant.CREATE_PROCEDURE_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step5.1: select调用存储过程 expect: 成功----'
        self.LOG.info(text)
        cmd = f"select {self.p_name}($1, $2);"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(1, 'test1'), [('',)], '执行失败：' + text)

        text = '----step5.2: call调用存储过程 expect: 成功----'
        self.LOG.info(text)
        cmd = f"call {self.p_name}(2, 'test2');"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertTrue(not sql_res, '执行失败：' + text)

        text = '----step5.3: proc方法调用存储过程 expect: 成功----'
        self.LOG.info(text)
        cmd = f"select oid from pg_proc where proname = '{self.p_name}'"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertTrue(sql_res, '执行失败：' + text)

        proc = self.db.proc(sql_res)
        self.assertTrue(not proc(3, 'test3'), '执行失败：' + text)

        text = '----step5.4: 查看表数据 expect: 成功----'
        self.LOG.info(text)
        cmd = f"select count(*) from {self.t_name};"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 3, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step13: 删除索引和表 expect: 成功----'
        self.LOG.info(text)
        cmd = f"drop procedure if exists {self.p_name}; " \
            f"drop table if exists {self.t_name};"
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step14: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0047 end----'
        self.LOG.info(text)
