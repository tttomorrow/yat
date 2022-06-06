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
Case Name   : openGauss模式连接数据库，定义列存表
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建普通列存表
    4.创建局部聚簇存储的列存表
    5.创建一个带压缩的列存表
    6.删除表
    7.断开连接
    8.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功
    4.执行成功
    5.执行成功
    6.执行成功
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


class ConnPython44(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_44'
        text = '----Opengauss_Function_Connect_Python_Case0044 start----'
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

        text = '----step3: 创建普通列存表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_1(
            w_warehouse_sk     integer      not null,
            w_warehouse_id     char(16)     not null,
            w_warehouse_name   varchar(20),
            w_gmt_offset       decimal(5,2)
            ) with (orientation = column);'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step4: 创建局部聚簇存储的列存表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_2(
            w_warehouse_sk    integer       not null,
            w_warehouse_id    char(16)      not null,
            w_warehouse_name  varchar(20),
            w_gmt_offset      decimal(5,2),
            partial cluster key(w_warehouse_sk, w_warehouse_id)
            ) with (orientation = column);'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step5: 创建一个带压缩的列存表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_3(
            w_warehouse_sk     integer      not null,
            w_warehouse_id     char(16)     not null,
            w_warehouse_name   varchar(20),
            w_gmt_offset       decimal(5,2)
            ) with (orientation = column, compression=high);'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step6: 删除表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'drop table if exists {self.t_name}_1 cascade; ' \
            f'drop table if exists {self.t_name}_2 cascade; ' \
            f'drop table if exists {self.t_name}_3 cascade;'
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step7: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0044 end----'
        self.LOG.info(text)
