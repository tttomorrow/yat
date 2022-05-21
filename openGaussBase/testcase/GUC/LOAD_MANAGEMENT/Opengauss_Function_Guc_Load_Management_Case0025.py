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
Case Type   : GUC
Case Name   : 修改enable_resource_record为on，观察预期结果；
Description :
    1、查询enable_resource_record默认值 ；
    show resource_track_duration;
    2、修改resource_track_duration为120，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c 'enable_resource_track=on'
    gs_guc set -D {cluster/dn1} -c 'resource_track_level=operator'
    gs_guc set -D {cluster/dn1} -c 'enable_resource_record=on'
    gs_guc set -D {cluster/dn1} -c 'resource_track_cost=1'
    gs_guc set -D {cluster/dn1} -c 'resource_track_duration=120'
    gs_om -t stop && gs_om -t start
    show resource_track_duration;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值
    2、参数修改成功，校验修改后系统参数值为off
    3、DML无报错 查询gs_wlm_plan_operator_history不变
    4、恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

LOGGER = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info('==Guc_Load_Management_Case0025开始执行==')
        self.constant = Constant()
        self.user_node = Node('PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)

    def test_guc(self):
        LOGGER.info('查询enable_resource_record 期望：默认值off')
        sql_cmd = COMMONSH.execut_db_sql('show resource_track_duration;')
        LOGGER.info(sql_cmd)
        self.assertEqual('1min', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('修改enable_resource_record为off，'
                    '重启生效，期望设置成功')
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_resource_track=on')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_level=operator')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_resource_record=on')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_cost=1')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_duration=120')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'use_workload_manager=on')
        self.assertTrue(result)

        LOGGER.info('期望：重启后查询结果为设置值')
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        sql_cmd = COMMONSH.execut_db_sql('''show enable_resource_track;
            show resource_track_level;
            show enable_resource_record;
            show resource_track_cost;
            show resource_track_duration;
            show use_workload_manager;
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn('on', sql_cmd)
        self.assertIn('operator', sql_cmd)
        self.assertIn('1', sql_cmd)
        self.assertIn('2min', sql_cmd)

        LOGGER.info('查询gs_wlm_plan_operator_info数据量')
        result1 = COMMONSH.execut_db_sql(f"select count(*) from "
            f"gs_wlm_plan_operator_history "
            f"where datname='{self.user_node.db_name}';")
        LOGGER.info(result1)

        LOGGER.info('做DML')
        sql_cmd = COMMONSH.execut_db_sql('''drop table if exists test ;
            create table test(c_int int);
            insert into test values(1),(2);
            update test set c_int = 5 where c_int = 1;
            delete from test where c_int = 2;
            select * from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)
        LOGGER.info('查询gs_wlm_plan_operator_info数据量不变')
        result2 = COMMONSH.execut_db_sql(f"select count(*) from "
            f"gs_wlm_plan_operator_history "
            f"where datname='{self.user_node.db_name}';")
        LOGGER.info(result2)
        self.assertEqual(int(result2.split('\n')[-2].strip()),
                         int(result1.split('\n')[-2].strip()))

        LOGGER.info('恢复默认值')
        LOGGER.info('删除表')
        sql_cmd = COMMONSH.execut_db_sql('drop table test cascade;')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_resource_track=on')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_level=query')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_resource_record=off')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_cost=100000')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_duration=1min')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'use_workload_manager=off')
        self.assertTrue(result)

        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in result or 'Normal' in result)

    def tearDown(self):
        LOGGER.info('恢复默认值')
        sql_cmd = COMMONSH.execut_db_sql('''show enable_resource_track;
            show resource_track_level;
            show enable_resource_record;
            show resource_track_cost;
            show resource_track_duration;
            show use_workload_manager;
            ''')
        LOGGER.info(sql_cmd)
        info_list = ['on', 'off', 'query', '100000', '1min']
        for info in info_list:
            if info != sql_cmd.split('\n')[-2].strip():
                COMMONSH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                      'enable_resource_track=on')
                COMMONSH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                      'resource_track_level=query')
                COMMONSH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                      'enable_resource_record=off')
                COMMONSH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                      'resource_track_cost=100000')
                COMMONSH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                      'resource_track_duration=1min')
                COMMONSH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                      'use_workload_manager=off')

                result = COMMONSH.restart_db_cluster()
                LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        LOGGER.info('==Guc_Load_Management_Case0025执行结束==')
