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
Case Name   : openGauss模式连接数据库，聚合查询
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.聚合查询
    --3.1建表插入数据
    --3.2sum
    --3.3max
    --3.4min
    --3.5avg
    --3.6first
    --3.7last
    --3.8count
    --3.9group by
    --3.10having
    --3.11删除表
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.1~3.11执行成功
    4.执行成功，db.state返回'closed'
History     :
"""
import os
import unittest
from decimal import Decimal

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython28(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0028 start----'
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

        text = '----step3: 聚合查询 expect: 成功----'
        self.LOG.info(text)

        text = '----step3.1: 建表插入数据 expect: 成功----'
        self.LOG.info(text)
        cmd = "drop table if exists t_py_28;" \
              "create table t_py_28(a int, b text);" \
              "insert into t_py_28 values (1, 'red'), (2, 'red'), " \
              "(3, 'yello'), (4, 'blue'), (5, 'blue');"
        self.LOG.info(cmd)
        res = db.execute(cmd)
        self.assertIsNone(res)

        text = '----step3.2: sum expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select sum(a) from t_py_28;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(15,)], text)

        text = '----step3.3: max expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select max(a) from t_py_28;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(5,)], text)

        text = '----step3.4: min expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select min(a) from t_py_28;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(1,)], text)

        text = '----step3.5: avg expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select avg(a) from t_py_28;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)

        text = '----step3.6: first expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select first(a) from t_py_28;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(1,)], text)

        text = '----step3.7: last expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select last(a) from t_py_28;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(5,)], text)

        text = '----step3.8: count expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select count(*) from t_py_28;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), [(5,)], text)

        text = '----step3.9: group by expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select count(b) as num, b from t_py_28 group by b ' \
              'order by num desc;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        expect = [(2, 'red'), (2, 'blue'), (1, 'yello')]
        self.assertEqual(sql(), expect, text)

        text = '----step3.10: having expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'select count(b) as num, b from t_py_28 group by b ' \
              'having num>1;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        expect = [(2, 'red'), (2, 'blue')]
        self.assertEqual(sql(), expect, text)

        text = '----step3.11: 删除表 expect: 操作成功----'
        self.LOG.info(text)
        cmd = "drop table if exists t_py_28;"
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

        text = '----Opengauss_Function_Connect_Python_Case0028 end----'
        self.LOG.info(text)
