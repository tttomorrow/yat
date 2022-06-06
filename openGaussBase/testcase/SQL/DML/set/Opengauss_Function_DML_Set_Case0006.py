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
--  @testpoint:事务中，添加参数session设置时区后再提交事务，最后再重置参数值
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0006开始执行-----------------------------')

    def test_set(self):
        # 开启事务
        # 设置时区是UTC
        # 查看设置是否生效
        # 查看当前北京时间的UTC时区时间
        # 提交事务
        # 回滚
        # 查询当前时间
        sql_cmd1 = commonsh.execut_db_sql('''start transaction;
                                     set session time zone UTC;
                                     show time zone;
                                     select now();
                                     commit;
                                     rollback;
                                     select now();
                                     ''')
        logger.info(sql_cmd1)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('UTC', sql_cmd1)
        self.assertIn('+00', sql_cmd1)
        self.assertIn(constant.COMMIT_SUCCESS_MSG, sql_cmd1)
        self.assertIn('NOTICE:  there is no transaction in progress', sql_cmd1)
        self.assertIn('+00', sql_cmd1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 重置时区为PRC
        sql_cmd2 = commonsh.execut_db_sql('''set session time zone PRC;''')
        logger.info(sql_cmd2)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0006执行结束--------------------------')
