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
Case Type   :  keyword-nvarchar
Case Name   :  opengauss关键字nvarchar(非保留)，作为目录对象名
Description :
    1.关键字作为目录对象名不带双引号 - 成功
    2.关键字作为目录对象名带双引号 - 成功
    3.关键字作为目录对象名带单引号 - 合理报错
    4.关键字作为目录对象名带反引号 - 合理报错
Expect      :
    1.成功
    2.成功
    3.合理报错
    4.合理报错
History     :
"""

import unittest


from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class KeywordNvarchar(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()
        self.logger.info("Opengauss_Function_Keyword_Nvarchar_Case0020 开始执行")
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()


    def test_nvarchar(self):
        text = "--step1:关键字作为目录对象名不带双引号;expect:成功"
        self.logger.info(text)
        result = self.commonsh.execut_db_sql("create directory nvarchar "
            "as '/tmp/';drop directory nvarchar;")
        self.logger.info(result)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG, result,
                      "执行失败:" + text)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG, result,
                      "执行失败:" + text)

        text = "--step2:关键字作为目录对象名带双引号;expect:成功"
        self.logger.info(text)
        result = self.commonsh.execut_db_sql('''create directory "nvarchar" \
            as '/tmp/';drop directory "nvarchar";''')
        self.logger.info(result)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG, result,
                      "执行失败:" + text)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG, result,
                      "执行失败:" + text)

        text = "--step3:关键字作为目录对象名带单引号;expect:合理报错"
        self.logger.info(text)
        result = self.commonsh.execut_db_sql("drop directory "
                                             "if exists 'nvarchar';")
        self.logger.info(result)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, result, "执行失败:" + text)

        result = self.commonsh.execut_db_sql("create directory "
                                             "'nvarchar' as '/tmp/';")
        self.logger.info(result)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, result, "执行失败:" + text)

        text = "--step4:关键字作为目录对象名带反引号;expect:合理报错"
        self.logger.info(text)
        result = self.commonsh.execut_db_sql("drop directory "
                                             "if exists \`nvarchar\`;")
        self.logger.info(result)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, result, "执行失败:" + text)

        result = self.commonsh.execut_db_sql("create directory "
                                             "\`nvarchar\` as '/tmp/';")
        self.logger.info(result)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, result, "执行失败:" + text)

    def tearDown(self):
        self.logger.info("Opengauss_Function_Keyword_Nvarchar_Case0020 执行结束")