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
Case Name   : 测试系统视图GS_WLM_SESSION_INFO_ALL字段与数据类型
Description :
    1.查看系统视图GS_WLM_SESSION_INFO_ALL的结构
    2.该视图字段与对应字段数据类型是否正确
Expect      :
    1.查看系统视图GS_WLM_SESSION_INFO_ALL的结构成功
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
        logger.info('--------------Opengauss_Function_System_View_Case0010开始执行--------------')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['datid', 'dbname', 'schemaname', 'nodename', 'username', 'application_name', 'client_addr',
                       'client_hostname', 'client_port', 'query_band', 'block_time', 'start_time', 'finish_time',
                       'duration', 'estimate_total_time', 'status', 'abort_info', 'resource_pool', 'control_group',
                       'estimate_memory', 'min_peak_memory', 'max_peak_memory', 'average_peak_memory',
                       'memory_skew_percent', 'spill_info', 'min_spill_size', 'max_spill_size', 'average_spill_size',
                       'spill_skew_percent', 'min_dn_time', 'max_dn_time', 'average_dn_time', 'dntime_skew_percent',
                       'min_cpu_time', 'max_cpu_time', 'total_cpu_time', 'cpu_skew_percent', 'min_peak_iops',
                       'max_peak_iops', 'average_peak_iops', 'iops_skew_percent', 'warning', 'queryid', 'query',
                       'query_plan', 'node_group', 'cpu_top1_node_name', 'cpu_top2_node_name', 'cpu_top3_node_name',
                       'cpu_top4_node_name', 'cpu_top5_node_name', 'mem_top1_node_name', 'mem_top2_node_name',
                       'mem_top3_node_name', 'mem_top4_node_name', 'mem_top5_node_name', 'cpu_top1_value',
                       'cpu_top2_value', 'cpu_top3_value', 'cpu_top4_value', 'cpu_top5_value', 'mem_top1_value',
                       'mem_top2_value', 'mem_top3_value', 'mem_top4_value', 'mem_top5_value', 'top_mem_dn',
                       'top_cpu_dn', 'n_returned_rows', 'n_tuples_fetched', 'n_tuples_returned', 'n_tuples_inserted',
                       'n_tuples_updated', 'n_tuples_deleted', 'n_blocks_fetched', 'n_blocks_hit', 'db_time',
                       'cpu_time', 'execution_time', 'parse_time', 'plan_time', 'rewrite_time', 'pl_execution_time',
                       'pl_compilation_time', 'net_send_time', 'data_io_time', 'is_slow_query'],
            'Type': ['oid', 'text', 'text', 'text', 'text', 'text', 'inet', 'text', 'integer', 'text', 'bigint',
                     'timestamp with time zone', 'timestamp with time zone', 'bigint', 'bigint', 'text', 'text', 'text',
                     'text', 'integer', 'integer', 'integer', 'integer', 'integer', 'text', 'integer', 'integer',
                     'integer', 'integer', 'bigint', 'bigint', 'bigint', 'integer', 'bigint', 'bigint', 'bigint',
                     'integer', 'integer', 'integer', 'integer', 'integer', 'text', 'bigint', 'text', 'text', 'text',
                     'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'bigint', 'bigint',
                     'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'text', 'text',
                     'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint',
                     'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint', 'bigint']}

    def test_Index_file_damaged(self):
        logger.info('----------------------------查看表结构-----------------------------')
        msg = self.comsh.execut_db_sql('\d GS_WLM_SESSION_INFO_ALL')
        logger.info(msg)
        result_dict = self.com.format_sql_result(msg)
        logger.info(result_dict)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        # 无须清理环境
        logger.info('-----------------------Opengauss_Function_System_View_Case0010执行完成-----------------------------')
