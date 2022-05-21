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
Case Name   : 所有输入都是相同的类型，并且不是unknown类型，解析成这种类型
Description :
    1.查看执行计划,所有输入都是相同的类型int进行union
    2.查看执行计划,所有输入都是相同的类型float8进行union
    3.查看执行计划,所有输入都是相同的类型REAL进行union
    4.查看执行计划,所有输入都是相同的类型text进行union
    5.查看执行计划,所有输入都是相同的类型clob进行union
    6.查看执行计划,所有输入都是相同的类型name进行union
    7.查看执行计划,所有输入都是相同的类型date进行union
    8.查看执行计划,所有输入都是相同的类型raw进行union
    9.查看执行计划,所有输入都是相同的类型tsquery进行union
    10.查看执行计划,所有输入都是相同的类型inet进行union
    11.查看执行计划,所有输入都是相同的类型bit进行union
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.成功
    7.成功
    8.成功
    9.成功
    10.成功
    11.成功
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
        text = f'-----step1：查看执行计划,所有输入都是相同的类型int进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123::int " \
            f"union SELECT 456::int;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertEqual(2, sql_res.count('Output: (123)'), '执行失败:' + text)
        self.assertIn('Output: 123' and 'Output: 456', sql_res,
                      '执行失败:' + text)

        text = f'-----step2：查看执行计划,所有输入都是相同的类型float8进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123.456::float8 " \
            f"union SELECT 456.123::float8 union SELECT 789.123::float8;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('Output: (123.456::double precision)' and
                      'Output: 123.456::double precision' and
                      'Output: 789.123::double precision' and
                      'Output: 456.123::double precision', sql_res,
                      '执行失败:' + text)

        text = f'-----step3：查看执行计划,所有输入都是相同的类型REAL进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123.456::REAL " \
            f"union SELECT 456.123::REAL union SELECT 789.123::REAL;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('Output: (123.456::real)' and
                      'Output: 123.456::real' and
                      'Output: 789.12299::real' and
                      'Output: 456.12299::real', sql_res,
                      '执行失败:' + text)

        text = f'-----step4：查看执行计划,所有输入都是相同的类型text进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123::text " \
            f"union SELECT 456::text;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertEqual(2, sql_res.count("Output: ('123'::text)"),
                         '执行失败:' + text)
        self.assertIn("Output: '123'::text" and
                      "Output: '456'::text", sql_res, '执行失败:' + text)

        text = f'-----step5：查看执行计划,所有输入都是相同的类型clob进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123::clob " \
            f"union SELECT 456::clob;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertEqual(2, sql_res.count("Output: ('123'::clob)"),
                         '执行失败:' + text)
        self.assertIn("Output: '123'::clob" and
                      "Output: '456'::clob", sql_res, '执行失败:' + text)

        text = f'-----step6：查看执行计划,所有输入都是相同的类型name进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 'test29'::name " \
            f"union SELECT 'test29'::name;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        output1 = sql_res.count("Output: ('test29'::name)")
        output2 = sql_res.count("Output: 'test29'::name")
        self.assertEqual(2, output1 and output2, '执行失败:' + text)

        text = f'-----step7：查看执行计划,所有输入都是相同的类型date进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT '2020-09-28'::date " \
            f"union SELECT '2020-09-30'::date;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        output1 = sql_res.count(
            "Output: ('2020-09-28 00:00:00'::timestamp(0) without time zone)")
        output2 = "Output: '2020-09-28 00:00:00'::timestamp(0) " \
                  "without time zone"
        output3 = "Output: '2020-09-30 00:00:00'::timestamp(0) " \
                  "without time zone"
        self.assertEqual(2, output1, '执行失败:' + text)
        self.assertIn(output2 and output3, sql_res, '执行失败:' + text)

        text = f'-----step8：查看执行计划,所有输入都是相同的类型raw进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT HEXTORAW('DEADBEEF')::raw " \
            f"union SELECT HEXTORAW('DEABEEF')::raw;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        output1 = sql_res.count("Output: ('DEADBEEF'::raw)")
        self.assertEqual(2, output1, '执行失败:' + text)
        self.assertIn("Output: 'DEADBEEF'::raw" and
                      "Output: '0DEABEEF'::raw", sql_res, '执行失败:' + text)

        text = f'-----step9：查看执行计划,所有输入都是相同的类型tsquery进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 'fat & rat'::tsquery " \
            f"union SELECT 'sate & rat'::tsquery;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        output1 = sql_res.count("Output: ('''fat'' & ''rat'''::tsquery)")
        output2 = " Output: '''fat'' & ''rat'''::tsquery"
        output3 = "Output: '''sate'' & ''rat'''::tsquery"
        self.assertEqual(2, output1, '执行失败:' + text)
        self.assertIn(output2 and output3, sql_res, '执行失败:' + text)

        text = f'-----step10：查看执行计划,所有输入都是相同的类型inet进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT inet '0.0.0.0/24'::inet " \
            f"union SELECT inet '0.0.0.0/24'::inet;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        output1 = sql_res.count("Output: ('0.0.0.0/24'::inet)")
        output2 = sql_res.count("Output: '0.0.0.0/24'::inet")
        self.assertEqual(2, output1 and output2, '执行失败:' + text)

        text = f'-----step11：查看执行计划,所有输入都是相同的类型bit进行union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT B'1'::bit " \
            f"union SELECT B'101'::bit(3);"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        output1 = sql_res.count("Output: (B'1'::bit(1))")
        self.assertEqual(2, output1, '执行失败:' + text)
        self.assertIn("Output: B'1'::bit(1)" and "Output: B'101'::bit(3)",
                      sql_res, '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----无需清理环境-----')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
