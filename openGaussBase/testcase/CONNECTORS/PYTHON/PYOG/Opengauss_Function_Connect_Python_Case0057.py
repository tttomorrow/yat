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
Case Name   : openGauss模式连接数据库，非数值类型校验
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.非数值类型校验
    3.1建表
    3.2插入数据
    3.3删除表
    4.断开连接
    5.关闭pg_hba入口
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功
    3.1执行成功，回显CREATE TABLE
    3.2执行成功，执行结果与gsql执行结果一致
    3.3执行成功，回显DROP TABLE
    4.执行成功，db.state返回'closed'
    5.执行成功
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


class ConnPython57(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_57'
        text = '----Opengauss_Function_Connect_Python_Case0057 start----'
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

        text = '----step3: 非数值类型校验 expect: 成功----'
        self.LOG.info(text)
        text = '----step3.1: 建表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''create table {self.t_name}  
            (
                col1 money, --货币类型
                col2 boolean, --布尔型
                col3 CHAR(4), --字符类型
                col4 CHARACTER(4), 
                col5 NCHAR(4),
                col6 VARCHAR(10),
                col7 CHARACTER VARYING(10),
                col8 VARCHAR2(10),
                col9 NVARCHAR2(10),
                col10 TEXT,
                col11 CLOB,
                col12 BLOB, --二进制类型
                col13 RAW,
                col14 BYTEA,
                col15 DATE, --时间日期类型
                col16 TIME,
                col17 time with time zone,
                col18 timestamp,
                col19 timestamp with time zone,
                col20 SMALLDATETIME,
                col21 abstime,
                col22 cidr, --网络地址类型
                col23 inet,
                col24 macaddr,
                col25 BIT(3), --位串类型
                col26 BIT VARYING(5),
                col27 UUID, --UUID类型
                col28 tsvector, --文本搜索类型
                col29 tsquery,
                col30 json, --json类型
                col31 jsonb,
                set hll(14), --HLL类型
                col33 int4range, --范围类型
                col34 int8range,
                col35 numrange,
                col36 tsrange,
                col37 tstzrange,
                col38 daterange,
                col39 HASH16, --账本数据库HASH类型
                col40 HASH32
            );'''
        self.LOG.info(re.sub('--.*\n', '\n', cmd))
        sql_res = self.db.prepare(re.sub('--.*\n', '\n', cmd)).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, self.constant.CREATE_TABLE_SUCCESS,
                         '执行失败：' + text)

        text = '----step3.2: 插入数据 expect: 成功----'
        self.LOG.info(text)
        cmd = f"insert into {self.t_name} values ('52093.89'::money, " \
            f"true, 'aa', 'aa', 'aa', 'aa', 'aa', 'aa', 'aa', 'aa', " \
            f"'aa', empty_blob(), HEXTORAW('DEADBEEF'), E'\\xDEADBEEF', " \
            f"'1900-01-01 00:00:00', '1900-01-01 00:00:00 pst', " \
            f"'1900-01-01 00:00:00', '1900-01-01 00:00:00 pst', " \
            f"'1900-01-01 00:00:00', '1900-01-01 00:00:00', " \
            f"'1910-01-01 00:00:00', '10.10.10.10', '10.10.10.10', " \
            f"'08002b010203', B'10'::bit(3), B'00', " \
            f"'a0eebc999c0b4ef8bb6d6bb9bd380a11', 'test', 'test', " \
            f"'{{\"aa\":1}}'::json, '{{\"bb\":2}}'::jsonb, " \
            f"hll_empty(14,-1), '[1,10]', '[1,10]', '[0.00, 10.00]', " \
            f"'[1900-01-01 00:00:00, 2020-01-01 00:00:00]', " \
            f"'[1900-01-01 00:00:00 pst, 2020-01-01 00:00:00 pst]', " \
            f"'(1900-01-01, 2020-01-01)','ffff', " \
            f"'ffffffffffffffffffffffffffffffff');"
        self.LOG.info(cmd)
        sql_res = self.db.prepare(cmd).first()
        self.LOG.info(sql_res)
        self.assertEqual(sql_res, 1, '执行失败：' + text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step3.3: 删除表 expect: 成功----'
        self.LOG.info(text)
        cmd = f'''drop table if exists {self.t_name} cascade;'''
        self.LOG.info(cmd)
        sql_res = self.db.execute(cmd)

        text = '----step4: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.db.close()

        self.assertIsNone(sql_res, '执行失败：' + text)
        self.assertEqual('closed', self.db.state, '执行失败：' + text)

        text = '----Opengauss_Function_Connect_Python_Case0057 end----'
        self.LOG.info(text)
