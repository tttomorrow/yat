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
Case Type   : 系统表
Case Name   : 测试系统表GS_WLM_OPERATOR_INFO字段与数据类型
Description :
    1.查看系统表GS_WLM_OPERATOR_INFO的表结构
    2.该表字段与对应字段数据类型是否正确
Expect      :
    1.查看系统表GS_WLM_OPERATOR_INFO的表结构成功
    2.该表字段与字段数据类型对应正确
History     :
"""

import unittest
import sys
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class IndexFileDamaged(unittest.TestCase):
    def setUp(self):
        logger.info('----------------this is setup-----------------------')
        logger.info('----------------Opengauss_Function_System_Table_Case0003开始执行--------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['queryid', 'pid', 'plan_node_id', 'plan_node_name', 'start_time', 'duration', 'query_dop',
                       'estimated_rows', 'tuple_processed', 'min_peak_memory', 'max_peak_memory', 'average_peak_memory',
                       'memory_skew_percent', 'min_spill_size', 'max_spill_size', 'average_spill_size',
                       'spill_skew_percent', 'min_cpu_time', 'max_cpu_time', 'total_cpu_time', 'cpu_skew_percent',
                       'warning'],
            'Type': ['bigint', 'bigint', 'integer', 'text', 'timestamp with time zone', 'bigint', 'integer', 'bigint',
                     'bigint', 'integer', 'integer', 'integer', 'integer', 'integer', 'integer', 'integer', 'integer',
                     'bigint', 'bigint', 'bigint', 'integer', 'text']}

    def test_Index_file_damaged(self):
        logger.info('----------------------------查看表结构-----------------------------')
        msg = self.comsh.execut_db_sql('\d GS_WLM_OPERATOR_INFO')
        logger.info(msg)
        result_dict = self.com.format_sql_result(msg)
        logger.info(result_dict)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict,result_dict)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        # 无须清理环境
        logger.info('-----------------------Opengauss_Function_System_Table_Case0003执行完成-----------------------------')
