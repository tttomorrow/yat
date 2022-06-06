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
Case Name   : 测试系统视图PG_SESSION_IOSTAT字段与数据类型
Description :
    1.查看系统视图PG_SESSION_IOSTAT的结构
    2.该视图字段与对应字段数据类型是否正确
Expect      :
    1.查看系统视图PG_SESSION_IOSTAT的结构成功
    2.该视图字段与字段数据类型对应正确
History     :
    modified：2021/10/12 by 5318639 优化用例适配新代码
"""

import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class IndexFileDamaged(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '------Opengauss_Function_System_View_Case0035start------')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['query_id', 'mincurriops', 'maxcurriops',
                       'minpeakiops', 'maxpeakiops', 'io_limits',
                       'io_priority', 'query', 'node_group',
                       'curr_io_limits'],
            'Type': ['bigint', 'integer', 'integer', 'integer', 'integer',
                     'integer', 'text', 'text', 'text', 'integer']}

    def test_sysview(self):
        text = '----------step1:查看表结构;expect:查看成功-------------'
        self.log.info(text)
        msg = self.comsh.execut_db_sql('\d PG_SESSION_IOSTAT')
        self.log.info(msg)
        result_dict = self.com.format_sql_result(msg)
        self.log.info(result_dict)
        text = '-----step2:查看表字段与对应字段数据类型是否正确;expect:对应正确-----'
        self.log.info(text)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict,
                             '执行失败' + text)

    def tearDown(self):
        self.log.info(
            '--------Opengauss_Function_System_View_Case0035finsh--------')
