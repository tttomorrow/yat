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
Case Name： pg_current_sessionid当前执行环境下的会话ID
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.执行pg_current_sessionid;返回当前执行环境下的会话ID时间戳.会话ID
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
constant = Constant()

class Pg_current_sessionid(unittest.TestCase):


    def setUp(self):
        logger.info("------------------------Opengauss_BaseFunc_pg_current_sessionid_001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        db_status = commonsh.get_db_cluster_status()
        logger.info(db_status)
        if not db_status:
            commonsh.start_db_cluster()
            if not db_status:
                raise Exception("db status is not true, please check!")
        logger.info(db_status)

    def test_pg_current_sessionid(self):

        SqlMdg = commonsh.execut_db_sql('SELECT pg_current_sessionid();').splitlines()[-2].strip().split('.')
        SqlMdg_sessid = commonsh.execut_db_sql('select pg_current_sessid();').splitlines()
        logger.info(SqlMdg)
        logger.info(SqlMdg_sessid)
        try:
            int_SqlMdg = int(SqlMdg[-2])
            len_SqlMdg = len(SqlMdg[-2])
            self.assertEqual(len_SqlMdg,10)
            logger.info(f'{int_SqlMdg},{len_SqlMdg}')
        except Exception as e:
            logger.error(f'{len_SqlMdg} != 10')
            raise
        try:
            self.assertEqual(SqlMdg_sessid[-2].strip(),SqlMdg[-1])
            logger.info(f'{SqlMdg_sessid[-2].strip()} == {SqlMdg[-1]}')
        except Exception as e:
            logger.info(f'{SqlMdg_sessid[-2].strip()} != {SqlMdg[-1]}')
            raise



    def tearDown(self):
        logger.info('------------------------Opengauss_BaseFunc_pg_current_sessionid_001执行结束--------------------------')