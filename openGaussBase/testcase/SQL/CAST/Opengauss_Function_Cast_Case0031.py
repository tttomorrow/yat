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
Case Type   : Cast
Case Name   : 输入类型是同一个类型范畴，则选择该类型范畴的首选类型
Description :
    1.查看执行计划,输入类型int,union类型float8
    2.查看执行计划,输入类型float8,union类型int,NUMBER
    3.查看执行计划,输入类型DOUBLE,union类型NUMBER,REAL
    4.查看执行计划,输入类型clob,union类型text
    5.查看执行计划,输入类型date,union类型timestamp
    6.查看执行计划,输入类型BLOB,union类型raw
    7.查看执行计划,输入类型inet,union类型cidr
    8.查看执行计划,输入类型bit,union类型bit(3)
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.成功
    7.成功
    8.成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Sql(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')

    def test_01(self):
        text = f'-----step1：查看执行计划,输入类型int,union类型float8 expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123::int2 " \
            f"union SELECT 456::float8;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: ((123::smallint)::double precision)",
                   "         Output: ((123::smallint)::double precision)",
                   "                     Output: 123::smallint",
                   "                           Output: 123::smallint",
                   "                     Output: 456::double precision"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

        text = f'-----step2：查看执行计划,输入类型float8,union类型int,NUMBER ' \
            f'expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123.456::float8 " \
            f"union SELECT 456.123::int union SELECT 789.123::NUMBER;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: (123.456::double precision)",
                   "               Output: 123.456::double precision",
                   "               Output: 456",
                   "                     Output: 456",
                   "               Output: 789.123",
                   "                     Output: 789.123"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

        text = f'-----step3：查看执行计划,输入类型DOUBLE,union类型NUMBER,REAL ' \
            f'expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123.456::DOUBLE PRECISION " \
            f"union SELECT 456.123::NUMBER union SELECT 789.123::REAL;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: (123.456::double precision)",
                   "               Output: 123.456::double precision",
                   "               Output: 456.123",
                   "                     Output: 456.123",
                   "               Output: 789.12299::real",
                   "                     Output: 789.12299::real"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

        text = f'-----step4：查看执行计划,输入类型clob,union类型text expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123::clob " \
            f"union SELECT 456::text;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: ('123'::clob)",
                   "         Output: ('123'::clob)",
                   "                     Output: '123'::clob",
                   "                     Output: ('456'::text)::clob",
                   "                           Output: '456'::text"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

        text = f'-----step5：查看执行计划,输入类型date,union类型timestamp expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT '2020-09-28'::date " \
            f"union SELECT '2020-09-30'::timestamp;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: ('2020-09-28 00:00:00'::"
                   "timestamp(0) without time zone)",
                   "         Output: ('2020-09-28 00:00:00'::"
                   "timestamp(0) without time zone)",
                   "                     Output: '2020-09-28 00:00:00'::"
                   "timestamp(0) without time zone",
                   "                     Output: '2020-09-30 00:00:00'::"
                   "timestamp without time zone"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

        text = f'-----step6：查看执行计划,输入类型BLOB,union类型raw expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT HEXTORAW('DEADBEEF')::BLOB " \
            f"union SELECT HEXTORAW('DEABEEF')::raw;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: ('DEADBEEF'::blob)",
                   "         Output: ('DEADBEEF'::blob)",
                   "                     Output: 'DEADBEEF'::blob",
                   "                     Output: '0DEABEEF'::raw",
                   "                           Output: '0DEABEEF'::raw"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

        text = f'-----step7：查看执行计划,输入类型inet,union类型cidr expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT inet '0.0.0.0/24'::inet " \
            f"union SELECT inet '0.0.0.0/24'::cidr;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: ('0.0.0.0/24'::inet)",
                   "         Output: ('0.0.0.0/24'::inet)",
                   "                     Output: '0.0.0.0/24'::inet",
                   "                     Output: '0.0.0.0/24'::cidr",
                   "                           Output: '0.0.0.0/24'::cidr"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

        text = f'-----step8：查看执行计划,输入类型bit,union类型bit(3) expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT B'1'::bit varying " \
            f"union SELECT B'101'::bit(3);"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        outputs = ["   Output: (B'1'::bit varying)",
                   "         Output: (B'1'::bit varying)",
                   "                     Output: B'1'::bit varying",
                   "                     Output: B'101'::bit(3)",
                   "                           Output: B'101'::bit(3)"]
        for output in outputs:
            self.assertIn(output, sql_res, '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----无需清理环境-----')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
