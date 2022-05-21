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
Case Name   : openGauss模式连接数据库，定义游标
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.创建表，插入数据
    4.开始事务，定义游标
    5.删除表、视图
    6.断开连接
    7.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功，回显CREATE TABLE, INSERT 0 100
    4.执行成功，回显START TRANSACTION.*DECLARE CURSOR.*MOVE 3.*(2 rows).*CLOSE CURSOR
        DECLARE CURSOR.*(1 row).*COMMIT.*(1 row).*CLOSE CURSOR
    5.执行成功
    6.执行成功，db.state返回'closed'
    7.执行成功
History     :
"""
import os
import re
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython51(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_51'
        self.cur_name = 'cur_py_51'
        text = '----Opengauss_Function_Connect_Python_Case0051 start----'
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

        text = '----step3: 创建表，插入数据 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table if exists {self.t_name};
            create table {self.t_name}(id int, name varchar(20));
            insert into {self.t_name} values (generate_series(1,100), \
            generate_series(1,100)||'test');'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)
        self.LOG.info(sql_res)
        self.assertIsNone(sql_res, '执行失败：' + text)

        text = '----step4: 开始事务,定义游标 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''--开始事务
            start transaction;
            --定义一个名为{self.cur_name}_1的游标
            cursor {self.cur_name}_1 for \
            select * from {self.t_name} order by id;
            --忽略游标{self.cur_name}_1的前3行
            move forward 3 from {self.cur_name}_1;
            --抓取游标{self.cur_name}_1的前2行
            fetch 2 from {self.cur_name}_1;
            --关闭游标{self.cur_name}_1
            close {self.cur_name}_1;

            --创建一个with hold游标{self.cur_name}_2
            declare {self.cur_name}_2 cursor with hold for \
            select * from {self.t_name} order by id;
            --抓取头1行到游标{self.cur_name}_2里
            fetch forward 1 from {self.cur_name}_2;
            --结束事务
            end;

            --抓取下一行到游标cur_py_51_2里
            fetch forward 1 from cur_py_51_2;
            --关闭游标
            close cur_py_51_2;'''
        result = list()
        for c in re.split('--.*\n', cmd):
            if c:
                self.LOG.info(c.strip())
                sql_res = self.db.prepare(c.strip()).first()
                self.LOG.info(sql_res)
                result.append(sql_res)
        expect = ['START TRANSACTION', 'DECLARE CURSOR', 3, (4, '4test'),
                  'CLOSE CURSOR', 'DECLARE CURSOR', (1, '1test'), 'COMMIT',
                  (2, '2test'), 'CLOSE CURSOR']
        self.assertEqual(result, expect, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step5: 删除表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table {self.t_name} cascade;'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step6: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0051 end----'
        self.LOG.info(text)
