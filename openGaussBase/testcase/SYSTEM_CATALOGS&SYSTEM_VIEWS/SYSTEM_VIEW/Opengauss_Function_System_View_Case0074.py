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
Case Type   : 系统视图
Case Name   : 测试系统视图PLAN_TABLE字段与数据类型
Description :
    1.查看系统视图PLAN_TABLE的结构且该视图字段与对应字段数据类型是否正确
Expect      :
    1.查看系统视图PLAN_TABLE的结构成功且该视图字段与字段数据类型对应正确
History     :
"""

import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class SystemView(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['statement_id', 'plan_id', 'id', 'operation',
                       'options', 'object_name', 'object_type',
                       'object_owner', 'projection', 'cost', 'cardinality'],
            'Type': ['character varying(30)', 'bigint', 'integer',
                     'character varying(30)', 'character varying(255)',
                     'name', 'character varying(30)', 'name',
                     'character varying(4000)', 'double precision',
                     'double precision']}

    def test_system_view(self):
        text = '---step1:查看系统表PLAN_TABLE的表结构且该表字段与对应字段数据类型是否正确;expect:成功---'
        self.log.info(text)
        check_cmd = self.comsh.execut_db_sql('\d PLAN_TABLE')
        self.log.info(check_cmd)
        result_dict = self.com.format_sql_result(check_cmd)
        self.log.info(result_dict)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict,
                             '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----无须清理环境-----')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
