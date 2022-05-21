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
Case Type   : 功能测试
Case Name   : 比较操作符对二进制类型进行比较
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.对二进制bytea类型进行比较
    步骤 3.对不同类型二进制进行比较
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：返回正确布尔类型
    步骤 3：不支持，合理报错
History     : 
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Compare_function(unittest.TestCase):

    def setUp(self):
        logger.info("--------Opengauss_Function_Innerfunc_Compare_Case0001开始执行------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):

        opera_list = ['>', '<', '=', '<=', '>=', '!=', '<>']

        logger.info("-------------bytea------------")
        result_list = ['f', 't', 'f', 't', 'f', 't', 't']
        for oper in opera_list:
            sql_cmd = r"""SELECT E'\\\\xACDEADBEEF'::BYTEA """ + f"""{oper}""" + r""" E'\\\\xDEADBEEF'::BYTEA;"""
            msg = self.commonsh.execut_db_sql(sql_cmd)
            logger.info(msg)
            self.assertTrue(result_list[opera_list.index(oper)] == msg.splitlines()[2].strip())

        logger.info("-----------bytea & raw-----------")
        for oper in opera_list:
            sql_cmd = r"""SELECT E'\\\\xACDEADBEEF'::BYTEA """ + f"""{oper}""" + r""" 'ACDEADBEEF'::RAW"""
            msg1 = self.commonsh.execut_db_sql(sql_cmd)
            logger.info(msg1)
            self.assertTrue('ERROR:  operator does not exist' in msg1)

    def tearDown(self):
        logger.info('----------Opengauss_Function_Innerfunc_Compare_Case0001执行结束---------')
