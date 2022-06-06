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
Case Name   : openGauss模式连接数据库，连接信息错误
Description :
    1.创建库、用户，用户密码不含特殊字符，并赋权
    2.配置pg_hba入口
    3.连接数据库
Expect      :
    1.执行成功
    2.执行成功
    3.连接失败，有相应提示信息
History     :
"""
import os
import re
import unittest

import py_opengauss
from py_opengauss.exceptions import AuthenticationSpecificationError, \
    ClientCannotConnectError, ConnectionRejectionError, ServerNotReadyError
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython8(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.db_name = 'py_db'
        self.db_user = 'py_user'
        text = '----Opengauss_Function_Connect_Python_Case0008 start----'
        self.LOG.info(text)

    def test_conn(self):
        text = '----step1: 创建库、用户，用户密码不含特殊字符，并赋权 expect: 成功----'
        self.LOG.info(text)
        sql_cmd = f"drop database if exists {self.db_name}; " \
            f"create database {self.db_name}; " \
            f"create user {self.db_user} with password " \
            f"'{macro.PASSWD_INITIAL}'; " \
            f"grant all privileges on database {self.db_name} " \
            f"to {self.db_user};"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.LOG.info(sql_res)
        expect = f'{self.constant.DROP_DATABASE_SUCCESS}(.*)' \
            f'{self.constant.CREATE_DATABASE_SUCCESS}(.*)' \
            f'{self.constant.CREATE_ROLE_SUCCESS_MSG}(.*)' \
            f'{self.constant.GRANT_SUCCESS_MSG}'
        regex_res = re.search(expect, sql_res, re.S)
        self.assertIsNotNone(regex_res, text)

        text = '----step2: 配置pg_hba入口 expect: 成功----'
        self.LOG.info(text)
        host_cmd = "ifconfig -a|grep inet6 -a2|" \
                   "grep broadcast|awk '{print $2}'"
        self.host = os.popen(host_cmd).readlines()[0].strip()
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.db_name} {self.db_user} ' \
            f'{self.host}/32 sha256"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res, text)

        text = '----step3: 连接数据库 expect: 连接失败，有相应提示信息----'
        self.LOG.info(text)
        conn_info = f'opengauss://er_user:{macro.PASSWD_INITIAL}@' \
            f'{self.pri_user.db_host}:{self.pri_user.db_port}/' \
            f'{self.db_name}'
        with self.assertRaises(
                (ClientCannotConnectError, AuthenticationSpecificationError)):
            py_opengauss.open(conn_info)

        conn_info = f'opengauss://{self.db_user}:er_password@' \
            f'{self.pri_user.db_host}:{self.pri_user.db_port}/' \
            f'{self.db_name}'
        with self.assertRaises(
                (ClientCannotConnectError, AuthenticationSpecificationError)):
            py_opengauss.open(conn_info)

        conn_info = f'opengauss://{self.db_user}:{macro.PASSWD_INITIAL}@' \
            f'10.10.10.10:{self.pri_user.db_port}/' \
            f'{self.db_name}'
        with self.assertRaises(
                (ClientCannotConnectError, ConnectionRejectionError)):
            py_opengauss.open(conn_info)

        er_port = str(int(self.pri_user.db_port) + 1)
        conn_info = f'opengauss://{self.db_user}:{macro.PASSWD_INITIAL}@' \
            f'{self.pri_user.db_host}:{er_port}/' \
            f'{self.db_name}'
        with self.assertRaises(
                (ClientCannotConnectError, ServerNotReadyError)):
            py_opengauss.open(conn_info)

        conn_info = f'opengauss://{self.db_user}:{macro.PASSWD_INITIAL}@' \
            f'{self.pri_user.db_host}:{self.pri_user.db_port}/' \
            f'er_db'
        with self.assertRaises(
                (ClientCannotConnectError, AuthenticationSpecificationError)):
            py_opengauss.open(conn_info)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text_1 = '----还原pg_hba入口 expect: 成功----'
        self.LOG.info(text_1)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.db_name} {self.db_user} ' \
            f'{self.host}/32"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)

        text_2 = '----删除库、用户，用户密码 expect: 成功----'
        self.LOG.info(text_2)
        sql_cmd = f'drop database if exists {self.db_name}; ' \
            f'drop user if exists {self.db_user};'
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.LOG.info(sql_res)

        text = '----Opengauss_Function_Connect_Python_Case0008 end----'
        self.LOG.info(text)

        text = '----断言teardown执行成功----'
        self.LOG.info(text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res, text_1)

        expect = f'{self.constant.DROP_DATABASE_SUCCESS}(.*)' \
            f'{self.constant.DROP_ROLE_SUCCESS_MSG}'
        regex_res = re.match(expect, sql_res, re.S)
        self.assertIsNotNone(regex_res, text_2)
