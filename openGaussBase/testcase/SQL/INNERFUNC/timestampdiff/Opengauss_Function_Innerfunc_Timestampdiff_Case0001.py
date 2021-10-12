"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : 功能测试
Case Name   : 使用timestampdiff函数计算两个日期时间之间的差值
Description : TIMESTAMPDIFF(unit , timestamp_expr1, timestamp_expr2)
    timestampdiff函数是计算两个日期时间之间(timestamp_expr2-timestamp_expr1)的差值，并以unit形式返回结果。
    timestamp_expr1，timestamp_expr2必须是一个timestamp、timestamptz、date类型的值表达式。unit表示的是两个日期差的单位。
    该函数仅在openGauss兼容MY类型时（即dbcompatibility = 'B'）有效，其他类型不支持该函数。
    1.创建兼容MY的数据库
    2.在该数据库中执行timestampdiff函数
Expect      : 
    1.创建成功
    2.函数返回结果正确
History     : 
"""

import unittest
import sys
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info("--------Opengauss_Function_Innerfunc_Timestampdiff_Case0001.py开始执行--------")
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_timestampdiff(self):
        sql_cmd = ["select timestampdiff(year, '2018-01-01', '2020-01-01');",
                   "select timestampdiff(quarter, '2018-01-01', '2020-01-01');",
                   "select timestampdiff(month, '2018-01-01', '2020-01-01');",
                   "select timestampdiff(week, '2018-01-01', '2020-01-01');",
                   "select timestampdiff(day, '2018-01-01', '2020-01-01');",
                   "select timestampdiff(hour, '2020-01-01 10:10:10', '2020-01-01 11:11:11');",
                   "select timestampdiff(minute, '2020-01-01 10:10:10', '2020-01-01 11:11:11');",
                   "select timestampdiff(second, '2020-01-01 10:10:10', '2020-01-01 11:11:11');",
                   "select timestampdiff(microsecond, '2020-01-01 10:10:10.000000', '2020-01-01 10:10:10.111111');",
                   "select timestampdiff(hour,'2020-05-01 10:10:10-01','2020-05-01 10:10:10-03');"]
        result = ['2', '8', '24', '104', '730', '1', '61', '3661', '111111', '2']

        db_create = f"""drop database if exists test_diff;
                        create database test_diff dbcompatibility 'B';"""
        msg1 = self.commonsh.execut_db_sql(db_create)
        logger.info(msg1)
        self.assertTrue('CREATE' in msg1)

        for j in range(len(sql_cmd)):
            cmd1 = f'''source {self.DB_ENV_PATH};
                       gsql -d test_diff -p {self.userNode.db_port} -c "{sql_cmd[j]}"'''
            msg2 = self.userNode.sh(cmd1).result()
            logger.info(msg2)
            self.assertTrue(msg2.splitlines()[-2].strip() == result[j])

        db_drop = f'''drop database test_diff;'''
        msg3 = self.commonsh.execut_db_sql(db_drop)
        logger.info(msg3)
        self.assertTrue('DROP' in msg3)

    def tearDown(self):
        logger.info('--------Opengauss_Function_Innerfunc_Timestampdiff_Case0001.py执行结束--------')