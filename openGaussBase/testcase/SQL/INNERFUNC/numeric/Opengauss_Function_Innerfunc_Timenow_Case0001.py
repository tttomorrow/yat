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
Case Type   : 时间/日期函数
Case Name   : 函数timenow(),查看当前日期及时间
Description :
    1.查看当前日期及时间
    2.使用函数timenow查看当前时间
Expect      :
    1.查看当前日期及时间成功
    2.使用函数timenow查看当前时间成功
History     :
"""
import datetime
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Functions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Timenow_Case0001开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        self.log.info(f'---步骤1.查看当前日期及时间---')
        now = datetime.datetime.now()
        self.log.info(now)
        self.log.info(f'---步骤2.使用函数timenow查看当前时间---')
        sql_cmd = self.commonsh.execut_db_sql(f'select timenow();')
        self.log.info(sql_cmd)
        str_time = sql_cmd.splitlines()[-2].strip()[:-3:]
        self.log.info(str_time)
        test1 = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        self.log.info(test1)
        result = (test1 - now).seconds
        self.log.info(result)
        self.assertTrue(result >= 0)

    def tearDown(self):
        self.log.info('-------无需清理环境-------')
        self.log.info('-Opengauss_Function_Innerfunc_Timenow_Case0001结束-')
