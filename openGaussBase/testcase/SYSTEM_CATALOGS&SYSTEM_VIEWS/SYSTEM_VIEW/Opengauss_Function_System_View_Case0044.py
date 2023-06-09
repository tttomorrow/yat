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
Case Name   : 测试系统视图PG_STAT_DATABASE字段与数据类型
Description :
    1.查看系统视图PG_STAT_DATABASE的结构
    2.该视图字段与对应字段数据类型是否正确
Expect      :
    1.查看系统视图PG_STAT_DATABASE的结构成功
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
            '------Opengauss_Function_System_View_Case0044开始执行----------')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['datid', 'datname', 'numbackends', 'xact_commit',
                       'xact_rollback', 'blks_read', 'blks_hit',
                       'tup_returned', 'tup_fetched', 'tup_inserted',
                       'tup_updated', 'tup_deleted', 'conflicts',
                       'temp_files', 'temp_bytes', 'deadlocks',
                       'blk_read_time', 'blk_write_time', 'stats_reset'],
            'Type': ['oid', 'name', 'integer', 'bigint', 'bigint', 'bigint',
                     'bigint', 'bigint', 'bigint', 'bigint',
                     'bigint', 'bigint', 'bigint', 'bigint', 'bigint',
                     'bigint', 'double precision', 'double precision',
                     'timestamp with time zone']}

    def test_index_file_damaged(self):
        LOG.info(
            '--------------------查看表结构--------------------------')
        msg = self.comsh.execut_db_sql('\d PG_STAT_DATABASE')
        LOG.info(msg)
        result_dict = self.com.format_sql_result(msg)
        LOG.info(result_dict)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        # 无须清理环境
        LOG.info(
            '---Opengauss_Function_System_View_Case0044执行完成------------')
