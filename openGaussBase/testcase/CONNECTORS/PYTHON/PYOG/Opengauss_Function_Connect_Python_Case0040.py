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
Case Name   : openGauss模式连接数据库，定义表空间
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建表空间
    4.创建用户u_py_40
    5.重命名表空间
    6.改变表空间的所有者
    7.删除表空间、用户
    8.断开连接
    9.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功
    4.执行成功
    5.执行成功
    6.执行成功
    7.执行成功
    8.执行成功，db.state返回'closed'
    9.执行成功
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


class ConnPython40(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.user = 'u_py_40'
        text = '----Opengauss_Function_Connect_Python_Case0040 start----'
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

        text = '----step3: 创建表空间 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create tablespace ts_py_40 relative location " \
            f"'tablespace1';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('CREATE TABLESPACE', None), text)

        text = '----step4: 创建用户u_py_40 expect: 成功----'
        self.LOG.info(text)
        cmd = f"create role {self.user} identified by " \
            f"'{macro.PASSWD_INITIAL}';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_ROLE_SUCCESS_MSG,
                                 None), text)

        text = '----step5: 重命名表空间 expect: 成功----'
        self.LOG.info(text)
        cmd = f'alter tablespace ts_py_40 rename to ts_new_40;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('ALTER TABLESPACE', None), text)

        text = '----step6: 改变表空间的所有者 expect: 成功----'
        self.LOG.info(text)
        cmd = f'alter tablespace ts_new_40 owner to {self.user};'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('ALTER TABLESPACE', None), text)

        text = '----step7: 删除表空间、用户 expect: 成功----'
        self.LOG.info(text)
        cmd = 'drop tablespace ts_new_40;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('DROP TABLESPACE', None), text)

        cmd = f'drop user {self.user} cascade;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.DROP_ROLE_SUCCESS_MSG, None),
                         text)

        text = '----step8: 断开连接 expect: 成功----'
        self.LOG.info(text)
        db.close()
        self.assertEqual('closed', db.state, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----Opengauss_Function_Connect_Python_Case0040 end----'
        self.LOG.info(text)
