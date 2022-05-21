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
Case Name   : 测试系统视图PG_VARIABLE_INFO字段与数据类型
Description :
    1.查看系统视图PG_VARIABLE_INFO的结构
    2.该视图字段与对应字段数据类型是否正确
Expect      :
    1.查看系统视图PG_VARIABLE_INFO的结构成功
    2.该视图字段与字段数据类型对应正确
History     :
    modified：2021/10/12 by 5318639 优化用例适配新代码
"""

import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class SystemView(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--------Opengauss_Function_System_View_Case0086start--------')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['node_name', 'next_oid', 'next_xid', 'oldest_xid',
                       'xid_vac_limit', 'oldest_xid_db',
                       'last_extend_csn_logpage',
                       'start_extend_csn_logpage', 'next_commit_seqno',
                       'latest_completed_xid', 'startup_max_xid'],
            'Type': ['text', 'oid', 'xid', 'xid', 'xid', 'oid', 'xid', 'xid',
                     'xid', 'xid', 'xid']}

    def test_sysview(self):
        text = '----------step1:查看表结构;expect:查看成功-------------'
        self.log.info(text)
        msg = self.comsh.execut_db_sql('\d PG_VARIABLE_INFO')
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
            '------Opengauss_Function_System_View_Case0086finsh--------')
