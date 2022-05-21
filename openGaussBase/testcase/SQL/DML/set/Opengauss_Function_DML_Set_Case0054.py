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
'''
--  @testpoint:参数checkpoint_segments测试，无效值，合理报错
'''
import sys
import unittest
import time
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0054开始执行-----------------------------')

    def test_checkpoint(self):
        # 查看默认值为64；设置参数checkpoint_segments为65
        # 设置参数值为0以及63.5，合理报错
        sql_cmd1 = commonsh.execut_db_sql('''show checkpoint_segments;
        ALTER SYSTEM SET checkpoint_segments to 65;
        ALTER SYSTEM SET checkpoint_segments to 0;
        ALTER SYSTEM SET checkpoint_segments to 63.5;
        ''')
        logger.info(sql_cmd1)
        self.assertIn('64', sql_cmd1)
        self.assertIn(constant.ALTER_SYSTEM_SUCCESS_MSG, sql_cmd1)
        self.assertIn('ERROR:  0 is outside the valid range for parameter "checkpoint_segments" (1 .. 2147483646)', sql_cmd1)
        self.assertIn('ERROR:  invalid value for parameter "checkpoint_segments": "63.5"', sql_cmd1)
        time.sleep(3)
        # 查看参数值
        sql_cmd2 = commonsh.execut_db_sql('''show checkpoint_segments;''')
        logger.info(sql_cmd2)
        self.assertIn('65', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 恢复默认值
        sql_cmd2 = commonsh.execut_db_sql('''ALTER SYSTEM SET checkpoint_segments to 64;''')
        logger.info(sql_cmd2)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0054执行结束--------------------------')
