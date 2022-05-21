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
Case Name   : 修改memory_detail_tracking为空，观察预期结果；
Description :
    1、查询memory_detail_tracking默认值 ；
    show memory_detail_tracking;
    2、修改memory_detail_tracking为空，重启使其生效，并校验其预期结果；
    gs_guc set -D {cluster/dn1} -c 'memory_detail_tracking=140611422254848'
    gs_om -t stop && gs_om -t start
    show memory_detail_tracking;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值
    2、设置失败
    3、恢复默认值成功
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
        LOGGER.info('==Guc_Load_Management_Case0009开始执行==')
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)

    def test_guc(self):
        LOGGER.info('查询memory_detail_tracking 期望：默认值空')
        sql_cmd = COMMONSH.execut_db_sql('show memory_detail_tracking;')
        LOGGER.info(sql_cmd)
        self.assertEqual('', sql_cmd.split('\n')[-2].strip())

        LOGGER.info('修改memory_detail_tracking为140611422254848，'
                    '重启使其生效，期望：设置失败')
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'memory_detail_tracking=140611422254848')
        self.assertFalse(result)
        LOGGER.info('期望：重启后查询结果为空')
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        sql_cmd = COMMONSH.execut_db_sql('show memory_detail_tracking;')
        LOGGER.info(sql_cmd)
        self.assertEqual('', sql_cmd.split('\n')[-2].strip())

    def tearDown(self):
        LOGGER.info('恢复默认值')
        sql_cmd = COMMONSH.execut_db_sql('show memory_detail_tracking;')
        if '' != sql_cmd.split('\n')[-2].strip():
            COMMONSH.execute_gsguc('set',
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "memory_detail_tracking=''")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue('Degraded' in status or 'Normal' in status)
        LOGGER.info('==-Guc_Load_Management_Case0009执行结束==')
