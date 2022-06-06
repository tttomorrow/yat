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
Case Name   : openGauss模式连接数据库，hint
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.指定Scan方式的Hint
    4.断开连接
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功
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


class ConnPython16(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0016 start----'
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

        text = '----step3: 指定Scan方式的Hint expect: 成功----'
        self.LOG.info(text)

        cmd = 'drop table if exists t_py_16;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.TABLE_DROP_SUCCESS,
                                 None), text)

        cmd = 'create table t_py_16(id int, name varchar(20));'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS,
                                 None), text)

        cmd = 'create index i_py_16 on t_py_16(id);'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_INDEX_SUCCESS_MSG,
                                 None), text)

        cmd = "insert into t_py_16 values (generate_series(1, 100000), " \
              "generate_series(1, 100000)||'test');"
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('INSERT', 100000), text)

        cmd = 'explain (costs off) select /*+ indexscan(t_py_16 i_py_16) */' \
              ' id, name from t_py_16 where id > 100;'
        sql = db.prepare(cmd)
        expect = [('[Bypass]',), ('Index Scan using i_py_16 on t_py_16',),
                  ('  Index Cond: (id > 100)',)]
        self.assertEqual(sql(), expect, text)

        cmd = 'drop table if exists t_py_16;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.TABLE_DROP_SUCCESS,
                                 None), text)

        text = '----step4: 断开连接 expect: 成功----'
        self.LOG.info(text)
        db.close()
        self.assertEqual('closed', db.state, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----Opengauss_Function_Connect_Python_Case0016 end----'
        self.LOG.info(text)
