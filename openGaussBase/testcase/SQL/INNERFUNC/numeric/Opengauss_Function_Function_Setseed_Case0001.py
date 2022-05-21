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

Case Type： 功能测试
Case Name： setseed函数与random正常连用
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.执行setseed函数取整并断言校验
步骤 3.清理环境并删除测试表
'''
import os
import unittest
from yat.test import Node
import time
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH


logger = Logger()
common = Common()
commonsh = CommonSH('dbuser')

class Setseed_001(unittest.TestCase):


    def setUp(self):
        logger.info("------------------------Opengauss_BaseFunc_setseed_001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        db_status = commonsh.get_db_cluster_status()
        logger.info(db_status)
        if not db_status:
            commonsh.start_db_cluster()
            if not db_status:
                raise Exception("db status is not true, please check!")
        logger.info(db_status)

    def test_setseed_001(self):

        SqlMdg1 = commonsh.execut_db_sql('SELECT setseed(0.5);SELECT random();')
        SqlMdg2 = commonsh.execut_db_sql('SELECT setseed(0.5);SELECT random();')
        try:
            self.assertEqual(SqlMdg1,SqlMdg2)
            logger.error(f'{SqlMdg1} == {SqlMdg2}')
        except Exception as e:
            logger.error(f'{SqlMdg1} != {SqlMdg2}')
            raise

    def tearDown(self):
        logger.info("------------------------drop table------------------")
        logger.info('------------------------Opengauss_BaseFunc_setseed_001执行结束--------------------------')