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
Case Name   : openGauss模式连接数据库，set
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.使用set session...to命令设置当前模式
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


class ConnPython19(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0019 start----'
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

        text = '----step3: 使用set session...to命令设置当前模式 expect: 成功----'
        self.LOG.info(text)

        cmd = 'drop schema if exists myschema;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('DROP SCHEMA', None), text)

        cmd = 'create schema myschema;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('CREATE SCHEMA', None), text)

        cmd = 'set session current_schema to myschema;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = 'select current_schema;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('myschema',)], text)

        cmd = "select * from pg_settings where name = 'current_schema';"
        sql = db.prepare(cmd)
        expect = [('current_schema', 'myschema', None,
                   'Client Connection Defaults / Statement Behavior',
                   'Sets the schema search order for names '
                   'that are not schema-qualified.',
                   None, 'user', 'string', 'session', None, None, None,
                   '"$user",public', '"$user",public', None, None)]
        self.assertEqual(sql(), expect, text)

        cmd = 'set session current_schema to default;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = 'select current_schema;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('public',)], text)

        text = '----step4: 断开连接 expect: 成功----'
        self.LOG.info(text)
        db.close()
        self.assertEqual('closed', db.state, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----Opengauss_Function_Connect_Python_Case0019 end----'
        self.LOG.info(text)
