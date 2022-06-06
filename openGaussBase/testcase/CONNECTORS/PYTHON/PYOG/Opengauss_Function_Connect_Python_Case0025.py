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
Case Name   : openGauss模式连接数据库，操作会话
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.操作会话
    --3.1创建模式ds
    --3.2设置模式搜索路径
    --3.3设置日期时间风格为传统的POSTGRES风格(日在月前)
    --3.4设置当前会话的字符编码为UTF8。
    --3.5设置时区为加州伯克利。
    --3.6设置时区为意大利。
    --3.7设置当前模式
    --3.8设置XML OPTION为DOCUMENT
    --3.9创建角色joe，并设置会话的角色为joe
    --3.10切换到默认用户
    --3.11删除ds模式,用户joe
    4.断开连接
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.1~3.11执行成功
    4.执行成功，db.state返回'closed'
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


class ConnPython25(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0025 start----'
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

        text = '----step3: 操作会话 expect: 成功----'
        self.LOG.info(text)

        text = '----step3.1: 创建模式ds expect: 成功----'
        self.LOG.info(text)
        cmd = 'drop schema if exists ds; create schema ds;'
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        cmd = "select n.nspname as name from pg_catalog.pg_namespace n " \
              "where n.nspname !~ '^pg_' and " \
              "n.nspname <> 'information_schema' and " \
              "name='ds';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('ds',)], text)

        text = '----step3.2: 设置模式搜索路径 expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'set search_path to ds, public;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = 'show search_path;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('ds, public',)], text)

        text = '----step3.3: 设置日期时间风格为传统的POSTGRES风格(日在月前) expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'set datestyle to postgres, dmy;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = 'select to_char(now());'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        regex_res = re.match(r"Mon|Tue|Sat|Sun|Wed|Thu|Fri", sql()[0][0])
        self.assertIsNotNone(regex_res)

        cmd = 'set datestyle to iso, ymd;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = 'select to_char(now());'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        regex_res = re.match(r'\d{4}-\d{2}-\d{2}', sql()[0][0])
        self.assertIsNotNone(regex_res)

        text = '----step3.4: 设置当前会话的字符编码为UTF8 expect: 操作成功----'
        self.LOG.info(text)
        cmd = "drop table if exists t_py_25; " \
              "create table t_py_25(a int, b text);"
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        cmd = "insert into t_py_25 values(1, '中文测试');"
        self.LOG.info(cmd)
        with self.assertRaises(UnicodeEncodeError):
            db.prepare(cmd)

        cmd = "alter session set names 'utf8';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = "insert into t_py_25 values(2, '中文测试');"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('INSERT', 1), text)

        cmd = "drop table if exists t_py_25;"
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        text = '----step3.5: 设置时区为加州伯克利 expect: 操作成功----'
        self.LOG.info(text)
        cmd = "set time zone 'pst8pdt';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = "show time zone;"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('PST8PDT',)], text)

        text = '----step3.6: 设置时区为意大利 expect: 操作成功----'
        self.LOG.info(text)
        cmd = "set time zone 'europe/rome';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = "show time zone;"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('Europe/Rome',)], text)

        text = '----step3.7: 设置当前模式 expect: 操作成功----'
        self.LOG.info(text)
        cmd = "alter session set current_schema to tpcds;"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = "show current_schema;"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('tpcds',)], text)

        text = '----step3.8: 设置XML OPTION为DOCUMENT expect: 操作成功----'
        self.LOG.info(text)
        cmd = "alter session set xml option document;"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        text = '----step3.9: 创建角色joe，并设置会话的角色为joe expect: 操作成功----'
        self.LOG.info(text)
        cmd = f"drop role if exists joe; " \
            f"create role joe with password '{macro.PASSWD_INITIAL}'; " \
            f"alter session set session authorization joe " \
            f"password '{macro.PASSWD_INITIAL}';"
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        cmd = "select definer_current_user();"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [('joe',)], text)

        text = '----step3.10: 切换到默认用户 expect: 操作成功----'
        self.LOG.info(text)
        cmd = "alter session set session authorization default;"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('SET', None), text)

        cmd = "select definer_current_user();"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(self.pri_user.db_user,)], text)

        text = '----step3.11: 删除ds模式,用户joe expect: 操作成功----'
        self.LOG.info(text)
        cmd = "drop schema if exists ds; drop role if exists joe;"
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

        text = '----Opengauss_Function_Connect_Python_Case0025 end----'
        self.LOG.info(text)
