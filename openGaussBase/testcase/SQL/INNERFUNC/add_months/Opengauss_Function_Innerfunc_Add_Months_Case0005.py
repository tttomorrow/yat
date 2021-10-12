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
Case Type   : 功能测试
Case Name   : add_months函数与其它函数嵌套使用
Description : add_months(d,n)描述：用于计算时间点d再加上n个月的时间。
    1. 函数与其它函数嵌套使用
Expect      :
    1. 返回结果正确
History     :
"""
import time
import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Add_Months_Case0005开始")
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_add(self):
        sql_cmd = """select add_months(to_date('05 Dec 2000',
         'DD Mon YYYY'),'89');"""
        exp1 = '2008-05-05 00:00:00'
        msg = self.commonsh.execut_db_sql(sql_cmd)
        LOG.info(f'msg = {msg}')
        self.assertTrue(msg.splitlines()[2].strip() == exp1)

        sql_cmd = '''select add_months(current_date,
        to_number(date_part('month',date'2018-09-28')));'''
        msg1 = self.commonsh.execut_db_sql(sql_cmd)
        LOG.info(f'msg1 = {msg1}')
        date = msg1.splitlines()[2].split()[0]
        LOG.info(f'date = {date}')
        msg2 = self.user.sh("""date +"%Y-%m-%d" -d'+9 month'""").result()
        LOG.info(f'msg2 = {msg2}')
        exp2 = msg2.strip()
        LOG.info(f'exp2 = {exp2}')
        self.assertTrue(exp2 >= date)

    def tearDown(self):
        LOG.info("Opengauss_Function_Innerfunc_Add_Months_Case0005结束")
