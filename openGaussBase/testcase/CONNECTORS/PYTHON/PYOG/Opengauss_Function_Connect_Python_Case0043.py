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
Case Name   : openGauss模式连接数据库，定义临时表
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建普通临时表
    4.创建本地临时表，并指定提交事务时删除该临时表数据
    5.创建全局临时表，并指定会话结束时删除该临时表数据
    6.删除表
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

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython43(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 'tmp_t_py_43'
        text = '----Opengauss_Function_Connect_Python_Case0043 start----'
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

        text = '----step3: 创建普通临时表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create temporary table {self.t_name}(
            id        integer     not null,
            name      char(16)    not null,
            address   varchar(50),
            postcode  char(6)
            );'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step4: 创建本地临时表，并指定提交事务时删除该临时表数据 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create temporary table {self.t_name}_local(
            id         integer      not null,
            name       char(16)     not null,
            address    varchar(50),
            postcode   char(6)
            ) on commit delete rows;'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

        text = '----step5: 创建全局临时表，并指定会话结束时删除该临时表数据 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create global temporary table {self.t_name}_global(
            id         integer      not null,
            name       char(16)     not null,
            address    varchar(50),
            postcode   char(6)
            ) on commit preserve rows;'''
        self.LOG.info(cmd)
        sql = self.db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS, None),
                         '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step6: 删除表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'drop table if exists {self.t_name}_global cascade;'
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step7: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0043 end----'
        self.LOG.info(text)
