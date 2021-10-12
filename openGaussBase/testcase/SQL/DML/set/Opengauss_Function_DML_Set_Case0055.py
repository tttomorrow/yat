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
--  @date:2020/11/11
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0055开始执行-----------------------------')

    def test_checkpoint(self):
        # 查看默认值为15min；设置参数checkpoint_segments为30s
        sql_cmd1 = commonsh.execut_db_sql('''show checkpoint_timeout;
        ALTER SYSTEM SET checkpoint_timeout to 30;
        ''')
        logger.info(sql_cmd1)
        self.assertIn('15min', sql_cmd1)
        self.assertIn(constant.ALTER_SYSTEM_SUCCESS_MSG, sql_cmd1)
        time.sleep(3)
        # 查看参数值
        sql_cmd2 = commonsh.execut_db_sql('''show checkpoint_timeout;''')
        logger.info(sql_cmd2)
        self.assertIn('30s', sql_cmd2)
        # 设置参数checkpoint_segments为3600s
        sql_cmd3 = commonsh.execut_db_sql('''ALTER SYSTEM SET checkpoint_timeout to 3600;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.ALTER_SYSTEM_SUCCESS_MSG, sql_cmd3)
        time.sleep(3)
        # 查看参数值
        sql_cmd4 = commonsh.execut_db_sql('''show checkpoint_timeout;''')
        logger.info(sql_cmd4)
        self.assertIn('1h', sql_cmd4)
        # 参数值取无效值，合理报错
        sql_cmd5 = commonsh.execut_db_sql('''ALTER SYSTEM SET checkpoint_timeout to 29;
        ALTER SYSTEM SET checkpoint_timeout to 3601;
        ALTER SYSTEM SET checkpoint_timeout to -30;
        ALTER SYSTEM SET checkpoint_timeout to 30.5;''')
        logger.info(sql_cmd5)
        self.assertIn('ERROR:  invalid value for parameter "checkpoint_timeout"', sql_cmd5)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 恢复默认值
        sql_cmd6 = commonsh.execut_db_sql('''ALTER SYSTEM SET checkpoint_timeout to '15min';''')
        logger.info(sql_cmd6)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0055执行结束--------------------------')
