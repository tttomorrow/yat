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
Case Type   : 系统视图
Case Name   : 测试系统视图PG_STAT_ACTIVITY字段与数据类型
Description :
    1.查看系统视图PG_STAT_ACTIVITY的结构
    2.该视图字段与对应字段数据类型是否正确
Expect      :
    1.查看系统视图PG_STAT_ACTIVITY的结构成功
    2.该视图字段与字段数据类型对应正确
History     :
"""

import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class SystemView(unittest.TestCase):
    def setUp(self):
        LOG.info('----------------this is setup-----------------------')
        LOG.info(
            '----------Opengauss_Function_System_View_Case0039开始执行-------')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['datid', 'datname', 'pid', 'sessionid', 'usesysid',
                       'usename', 'application_name', 'client_addr',
                       'client_hostname', 'client_port', 'backend_start',
                       'xact_start', 'query_start', 'state_change',
                       'waiting', 'enqueue', 'state', 'resource_pool',
                       'query_id', 'query', 'connection_info'],
            'Type': ['oid', 'name', 'bigint', 'bigint', 'oid', 'name', 'text',
                     'inet', 'text', 'integer',
                     'timestamp with time zone', 'timestamp with time zone',
                     'timestamp with time zone',
                     'timestamp with time zone', 'boolean', 'text', 'text',
                     'name', 'bigint', 'text', 'text']}

    def test_index_file_damaged(self):
        LOG.info(
            '------------------------查看表结构---------------------')
        msg = self.comsh.execut_db_sql('\d PG_STAT_ACTIVITY')
        LOG.info(msg)
        result_dict = self.com.format_sql_result(msg)
        LOG.info(result_dict)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        # 无须清理环境
        LOG.info(
            '-----Opengauss_Function_System_View_Case0039执行完成-----------')
