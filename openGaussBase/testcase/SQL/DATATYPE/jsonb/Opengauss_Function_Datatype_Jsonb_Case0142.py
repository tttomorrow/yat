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
Case Name   : MOT表不支持jsonb类型
Description :
    1. 创建mot表,包含列的类型为jsonb
    2.恢复环境
Expect      :
    1. 创建失败
    2.恢复环境
History     :
    的问题
"""

import os
import unittest
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Jsonb(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.primary_node = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        text = f'-----预置条件：enable_incremental_checkpoint=off-----'
        self.log.info(text)
        result = self.primary_node.get_db_cluster_status('detail')
        self.log.info(result)
        self.default_value = self.com.show_param(
            "enable_incremental_checkpoint")
        self.log.info(self.default_value)
        self.config_item = "enable_incremental_checkpoint=off"
        if 'off' != self.com.show_param("enable_incremental_checkpoint"):
            self.primary_node.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG, self.config_item)
            self.primary_node.restart_db_cluster()
            result = self.primary_node.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)

    def test_jsonb(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.schema = 'mot_jsonb_schema'
        self.tablename = 't_jsonb0142'
        self.datatype = 'jsonb'
        text = f'-----step1:创建mot表,包含列的类型为jsonb;expect:失败-----'
        self.log.info(text)
        sql_cmd = f'CREATE SCHEMA {self.schema};' \
            f'CREATE FOREIGN TABLE {self.schema}.{self.tablename}' \
            f'(t1 {self.datatype});' \
            f'DROP SCHEMA {self.schema} CASCADE;' \
            f'checkpoint;'
        msg = self.primary_node.execut_db_sql(sql_cmd)
        self.log.info(msg)
        self.assertIn(self.constant.NOT_SUPPORTED_TYPE, msg, '执行失败:' + text)

    def tearDown(self):
        text = f'-----step2:恢复环境;expect:恢复成功-----'
        self.log.info(text)
        sql_cmd = f'select pg_sleep(30);' \
            f'checkpoint;' \
            f'select pg_sleep(30);'
        msg = self.primary_node.execut_db_sql(sql_cmd)
        self.log.info(msg)
        self.assertIn('CHECKPOINT', msg, '执行失败:' + text)
        msg = self.primary_node.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"enable_incremental_checkpoint="
                                              f"{self.default_value}")
        self.log.info(msg)
        stop_msg = self.primary_node.stop_db_instance()
        self.log.info(stop_msg)
        start_msg = self.primary_node.start_db_cluster()
        self.log.info(start_msg)
        status = self.primary_node.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param(
            "enable_incremental_checkpoint")
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
