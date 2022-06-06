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
#--  @testpoint:opengauss关键字from(保留)，作为目录对象名（默认只允许初始化用户创建）
'''
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Hostname(unittest.TestCase):
    def setUp(self):
         logger.info("------------------------ Opengauss_Function_KeyWord_From_Case0020 开始执行--------------------------")
        		
    def test_from_1(self):
        logger.info("------------------------关键字作为目录对象名不带引号-合理报错--------------------------")
        SqlMdg = commonsh.execut_db_sql('''create directory from as '/tmp/';
                                                drop directory from;''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)

        logger.info("------------------------关键字作为目录对象名带双引号-成功--------------------------")
        SqlMdg = commonsh.execut_db_sql('create directory \\\"from\\\" as \'/tmp/\';'
                                      'drop directory \\\"from\\\"; ')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DIRECTORY_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.DROP_DIRECTORY_SUCCESS_MSG, SqlMdg)
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DIRECTORY_SUCCESS_MSG, SqlMdg)
        self.assertIn(constant.DROP_DIRECTORY_SUCCESS_MSG, SqlMdg)

        logger.info("------------------------关键字作为目录对象名带单引号 - 合理报错--------------------------")
        SqlMdg = commonsh.execut_db_sql('''drop directory if exists 'from';''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        SqlMdg = commonsh.execut_db_sql(''' create directory 'from' as '/tmp/';''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)

        logger.info("------------------------关键字作为目录对象名带反引号 - 合理报错--------------------------")
        SqlMdg = commonsh.execut_db_sql('''drop directory if exists \`from\`;''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
        SqlMdg = commonsh.execut_db_sql('''create directory \`from\` as '/tmp/';''')
        logger.info(SqlMdg)
        self.assertIn(constant.SYNTAX_ERROR_MSG, SqlMdg)
		
        def tearDown(self):
         logger.info('------------------------ Opengauss_Function_KeyWord_From_Case0020 执行结束--------------------------')
