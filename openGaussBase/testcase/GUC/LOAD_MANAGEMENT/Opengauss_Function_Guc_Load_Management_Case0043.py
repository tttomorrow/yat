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
Case Name   : 修改session_respool为invalid_pool，观察预期结果；
Description :
    1、查询session_respool默认值 ；
    show session_respool;
    2、修改session_respool为invalid_pool，重启使其生效，并校验其预期结果；
    set session_respool to default_pool;
    show session_respool;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值
    2、参数修改成功，校验修改后系统参数值为abc
    3、DML无报错
    4、恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH('PrimaryDbUser')


class GucTestCase(unittest.TestCase):
    def setUp(self):
        LOGGER.info('==Guc_Load_Management_Case0043开始执行==')
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)

    def test_guc(self):
        LOGGER.info('查询session_respool 期望：默认值invalid_pool')
        sql_cmd = COMMONSH.execut_db_sql('show session_respool;')
        LOGGER.info(sql_cmd)
        self.assertEqual('invalid_pool', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('修改session_respool为default_pool，'
                    '使其生效，期望：设置成功')
        LOGGER.info('期望：设置后查询结果为default_pool')
        sql_cmd = COMMONSH.execut_db_sql('''set session_respool to 
            default_pool;
            show session_respool;
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn('default_pool', sql_cmd)
        self.assertIn('SET', sql_cmd)
        LOGGER.info('设置后查询为invalid_pool')
        sql_cmd = COMMONSH.execut_db_sql('show session_respool;')
        LOGGER.info(sql_cmd)
        self.assertEqual('invalid_pool', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('做DML')
        sql_cmd = COMMONSH.execut_db_sql('''set session_respool to 
            default_pool;
            drop table if exists test cascade;
            create table test(c_int int);
            insert into test values(1),(2);
            update test set c_int = 5 where c_int = 1;
            delete from test where c_int = 2;
            select * from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

    def tearDown(self):
        LOGGER.info('恢复默认值')
        sql_cmd = COMMONSH.execut_db_sql('show session_respool;')
        if 'invalid_pool' != sql_cmd.split('\n')[-2].strip():
            COMMONSH.execute_gsguc('set',
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  'session_respool=invalid_pool')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        LOGGER.info('==-Guc_Load_Management_Case0043执行结束==')
