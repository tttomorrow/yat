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
Case Type   : GUC
Case Name   : 修改transaction_pending_time为on，观察预期结果；
Description :
    1、查询transaction_pending_time默认值 ；
    show transaction_pending_time;
    2、修改transaction_pending_time为50，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c 'transaction_pending_time=50'
    gs_om -t stop && gs_om -t start
    show transaction_pending_time;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值
    2、参数修改成功，校验修改后系统参数值为50
    3、DML无报错
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
        LOGGER.info('==Guc_Load_Management_Case0051开始执行==')
        self.constant = Constant()
        self.user_node = Node('PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)

    def test_guc(self):
        LOGGER.info('查询transaction_pending_time 期望：默认值0')
        sql_cmd = COMMONSH.execut_db_sql('show transaction_pending_time;')
        LOGGER.info(sql_cmd)
        self.assertEqual('0', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('修改transaction_pending_time为on，'
                    '重启使其生效，期望：设置成功')
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'transaction_pending_time=50')
        self.assertTrue(result)

        LOGGER.info('期望：重启后查询结果为设置值')
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        sql_cmd = COMMONSH.execut_db_sql('show transaction_pending_time;')
        LOGGER.info(sql_cmd)
        self.assertIn('50', sql_cmd)

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

        LOGGER.info('恢复默认值')
        LOGGER.info('删除表')
        sql_cmd = COMMONSH.execut_db_sql('drop table test cascade;')
        LOGGER.info(sql_cmd)
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'transaction_pending_time=0')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in result or 'Normal' in result)

    def tearDown(self):
        LOGGER.info('恢复默认值')
        sql_cmd = COMMONSH.execut_db_sql('show transaction_pending_time;')
        LOGGER.info(sql_cmd)
        if '0' != sql_cmd.split('\n')[-2].strip():
            COMMONSH.execute_gsguc('set',
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  'transaction_pending_time=0')
            result = COMMONSH.restart_db_cluster()
            LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        LOGGER.info('==-Guc_Load_Management_Case0051执行结束==')
