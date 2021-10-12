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
Case Type   : GUC
Case Name   : 使用set方法设置DateStyle的输出格式
Description :
    1.查询参数默认值
    2.设置参数值为Postgres并查看当前日期
    3.设置参数值为SQL并查看当前日期
    4.设置参数值为German并查看当前日期
    5.恢复参数默认值
Expect      :
    1.显示默认值ISO, MDY
    2.设置成功当前日期显示格式为月日年，时间显示格式如Sat Dec 19 09:17:31 2020
    3.设置成功当前日期显示格式为月日年，时间显示格式如12/19/2020 09:54:23.367 CST
    4.设置成功当前日期显示格式为日月年，时间显示格式如19.12.2020 09:54:49.099673 CST
    5.恢复成功
History     :
"""
import sys
import unittest
import time
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class ClientConnection(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_Guc_ClientConnection_Case0129开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_datestyle(self):

        # 查询默认值
        sql_cmd1 = commonsh.execut_db_sql('''show DateStyle;''')
        logger.info(sql_cmd1)
        self.res = sql_cmd1.splitlines()[-2].strip()
        # 设置日期格式为Postgres并查询
        sql_cmd2 = commonsh.execut_db_sql('''set DateStyle to 'Postgres'; 
                                           show DateStyle;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('Postgres, MDY', sql_cmd2)
        # 设置日期格式为Postgres并查询
        sql_cmd3 = commonsh.execut_db_sql('''set DateStyle to 'SQL'; 
                                            show DateStyle;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd3)
        self.assertIn('SQL, MDY', sql_cmd3)
        # 设置日期格式为German并查询
        sql_cmd4 = commonsh.execut_db_sql('''set DateStyle to 'German'; 
                                           show DateStyle;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd4)
        self.assertIn('German, DMY', sql_cmd4)


    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd5 = commonsh.execut_db_sql('''show DateStyle;''')
        logger.info(sql_cmd5)
        if self.res not in sql_cmd5:
            msg = commonsh.execut_db_sql('''set DateStyle to 'ISO, MDY';''')
            self.log.info(msg)
        logger.info('------------------------Opengauss_Function_Guc_ClientConnection_Case0129执行结束--------------------------')
