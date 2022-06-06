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
Case Name   : instr函数入参是特殊字符
Description :
    1.创建SQL_ASCII编码及UTF-8的数据库
    2.使用instr函数对特殊字符进行处理
    3.清理环境
Expect      :
    1.创建成功
    2.返回结果正确
    3.清理环境完成
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)}start -----')
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()
        self.db_name = "db_instr_case0005"
        self.db_name_01 = "db_instr_case0005_01"

    def test_right(self):
        sql_cmd = "select instr('@#%￥#……&￥￥&￥&','&',2,2) from sys_dummy;"
        text = '--step1:创建数据库;expect:成功--'
        self.log.info(text)
        db_create = f"drop database if exists {self.db_name};" \
                    f"create database {self.db_name} " \
                    f"encoding = 'SQL_ASCII';" \
                    f"drop database if exists {self.db_name_01};" \
                    f"create database {self.db_name_01} encoding = 'UTF8'"
        msg1 = self.commonsh.execut_db_sql(db_create)
        self.log.info(msg1)
        self.assertTrue(msg1.count(self.constant.CREATE_DATABASE_SUCCESS) == 2,
                        '执行失败:' + text)

        text = '--step2:分别连接新建的编码类型的库执行sql语句;expect:成功---'
        self.log.info(text)
        cmd1 = self.commonsh.execut_db_sql(sql_cmd, dbname=self.db_name)
        self.log.info(cmd1)
        self.assertEqual(cmd1.splitlines()[2].strip(), '21',
                         '执行失败:' + text)
        cmd1 = self.commonsh.execut_db_sql(sql_cmd, dbname=self.db_name_01)
        self.log.info(cmd1)
        self.assertEqual(cmd1.splitlines()[2].strip(), '11',
                         '执行失败:' + text)

    def tearDown(self):
        text = '--step3:清理环境;expect:成功--'
        self.log.info(text)
        db_drop = f'drop database {self.db_name};' \
                  f'drop database {self.db_name_01};'
        msg3 = self.commonsh.execut_db_sql(db_drop)
        self.log.info(msg3)
        self.assertTrue(msg3.count(self.constant.DROP_DATABASE_SUCCESS) == 2,
                        '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end -----')
