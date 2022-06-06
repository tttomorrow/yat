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
Case Name   : openGauss模式连接数据库，普通查询
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.普通查询
    --3.1建表插入数据
    --3.2查询数据
    --3.3删除表
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.1~3.3执行成功
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


class ConnPython26(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0026 start----'
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

        text = '----step3: 普通查询 expect: 成功----'
        self.LOG.info(text)

        text = '----step3.1: 建表插入数据 expect: 成功----'
        self.LOG.info(text)
        cmd = "drop table if exists t_py_26; " \
              "create table t_py_26(a int, b text); " \
              "insert into t_py_26 values" \
              "(1, 'test1'), (2, 'test2'), (3, 'test3');"
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        text = '----step3.2: 查询数据 expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select * from t_py_26;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        expect = [(1, 'test1'), (2, 'test2'), (3, 'test3')]
        self.assertEqual(sql(), expect, text)

        cmd = 'select a, b from t_py_26;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), expect, text)

        cmd = 'select *, a as c from t_py_26;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        expect = [(1, 'test1', 1), (2, 'test2', 2), (3, 'test3', 3)]
        self.assertEqual(sql(), expect, text)

        cmd = 'select * from t_py_26 where a>1;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(2, 'test2'), (3, 'test3')], text)

        text = '----step3.3: 删除ds模式,用户joe expect: 操作成功----'
        self.LOG.info(text)
        cmd = "drop table if exists t_py_26;"
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

        text = '----Opengauss_Function_Connect_Python_Case0026 end----'
        self.LOG.info(text)
