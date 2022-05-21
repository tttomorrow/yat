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
Case Name   : openGauss模式连接数据库，定义视图
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建表，插入数据
    4.创建普通视图
    5.创建视图提供行级安全
    6.创建临时视图
    7.创建增量物化视图,增量刷新
    8.创建全量物化视图,全量刷新
    9.查询
    10.删除表、视图
    11.断开连接
    12.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功，回显CREATE TABLE, INSERT 0 100
    4.执行成功，回显CREATE VIEW
    5.执行成功，回显CREATE VIEW
    6.执行成功，回显CREATE VIEW
    7.执行成功，回显CREATE MATERIALIZED VIEW， REFRESH MATERIALIZED VIEW
    8.执行成功，回显CREATE MATERIALIZED VIEW， REFRESH MATERIALIZED VIEW
    9.执行成功，所有查询结果一致
    10.执行成功
    11.执行成功，db.state返回'closed'
    12.执行成功
History     :
"""
import os
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython50(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_50'
        self.v_name = 'v_py_50'
        text = '----Opengauss_Function_Connect_Python_Case0050 start----'
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

        text = '----step3: 创建表，插入数据 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table if exists {self.t_name};
            create table {self.t_name}(id int, name varchar(20));
            insert into {self.t_name} values (generate_series(1,100), \
            generate_series(1,100)||'test');'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)
        self.LOG.info(sql_res)
        self.assertIsNone(sql_res, '执行失败：' + text)

        text = '----step4: 创建普通视图 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create view {self.v_name} as select * from {self.t_name};"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_VIEW_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step5: 创建视图提供行级安全 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create view {self.v_name}_1 with (security_barrier=0) as " \
            f"select * from {self.t_name};"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_VIEW_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step6: 创建临时视图 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create temp view tmp_{self.v_name} as " \
            f"select * from {self.t_name};"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_VIEW_SUCCESS_MSG,
                         '执行失败：' + text)

        text = '----step7.1: 创建增量物化视图 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create incremental materialized view {self.v_name}_2 as " \
            f"select * from {self.t_name};"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'CREATE MATERIALIZED VIEW', '执行失败：' + text)

        text = '----step7.2: 增量刷新 expect: 成功----'
        self.LOG.info(text)
        cmd = f"refresh incremental materialized view {self.v_name}_2;"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'REFRESH MATERIALIZED VIEW', '执行失败：' + text)

        text = '----step8.1: 创建全量物化视图 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create materialized view {self.v_name}_3 as " \
            f"select * from {self.t_name};"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'CREATE MATERIALIZED VIEW', '执行失败：' + text)

        text = '----step8.2: 全量刷新 expect: 成功----'
        self.LOG.info(text)
        cmd = f"refresh materialized view {self.v_name}_3;"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 'REFRESH MATERIALIZED VIEW', '执行失败：' + text)

        text = '----step9: 查询 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''select count(*) from {self.v_name};
            select count(*) from {self.v_name}_1;
            select count(*) from tmp_{self.v_name};
            select count(*) from {self.v_name}_2;
            select count(*) from {self.v_name}_3;'''
        self.LOG.info(cmd)
        for c in cmd.splitlines():
            sql_res = self.db.prepare(c.strip()).first()
            self.LOG.info(sql_res)
            self.assertEqual(100, sql_res, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step10: 删除表、视图 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop view if exists {self.v_name};
            drop view if exists {self.v_name}_1;
            drop view if exists tmp_{self.v_name};
            drop materialized view if exists {self.v_name}_2;
            drop materialized view if exists {self.v_name}_3;
            drop table {self.t_name} cascade;'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step11: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0050 end----'
        self.LOG.info(text)
