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

Case Type： 数据库系统
Case Name： 设置gin_fuzzy_search_limit为异常值
Case No:    Opengauss_Gin_Index_0024
Descption:  1.设置gin_fuzzy_search_limit=2 2.重启数据库3.执行Opengauss_Gin_Index_0024.sql脚本

history：
'''
import os
import unittest
from yat.test import Node
import time
import _thread
import queue
from yat.test import macro
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
logger = Logger()
common = Common()
TPCC_RES = queue.Queue()


class set_search_limit(unittest.TestCase):

    dbPrimaryUserNode = Node(node='PrimaryDbUser')
    dbPrimaryRootNode = Node(node='PrimaryRoot')
    FUZZY_SEARCH_LIMIT_MSG = Constant.FUZZY_SEARCH_LIMIT_MSG
    commsh = CommonSH('PrimaryDbUser')

    def setUp(self):
        logger.info("-----------this is setup-----------")
        logger.info("-----------Opengauss_Gin_Index_0024 start-----------")

    def test_set_search_limit(self):
        logger.info("-----------gin_fuzzy_search_limit=-1-----------")
        self.commsh.execute_gsguc('set', self.FUZZY_SEARCH_LIMIT_MSG, 'gin_fuzzy_search_limit=-1')
        
        

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        