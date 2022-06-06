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
Case Name   : openGauss模式连接数据库，定义表，表数据不写入预写日志
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建表并指定该表数据不写入预写日志
    4.插入数据、查询
    5.删除表
    6.断开连接
    7.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，self.db.state返回'idle'
    3.执行成功
    4.执行成功
    6.执行成功，self.db.state返回'closed'
    7.执行成功
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


class ConnPython42(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_42'
        text = '----Opengauss_Function_Connect_Python_Case0042 start----'
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

        text = '----step3: 创建表并指定该表数据不写入预写日志 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create unlogged table {self.t_name}(
            w_warehouse_sk    integer     not null,
            w_warehouse_id    char(16)    not null,
            w_warehouse_name  varchar(20),
            w_gmt_offset      decimal(5,2)
            );'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step4: 插入数据、查询 expect: 成功----'
        self.LOG.info(text)
        cmd = f"insert into {self.t_name} values (101, '101', 'nw', 10.1);"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), ('INSERT', 1), '执行失败：' + text)

        cmd = f"select * from {self.t_name};"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        expect_msg = [(101, '101             ', 'nw', Decimal('10.10'))]
        self.assertEqual(sql(), expect_msg, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step5: 删除表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'drop table if exists {self.t_name} cascade;'
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step6: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0042 end----'
        self.LOG.info(text)
