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
"""
Case Type   : 全文检索
Case Name   : 通过系统表PG_TS_PARSER或元命令，查看文本解析器
Description :
    1.通过系统表PG_TS_PARSER查看解析器名
    2.通过元命令查询
Expect      :
    1.显示四种解析器
    2.结果和系统表一致
History     :
"""
import sys
import unittest
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class FullTextSearch(unittest.TestCase):
    def setUp(self):
        logger.info('----------------this is setup-----------------------')
        logger.info('--------------Opengauss_Function_Dictionary_Case0056开始执行--------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Schema': ['Schema', 'pg_catalog', 'pg_catalog', 'pg_catalog', 'pg_catalog', 'pg_catalog', 'pg_catalog',
                       'pg_catalog', 'pg_catalog'],
            'Name': ['Name', 'default', 'ngram', 'pound', 'zhparser', 'default', 'ngram', 'pound', 'zhparser']}

    def test_text_match(self):
        msg = self.comsh.execut_db_sql('''select  prsname from PG_TS_PARSER;
                                     \dFp''')
        logger.info(msg)
        result_dict = self.com.format_sql_result(msg)
        logger.info(result_dict)
        del result_dict['Description']
        self.assertDictEqual(self.expect_result_dict, result_dict)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        # 无需清理环境
        logger.info('-----------------------Opengauss_Function_Dictionary_Case0056执行完成-----------------')
