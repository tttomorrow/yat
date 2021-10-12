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
Case Name   : 测试系统视图GS_WLM_SESSION_STATISTICS字段与数据类型
Description :
    1.查看系统视图GS_WLM_SESSION_STATISTICS的结构
    2.该视图字段与对应字段数据类型是否正确
Expect      :
    1.查看系统视图GS_WLM_SESSION_STATISTICS的结构成功
    2.该视图字段与字段数据类型对应正确
History     :
"""

import sys
import unittest
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class IndexFileDamaged(unittest.TestCase):
    def setUp(self):
        logger.info('----------------this is setup-----------------------')
        logger.info('--------------Opengauss_Function_System_View_Case0012开始执行--------------')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['datid', 'dbname', 'schemaname', 'nodename', 'username', 'application_name', 'client_addr',
                       'client_hostname', 'client_port', 'query_band', 'pid', 'sessionid', 'block_time', 'start_time',
                       'duration', 'estimate_total_time', 'estimate_left_time', 'enqueue', 'resource_pool',
                       'control_group', 'estimate_memory', 'min_peak_memory', 'max_peak_memory', 'average_peak_memory',
                       'memory_skew_percent', 'spill_info', 'min_spill_size', 'max_spill_size', 'average_spill_size',
                       'spill_skew_percent', 'min_dn_time', 'max_dn_time', 'average_dn_time', 'dntime_skew_percent',
                       'min_cpu_time', 'max_cpu_time', 'total_cpu_time', 'cpu_skew_percent', 'min_peak_iops',
                       'max_peak_iops', 'average_peak_iops', 'iops_skew_percent', 'warning', 'queryid', 'query',
                       'query_plan', 'node_group', 'top_cpu_dn', 'top_mem_dn'],
            'Type': ['oid', 'name', 'text', 'text', 'name', 'text', 'inet', 'text', 'integer', 'text', 'bigint',
                     'bigint', 'bigint', 'timestamp with time zone', 'bigint', 'bigint', 'bigint', 'text', 'name',
                     'text', 'integer', 'integer', 'integer', 'integer', 'integer', 'text', 'integer', 'integer',
                     'integer', 'integer', 'bigint', 'bigint', 'bigint', 'integer', 'bigint', 'bigint', 'bigint',
                     'integer', 'integer', 'integer', 'integer', 'integer', 'text', 'bigint', 'text', 'text', 'text',
                     'text', 'text']}

    def test_Index_file_damaged(self):
        logger.info('----------------------------查看表结构-----------------------------')
        msg = self.comsh.execut_db_sql('\d GS_WLM_SESSION_STATISTICS')
        logger.info(msg)
        result_dict = self.com.format_sql_result(msg)
        logger.info(result_dict)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        # 无须清理环境
        logger.info('-----------------------Opengauss_Function_System_View_Case0012执行完成-----------------------------')
