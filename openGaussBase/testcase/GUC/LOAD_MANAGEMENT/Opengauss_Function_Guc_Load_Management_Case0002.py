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
Case Name   : 修改参数use_workload_manager为其他数据类型及超边界值
Description :
    1、查看use_workload_manager默认值 期望：off；
    show use_workload_manager;
    2、修改use_workload_manager为12345等，期望：合理报错
    gs_guc set -D {cluster/dn1} -c 'use_workload_manager=12345';
    3、恢复默认值 无需恢复
Expect      :
    1、查看use_workload_manager默认值 期望：off；
    2、修改use_workload_manager为12345等，期望：合理报错
    3、恢复默认值 无需恢复
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
        LOGGER.info('==Guc_Load_Management_Case0002开始执行==')
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)

    def test_guc(self):
        LOGGER.info('==查询use_workload_manager 期望：默认值off==')
        sql_cmd = COMMONSH.execut_db_sql('show use_workload_manager;')
        LOGGER.info(sql_cmd)
        self.assertEqual('off', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('==修改use_workload_manager为12345，'
                    '期望：合理报错==')
        LOGGER.info('==修改use_workload_manager为12345，'
                    '期望：修改失败，show参数为默认值==')
        result = COMMONSH.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       'use_workload_manager=12345')
        self.assertFalse(result)
        sql_cmd = COMMONSH.execut_db_sql('show use_workload_manager;')
        LOGGER.info(sql_cmd)
        self.assertEqual('off', sql_cmd.split('\n')[-2].strip())

    def tearDown(self):
        LOGGER.info('==恢复默认值==')
        LOGGER.info('恢复默认值')
        sql_cmd = COMMONSH.execut_db_sql('show use_workload_manager;')
        if 'off' != sql_cmd.split('\n')[-2].strip():
            COMMONSH.execute_gsguc('set',
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  'use_workload_manager=off')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        LOGGER.info('==-Guc_Load_Management_Case0002执行结束==')
