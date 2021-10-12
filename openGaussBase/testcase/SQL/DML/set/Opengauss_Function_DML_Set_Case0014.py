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
'''
--  @date:2020/11/3
--  @testpoint:事务外，先使用set命令，再使用set local命令
'''
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0014开始执行-----------------------------')

    def test_set(self):
        # set命令设置时区为UTC;查看时区，设置生效;查看时间，显示UTC时区时间
        sql_cmd1 = commonsh.execut_db_sql('''set time zone UTC;
                                      show time zone;
                                      select now();''')
        logger.info(sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('UTC', sql_cmd1)
        self.assertIn('+00', sql_cmd1)
        # 使用set local命令设置时区为PRC;
        # 查看时间，依然显示UTC时区时间,事务外，先使用set命令，再使用set local命令，set命令生效
        sql_cmd2 = commonsh.execut_db_sql('''set local time zone PRC;
                                      select now();''')
        logger.info(sql_cmd2)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('+08', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''reset time zone;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0014执行结束--------------------------')
