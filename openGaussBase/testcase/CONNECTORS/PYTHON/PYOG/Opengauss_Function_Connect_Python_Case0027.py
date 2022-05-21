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
Case Name   : openGauss模式连接数据库，子查询
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.子查询
    --3.1建表插入数据
    --3.2子查询exists
    --3.3子查询in
    --3.4子查询any/some
    --3.5子查询all
    --3.6删除表
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.1~3.6执行成功
    4.执行成功，db.state返回'closed'
History     :
"""
import os
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython27(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0027 start----'
        self.LOG.info(text)

    def test_conn(self):
        text = '----step1: 配置pg_hba入口 expect: 成功----'
        self.LOG.info(text)
        host_cmd = "ifconfig -a|grep inet6 -a2|" \
                   "grep broadcast|awk '{print $2}'"
        self.host = os.popen(host_cmd).readlines()[0].strip()
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.pri_user.db_user} ' \
            f'{self.host}/32 sha256"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res, text)

        text = '----step2: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.pri_user.db_user}:' \
            f'{self.pri_user.db_password}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        db = py_opengauss.open(conn_info)
        self.assertEqual('idle', db.state, text)

        text = '----step3: 子查询 expect: 成功----'
        self.LOG.info(text)

        text = '----step3.1: 建表插入数据 expect: 成功----'
        self.LOG.info(text)
        cmd = "drop table if exists t_py_27;" \
              "create table t_py_27(a int, b text);" \
              "insert into t_py_27 values(generate_series(1,1000), " \
              "generate_series(1,1000)||'test');" \
              "drop table if exists t_py_sub_27;" \
              "create table t_py_sub_27 as table t_py_27;"
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        text = '----step3.2: 子查询exists expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select count(*) from t_py_27 where exists ' \
              '(select a from t_py_sub_27 where a is not null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(1000,)], text)

        cmd = 'select count(*) from t_py_27 where not exists ' \
              '(select a from t_py_sub_27 where a is not null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(0,)], text)

        text = '----step3.3: 子查询in expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select count(*) from t_py_27 where a in ' \
              '(select a from t_py_sub_27 where a<100);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(99,)], text)

        cmd = 'select count(*) from t_py_27 where a not in ' \
              '(select a from t_py_sub_27 where a<100);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(901,)], text)

        text = '----step3.4: 子查询any/some expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select count(*) from t_py_27 where a = any ' \
              '(select a from t_py_sub_27 where a is not null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(1000,)], text)

        cmd = 'select count(*) from t_py_27 where a = any ' \
              '(select a from t_py_sub_27 where a is null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(0,)], text)

        cmd = 'select count(*) from t_py_27 where a = some ' \
              '(select a from t_py_sub_27 where a is not null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(1000,)], text)

        cmd = 'select count(*) from t_py_27 where a = some ' \
              '(select a from t_py_sub_27 where a is null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(0,)], text)

        text = '----step3.5: 子查询all expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select count(*) from t_py_27 where a = all ' \
              '(select a from t_py_sub_27 where a is not null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(0,)], text)

        cmd = 'select count(*) from t_py_27 where a = all ' \
              '(select a from t_py_sub_27 where a is null);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(1000,)], text)

        text = '----step3.6: 删除表 expect: 操作成功----'
        self.LOG.info(text)
        cmd = "drop table if exists t_py_27; " \
              "drop table if exists t_py_sub_27;"
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        text = '----step4: 断开连接 expect: 成功----'
        self.LOG.info(text)
        db.close()
        self.assertEqual('closed', db.state, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----Opengauss_Function_Connect_Python_Case0027 end----'
        self.LOG.info(text)
