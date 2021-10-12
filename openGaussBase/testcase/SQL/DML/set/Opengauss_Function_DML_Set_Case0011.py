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
--  @testpoint:设置时区，先使用local参数，rollback之后再使用session参数
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0011开始执行-----------------------------')

    def test_set(self):
        # 开启事务
        # 设置时区为UTC
        # 查看设置是否生效
        # 查询时间
        # 回滚
        # 查询时间
        sql_cmd1 = commonsh.execut_db_sql('''start transaction;
                                      set local time zone UTC;
                                      show time zone;
                                      select now();
                                      rollback;
                                      select now();''')
        logger.info(sql_cmd1)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('UTC', sql_cmd1)
        self.assertIn('+00', sql_cmd1)
        self.assertIn(constant.ROLLBACK_MSG, sql_cmd1)
        self.assertIn('+08', sql_cmd1)
        # 使用session参数，设置会话级别的timezone
        # 查看时区，设置生效,通过pg_settings系统表，查看参数运行的具体信息，当前参数名是UTC
        sql_cmd2 = commonsh.execut_db_sql('''set session time zone UTC;
                                       show time zone;
                                       select now();
                                       select name ,setting from pg_settings where name='TimeZone';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('UTC', sql_cmd2)
        self.assertIn('+00', sql_cmd2)
        # 恢复时区PRC,通过pg_settings系统表，查看参数运行的具体信息，当前参数名是PRC
        sql_cmd3 = commonsh.execut_db_sql('''reset time zone;
        select name ,setting from pg_settings where name='TimeZone';
        select now();''')
        logger.info(sql_cmd3)
        self.assertIn(constant.RESET_SUCCESS_MSG, sql_cmd3)
        self.assertIn('+08', sql_cmd3)
    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0011执行结束--------------------------')
