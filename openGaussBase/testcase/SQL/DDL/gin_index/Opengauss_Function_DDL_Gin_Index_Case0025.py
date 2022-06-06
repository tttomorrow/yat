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
Case Type   : 基础功能
Case Name   : 设置gin_fuzzy_search_limit为异常值
Description :
    1.设置gin_fuzzy_search_limit=-1
    2.设置gin_fuzzy_search_limit=2147483648
Expect      :
    1.设置失败
    2.设置失败
History     :
"""

import unittest
import os
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
logger = Logger()
common = Common()


class set_search_limit(unittest.TestCase):
    dbPrimaryUserNode = Node(node='PrimaryDbUser')
    dbPrimaryRootNode = Node(node='PrimaryRoot')
    commsh = CommonSH('PrimaryDbUser')

    def setUp(self):
        logger.info("-----------this is setup-----------")
        logger.info(f"-{os.path.basename(__file__)[:-3]}  start---")
        self.constant = Constant()

    def test_set_search_limit(self):
        text = "--step1:设置gin_fuzzy_search_limit=-1 expect:设置失败--"
        logger.info(text)
        result = self.commsh.execute_gsguc('set', '',
                                           'gin_fuzzy_search_limit=-1',
                                           get_detail=True)
        logger.info(result)
        self.assertIn(self.constant.SQL_WRONG_MSG[1], result, "执行失败"+text)
        self.assertIn(self.constant.FUZZY_SEARCH_LIMIT_MSG,
                      result, "执行失败"+text)
        text = "--step2:设置gin_fuzzy_search_limit=2147483648 expect:设置失败--"
        logger.info(text)
        result = self.commsh.execute_gsguc(
            'set', '', 'gin_fuzzy_search_limit=2147483648', get_detail=True)
        logger.info(result)
        self.assertIn(self.constant.SQL_WRONG_MSG[1], result, "执行失败" + text)
        self.assertIn(self.constant.FUZZY_SEARCH_LIMIT_MSG,
                      result, "执行失败" + text)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        logger.info(f"-{os.path.basename(__file__)[:-3]}  end---")
        