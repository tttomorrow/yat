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
Case Name： pg_current_userid返回当前用户ID
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.执行SELECT pg_current_userid;返回当前用户ID与系统表内的userid对比
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

class Pg_current_userid(unittest.TestCase):


    def setUp(self):
        logger.info("------------------------Opengauss_BaseFunc_pg_current_userid_001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        db_status = commonsh.get_db_cluster_status()
        logger.info(db_status)
        if not db_status:
            commonsh.start_db_cluster()
            if not db_status:
                raise Exception("db status is not true, please check!")
        logger.info(db_status)       

    def test_pg_current_userid(self):
        SqlMdg = commonsh.execut_db_sql(f"select userid from GS_WLM_USER_INFO where username = '{commonsh.node.ssh_user}';").splitlines()[-2].strip()
        logger.info(SqlMdg)
        user_SqlMdg = commonsh.execut_db_sql('SELECT pg_current_userid();').splitlines()[-2].strip()
        logger.info(user_SqlMdg)
        try:
            self.assertEqual(SqlMdg,user_SqlMdg)
            logger.info(f'{user_SqlMdg} == {SqlMdg}')
        except Exception as e:
            logger.info(f'{user_SqlMdg} != {SqlMdg}')
            raise
    def tearDown(self):
        logger.info('------------------------Opengauss_BaseFunc_pg_current_userid_001执行结束--------------------------')