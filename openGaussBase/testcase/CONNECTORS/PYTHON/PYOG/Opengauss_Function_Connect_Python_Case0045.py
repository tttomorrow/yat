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
Case Name   : openGauss模式连接数据库，定义分区表
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建范围分区表
    4.创建间隔分区表
    5.创建列表分区表
    6.创建哈希分区表
    7.创建列存分区表
    8.删除表
    9.断开连接
    10.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3~8.执行成功
    9.执行成功，db.state返回'closed'
    10.执行成功
History     :
"""
import os
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython45(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_45'
        text = '----Opengauss_Function_Connect_Python_Case0045 start----'
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

        text = '----step3: 创建范围分区表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_1(
                t_id integer(20),
                t_name varchar(20) not null default ''
            )
            partition by range (t_id)
            (
                partition p1 values less than (100),
                partition p2 values less than (200),
                partition p3 values less than (300),
                partition p4 values less than (maxvalue)
            );'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step4: 创建间隔分区表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_2(
                t_id integer(20),
                t_name varchar(20) not null default '',
                t_date date not null default ''
            )
            partition by range (t_date)
            interval('6 month')
            (
                partition p1 values less than ('2001-01-01 00:00:00'),
                partition p2 values less than ('2001-07-01 00:00:00')
            );'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step5: 创建列表分区表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_3(
                t_id int, 
                t_name varchar(20) not null default ''
            )
            partition by list (t_id)
            (
                partition p1 values (2000),
                partition p2 values (3000),
                partition p3 values (4000),
                partition p4 values (5000)
            );'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step6: 创建哈希分区表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_4 (
                t_id int, 
                t_name varchar(20) not null default ''
            )
            partition by hash(t_id)
            (
                partition p1,
                partition p2
            );'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step7: 创建列存分区表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}_5(
                t_id integer(20),
                t_name varchar(20) not null default ''
            )with (orientation = column)
            partition by range (t_id)
            (
                partition p1 values less than (100),
                partition p2 values less than (200),
                partition p3 values less than (300),
                partition P4 values less than (maxvalue)
            );'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step8: 删除表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'drop table if exists {self.t_name}_1 cascade; ' \
            f'drop table if exists {self.t_name}_2 cascade; ' \
            f'drop table if exists {self.t_name}_3 cascade; ' \
            f'drop table if exists {self.t_name}_4 cascade; ' \
            f'drop table if exists {self.t_name}_5 cascade;'
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step9: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0045 end----'
        self.LOG.info(text)
