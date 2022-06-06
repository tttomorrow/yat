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
Case Type   : 功能测试
Case Name   : 使用pg_sleep函数进行服务器线程延迟
Description : pg_sleep(seconds)服务器线程延迟时间
    步骤 1.执行SELECT pg_sleep(10);语句，检查延迟时间是否正确
Expect      :
    步骤 1.函数执行结果正确
History     :
"""

import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info("----------Opengauss_Function_Innerfunc_Pg_Sleep_Case0001开始执行------------")
        self.commonsh = CommonSH('dbuser')

    def test_pg_sleep(self):

        cmd1 = f''' SELECT clock_timestamp();
                    SELECT pg_sleep(10);
                    SELECT clock_timestamp();'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        logger.info(msg1)

        before_time = msg1.splitlines()[2].strip()
        after_time = msg1.splitlines()[12].strip()

        cmd2 = f'''select timestamp '{after_time}' - timestamp '{before_time}';'''
        msg2 = self.commonsh.execut_db_sql(cmd2)
        logger.info(msg2)
        self.assertTrue('00:00:10' in msg2)

    def tearDown(self):
        logger.info('-----------Opengauss_Function_Innerfunc_Pg_Sleep_Case0001执行结束------------')
