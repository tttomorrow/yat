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
--  @testpoint:set命令设置日期时间风格
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0129开始执行-----------------------------')

    def test_reset(self):
        # 将搜索路径设置为myschema、public，首先搜索myschema
        sql_cmd1 = commonsh.execut_db_sql('''show datestyle;
                                       SET datestyle TO postgres,dmy;
                                       select now();
                                       reset datestyle;''')
        logger.info(sql_cmd1)
        self.assertIn('ISO, MDY', sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.RESET_SUCCESS_MSG, sql_cmd1)
        # 恢复搜索路径默认值
        sql_cmd2 = commonsh.execut_db_sql('''SET datestyle TO postgres;
                                      show datestyle;
                                      select now();
                                      reset datestyle;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('Postgres, MDY', sql_cmd2)
        self.assertIn(constant.RESET_SUCCESS_MSG, sql_cmd2)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0129执行结束--------------------------')
