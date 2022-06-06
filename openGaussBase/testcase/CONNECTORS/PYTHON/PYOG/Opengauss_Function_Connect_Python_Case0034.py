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
Case Name   : openGauss模式连接数据库，定义角色&授权
Description :
    1.新建有登录属性的角色并赋权
    2.配置pg_hba入口
    3.连接数据库
    4.角色u_py对表增删改查
    5.断开连接
    6.删除pg_hba入口
    7.删除用户
Expect      :
    1.执行成功
    2.执行成功
    3.连接成功，db.state返回'idle'
    4.执行成功
    5.执行成功，db.state返回'closed'
    6.执行成功
    7.执行成功
History     :
"""
import os
import re
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython34(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.user = 'u_py_34'
        text = '----Opengauss_Function_Connect_Python_Case0034 start----'
        self.LOG.info(text)

    def test_conn(self):
        text = '----step1: 新建有登录属性的角色并赋权 expect: 成功----'
        self.LOG.info(text)
        sql_cmd = f"drop table if exists t_py_34;" \
            f"drop role if exists {self.user};" \
            f"create role {self.user} with login " \
            f"password '{macro.PASSWD_INITIAL}';" \
            f"create table t_py_34(a int, b text);" \
            f"grant all privileges on t_py_34 to {self.user}"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.LOG.info(sql_res)
        pattern = f"{self.constant.TABLE_DROP_SUCCESS}.*" \
            f"{self.constant.DROP_ROLE_SUCCESS_MSG}.*" \
            f"{self.constant.CREATE_ROLE_SUCCESS_MSG}.*" \
            f"{self.constant.TABLE_CREATE_SUCCESS}.*" \
            f"{self.constant.GRANT_SUCCESS_MSG}"
        self.assertIsNotNone(re.search(pattern, sql_res, re.S))

        text = '----step2: 配置pg_hba入口 expect: 成功----'
        self.LOG.info(text)
        host_cmd = "ifconfig -a|grep inet6 -a2|" \
                   "grep broadcast|awk '{print $2}'"
        self.host = os.popen(host_cmd).readlines()[0].strip()
        self.assertIsNotNone(self.host)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.user} ' \
            f'{self.host}/32 sha256"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res, text)

        text = '----step3: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.user}:' \
            f'{macro.PASSWD_INITIAL}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        db = py_opengauss.open(conn_info)
        self.assertEqual('idle', db.state, text)

        text = '----step4: 角色u_py对表增删改查 expect: 成功----'
        self.LOG.info(text)
        cmd = f"insert into t_py_34 values (generate_series(1,100000), " \
            f"generate_series(1,100000)||'test');" \
            f"delete from t_py_34 where a<100;" \
            f"update t_py_34 set b=b||'new';" \
            f"select count(*) from t_py_34;"
        self.LOG.info(cmd)
        sql_res = db.execute(cmd)
        self.assertIsNone(sql_res)

        text = '----step5: 断开连接 expect: 成功----'
        self.LOG.info(text)
        db.close()
        self.assertEqual('closed', db.state, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text1 = '----step6: 删除pg_hba入口 expect: 成功----'
        self.LOG.info(text1)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.user} {self.host}/32"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)

        text2 = '----step7: 删除用户 expect: 成功----'
        self.LOG.info(text2)
        sql_cmd = f'drop table if exists t_py_34;' \
            f'drop role if exists {self.user}; '
        self.LOG.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.LOG.info(sql_res)

        text = '----Opengauss_Function_Connect_Python_Case0034 end----'
        self.LOG.info(text)

        text = '----断言teardown执行成功----'
        self.LOG.info(text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res, text1)

        expect = f'{self.constant.TABLE_DROP_SUCCESS}(.*)' \
            f'{self.constant.DROP_ROLE_SUCCESS_MSG}'
        regex_res = re.match(expect, sql_res, re.S)
        self.assertIsNotNone(regex_res, text2)
