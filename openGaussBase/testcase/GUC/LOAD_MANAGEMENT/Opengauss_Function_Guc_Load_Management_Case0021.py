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
Case Name   : 修改resource_track_level为on，观察预期结果；
Description :
    1、查询resource_track_level默认值 ；
    show resource_track_level;
    2、修改resource_track_level为none，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c 'resource_track_level=none'
    gs_om -t stop && gs_om -t start
    show resource_track_level;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值
    2、参数修改成功，校验修改后系统参数值为none
    3、DML无报错 查询gs_wlm_plan_operator_history数据量不变
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
        LOGGER.info('==Guc_Load_Management_Case0021开始执行==')
        self.constant = Constant()
        self.user_node = Node('PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)

    def test_guc(self):
        LOGGER.info('查询resource_track_level 期望：默认值query')
        sql_cmd = COMMONSH.execut_db_sql('show resource_track_level;')
        LOGGER.info(sql_cmd)
        self.assertEqual('query', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('修改resource_track_level为query，重启使其生效，'
                    '期望：设置成功')
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_level=none')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'use_workload_manager=on')
        self.assertTrue(result)

        LOGGER.info('期望：重启后查询结果为设置值')
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        sql_cmd = COMMONSH.execut_db_sql('show resource_track_level;')
        LOGGER.info(sql_cmd)
        self.assertEqual('none', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('查询gs_wlm_plan_operator_info数据量')
        result1 = COMMONSH.execut_db_sql(f"select count(*) "
            f"from gs_wlm_plan_operator_history "
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
        result2 = COMMONSH.execut_db_sql(f"select count(*) "
            f"from gs_wlm_plan_operator_history "
            f"where datname='{self.user_node.db_name}';")
        LOGGER.info(int(result2.split('\n')[-2].strip()))
        LOGGER.info(int(result1.split('\n')[-2].strip()))
        self.assertEqual(int(result2.split('\n')[-2].strip()),
                         int(result1.split('\n')[-2].strip()))

        LOGGER.info('恢复默认值')
        LOGGER.info('删除表')
        sql_cmd = COMMONSH.execut_db_sql('drop table test cascade;')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'resource_track_level=query')
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
        COMMONSH.execute_gsguc('set',
                               self.constant.GSGUC_SUCCESS_MSG,
                              'resource_track_level=query')
        COMMONSH.execute_gsguc('set',
                               self.constant.GSGUC_SUCCESS_MSG,
                              'use_workload_manager=off')
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        LOGGER.info('==-Guc_Load_Management_Case0021执行结束==')
