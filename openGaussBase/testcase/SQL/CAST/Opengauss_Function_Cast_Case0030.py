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
Case Name   : 隐式转换关系,结合union,不是同一类型合理报错
Description :
    1.查看执行计划,输入类型是同一个int类型范畴,则选择该类型范畴的首选类型 union
    2.查看执行计划,输入类型不是同一个类型范畴
    3.查看执行计划,输入类型是同一个HEXTORAW类型范畴,则选择该类型范畴的首选类型 union
Expect      :
    1.成功
    2.合理报错
    3.成功
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
        text = f'-----step1：查看执行计划,输入类型是同一个int类型范畴,' \
            f'则选择该类型范畴的首选类型 union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT 123::int " \
            f"union SELECT 456::int;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertEqual(2, sql_res.count('Output: (123)'), '执行失败:' + text)
        self.assertIn('Output: 123' and 'Output: 456', sql_res,
                      '执行失败:' + text)

        text = f'-----step2：查看执行计划,输入类型不是同一个类型范畴 expect:合理报错-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT '2020-09-30'::varchar " \
            f"union SELECT '2020-09-29'::date;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        expect_msg = 'ERROR:  UNION types character varying and timestamp ' \
                     'without time zone cannot be matched'
        self.assertIn(expect_msg, sql_res, '执行失败:' + text)

        text = f'-----step3：查看执行计划,输入类型是同一个HEXTORAW类型范畴,' \
            f'则选择该类型范畴的首选类型 union expect:成功-----'
        self.log.info(text)
        sql_cmd = f"explain performance SELECT HEXTORAW('DEADBEEF')::blob " \
            f"union SELECT HEXTORAW('DEABEEF')::raw;"
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        output1 = sql_res.count("Output: ('DEADBEEF'::blob)")
        output2 = sql_res.count("Output: '0DEABEEF'::raw")
        self.assertEqual(2, output1 and output2, '执行失败:' + text)
        self.assertIn("Output: 'DEADBEEF'::blob", sql_res, '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----无需清理环境-----')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
