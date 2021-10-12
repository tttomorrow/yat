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
--  @testpoint:事务中，先使用set命令，再使用SET LOCAL命令
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0012开始执行-----------------------------')

    def test_set(self):
        # 开启事务
        # 设置时区为UTC
        # 查看设置是否生效
        # 查看设置是否生效
        # 查询时间
        # 使用set local命令设置时区为PRC；查看时间和时区
        # 提交事务;查看时区，时区显示UTC;查看时间

        sql_cmd1 = commonsh.execut_db_sql('''start transaction;
                                     set local time zone UTC;
                                     show time zone;
                                     select now();
                                     set local time zone PRC;
                                     select now();
                                     show time zone;
                                     commit;
                                     show time zone;
                                     select now();''')
        logger.info(sql_cmd1)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('UTC', sql_cmd1)
        self.assertIn('+00', sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('+08', sql_cmd1)
        self.assertIn('PRC', sql_cmd1)
        self.assertIn(constant.COMMIT_SUCCESS_MSG, sql_cmd1)
        self.assertIn('UTC', sql_cmd1)
        self.assertIn('+00', sql_cmd1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 恢复时区为PRC
        sql_cmd2 = commonsh.execut_db_sql('''reset time zone;''')
        logger.info(sql_cmd2)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0012执行结束--------------------------')
