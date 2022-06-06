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
Case Type   : 系统表
Case Name   : 测试系统表PG_JOB字段与数据类型
Description :
    1.查看系统表PG_JOB的表结构
    2.该表字段与对应字段数据类型是否正确
Expect      :
    1.查看系统表PG_JOB的表结构成功
    2.该表字段与字段数据类型对应正确
History     :
    modified：2022/1/10 by 5318639 优化用例适配新代码
"""

import sys
import unittest

from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH


class IndexFileDamaged(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_System_Table_Case0036开始执行-----')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['job_id', 'current_postgres_pid', 'log_user',
                       'priv_user', 'dbname', 'node_name', 'job_status',
                       'start_date', 'next_run_date', 'failure_count',
                       'interval', 'last_start_date', 'last_end_date',
                       'last_suc_date', 'this_run_date', 'nspname',
                       'job_name', 'end_date', 'enable', 'failure_msg'],
            'Type': ['bigint', 'bigint', 'name', 'name', 'name', 'name',
                     '"char"', 'timestamp without time zone',
                     'timestamp without time zone', 'smallint', 'text',
                     'timestamp without time zone',
                     'timestamp without time zone',
                     'timestamp without time zone',
                     'timestamp without time zone',
                     'name', 'text', 'timestamp without time zone', 'boolean',
                     'text']}

    def test_Index_file_damaged(self):
        text = '----------step1:查看表结构;expect:查看成功-------------'
        self.log.info(text)
        msg = self.comsh.execut_db_sql('\d PG_JOB')
        self.log.info(msg)
        result_dict = self.com.format_sql_result(msg)
        self.log.info(result_dict)
        text = '-----step2:查看表字段与对应字段数据类型是否正确;expect:对应正确------'
        self.log.info(text)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict,
                             '执行失败' + text)

    def tearDown(self):
        self.log.info(
            '-----Opengauss_Function_System_Table_Case0036执行完成-----')
