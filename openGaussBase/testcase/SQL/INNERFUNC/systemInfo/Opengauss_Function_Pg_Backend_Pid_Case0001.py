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

Case Type： 功能测试
Case Name： pg_backend_pid()当前会话连接的服务进程的进程ID
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.执行SELECT pg_backend_pid();返回当前执行环境下当前会话连接的服务进程的进程ID为一个随机数
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

class Pg_backend_pid(unittest.TestCase):


    def setUp(self):
        logger.info("------------------------Opengauss_BaseFunc_pg_backend_pid_001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        db_status = commonsh.get_db_cluster_status()
        logger.info(db_status)
        if not db_status:
            commonsh.start_db_cluster()
            if not db_status:
                raise Exception("db status is not true, please check!")
        logger.info(db_status)

    def test_pg_backend_pid(self):

        SqlMdg = commonsh.execut_db_sql('SELECT pg_backend_pid();').splitlines()
        logger.info(SqlMdg)
        try:
            int_SqlMdg = int(SqlMdg[-2])
            len_SqlMdg = len(SqlMdg[-2])
            self.assertEqual(len_SqlMdg,16)
            logger.info(f'{int_SqlMdg},{len_SqlMdg}')
        except Exception as e:
            logger.error(f'{len_SqlMdg} != 16')
            raise

    def tearDown(self):
        logger.info('------------------------Opengauss_BaseFunc_pg_backend_pid_001执行结束--------------------------')