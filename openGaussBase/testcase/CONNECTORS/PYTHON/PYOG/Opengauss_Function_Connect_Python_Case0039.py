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
Case Name   : openGauss模式连接数据库，定义模式
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建一个角色u_py
    4.为用户u_py创建一个同名schema，子命令创建的表t_py_39和v_py_39的拥有者为u_py
    5.将当前模式更名为ds_new
    6.删除schema,u_py
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

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython39(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.user = 'u_py_39'
        text = '----Opengauss_Function_Connect_Python_Case0039 start----'
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
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res, text)

        text = '----step2: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.pri_user.db_user}:' \
            f'{self.pri_user.db_password}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        self.LOG.info(conn_info)
        db = py_opengauss.open(conn_info)
        self.assertEqual('idle', db.state, text)

        text = '----step3: 创建一个角色u_py expect: 成功----'
        self.LOG.info(text)
        cmd = f"create role {self.user} identified by " \
            f"'{macro.PASSWD_INITIAL}';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_ROLE_SUCCESS_MSG, None),
                         text)

        text = '----step4: 为用户u_py创建一个同名schema，' \
               '子命令创建的表t_py_39和v_py_39的拥有者为u_py expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create schema authorization {self.user}
            create table t_py_39 (title text, release date, awards text[])      
            create view v_py_39 as         
            select title, release from t_py_39 where awards is not null;'''
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_SCHEMA_SUCCESS_MSG,
                                 None), text)

        text = '----step5: 将当前模式更名为sc_new_39 expect: 成功----'
        self.LOG.info(text)
        cmd = f'alter schema {self.user} rename to sc_new_39;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.ALTER_SCHEMA_SUCCESS_MSG,
                                 None), text)

        text = '----step6: 删除schema,u_py expect: 成功----'
        self.LOG.info(text)
        cmd = f'drop schema sc_new_39 cascade; ' \
            f'drop user {self.user} cascade;'
        self.LOG.info(cmd)
        sql_res = db.execute(cmd)
        self.assertIsNone(sql_res)

        text = '----step6: 断开连接 expect: 成功----'
        self.LOG.info(text)
        db.close()
        self.assertEqual('closed', db.state, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----Opengauss_Function_Connect_Python_Case0039 end----'
        self.LOG.info(text)
