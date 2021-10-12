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
Case Name   : 使用transaction_timestamp()函数返回当前日期及时间
Description : transaction_timestamp()描述：当前日期及时间，与current_timestamp等效。
    1.正常获取select transaction_timestamp();
    2.异常校验
Expect      :
    1.函数返回结果正确
    2.异常报错
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info('\
            Opengauss_Function_Innerfunc_Transaction_Timestamp_Case0001开始')
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_timestamp(self):
        now = self.user.sh('date "+%Y-%m-%d %H:%M:%S"').result()
        # 测试点1：正常获取
        cmd = '''select transaction_timestamp();'''
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        db_time = msg.splitlines()[2].strip()  # 2021-01-08 15:57:42.610956+08
        self.assertTrue(len(db_time) > 23)
        cmd0 = f"select '{now}'::timestamp - '{db_time}'::timestamp;"
        msg0 = self.commonsh.execut_db_sql(cmd0)
        LOG.info(msg0)
        diff = msg0.splitlines()[-2].strip().strip('-')
        self.assertTrue(diff[:5] == '00:00')
        self.assertTrue(db_time[-3:] == '+08')
        # 测试点2：错误调用
        cmd1 = 'select transaction_timestamp;' \
               'select transaction_timestamp(987&&&);'
        msg1 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg1)
        self.assertTrue(msg1.count('ERROR') == 2)

    def tearDown(self):
        LOG.info('\
            Opengauss_Function_Innerfunc_Transaction_Timestamp_Case0001结束')