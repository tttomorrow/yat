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
Case Name   : openGauss模式连接数据库，定义索引
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.建表
    4.创建普通的唯一索引
    5.创建指定B-tree索引
    6.创建hash索引
    7.创建表达式索引
    8.创建global全局索引
    9.创建local全局索引
    10.创建gin索引
    11.重建索引
    12.重命名索引
    13.删除表
    14.断开连接
    15.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3~13.执行成功
    14.执行成功，db.state返回'closed'
    15.执行成功
History     :
"""
import os
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython46(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_46'
        self.i_name = 'i_py_46'
        text = '----Opengauss_Function_Connect_Python_Case0046 start----'
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
            drop table if exists {self.t_name}_1;
            create table {self.t_name}(
                t_id integer(20),
                t_name varchar(20) not null default ''
            );
            create table {self.t_name}_1(
                t_id integer(20),
                t_name varchar(20) not null default ''
            )
            partition by range (t_id)
            (
                partition p1 values less than (100),
                partition p2 values less than (200),
                partition p3 values less than (300),
                partition P4 values less than (maxvalue)
            );'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)
        self.assertIsNone(sql_res, '执行失败：' + text)

        text = '----step4: 创建普通的唯一索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create unique index {self.i_name}_1 on {self.t_name}(t_id);"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step5: 创建指定B-tree索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create index {self.i_name}_2 on {self.t_name} " \
            f"using btree(t_id);"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step6: 创建hash索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create index {self.i_name}_3 on {self.t_name} " \
            f"using hash(t_id);"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step7: 创建表达式索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create index {self.i_name}_4 on {self.t_name}" \
            f"(substr(t_name, 1, 4));"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step8: 创建global全局索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create index {self.i_name}_5 on {self.t_name}_1(t_id) global;"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step8.1: 删除global全局索引，全局分区索引和本地分区索引不应位于同一列 expect: 成功----'
        self.LOG.info(text)
        cmd = f"drop index if exists {self.i_name}_5;"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.DROP_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step9: 创建local全局索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create index {self.i_name}_6 on {self.t_name}_1(t_id) local \
                (partition p1,partition p2,partition p3,partition p4);"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step10: 创建gin索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create index {self.i_name}_7 on {self.t_name} " \
            f"using gin(to_tsvector('english', t_name));"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step11: 重建索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"reindex index {self.i_name}_1;"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.REINDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

        text = '----step12: 重命名索引 expect: 成功----'
        self.LOG.info(text)
        cmd = f"alter index if exists {self.i_name}_1 " \
            f"rename to {self.i_name}_new;"
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.ALTER_INDEX_SUCCESS_MSG,
                                 None), '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step13: 删除索引和表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'drop index if exists {self.i_name}_new; ' \
            f'drop index if exists {self.i_name}_2; ' \
            f'drop index if exists {self.i_name}_3; ' \
            f'drop index if exists {self.i_name}_4; ' \
            f'drop index if exists {self.i_name}_6; ' \
            f'drop index if exists {self.i_name}_7; ' \
            f'drop table if exists {self.t_name} cascade; ' \
            f'drop table if exists {self.t_name}_1 cascade;'
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step14: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0046 end----'
        self.LOG.info(text)
