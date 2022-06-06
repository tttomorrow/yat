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
Case Type   : GUC参数
Case Name   : 修改参数enable_sonic_optspill，观察预期结果
Description :
    1.show参数默认值
    2.修改参数默认值为off
    3.show参数值
    4.恢复参数默认值
Expect      :
    1.参数默认值为on
    2.修改参数默认值为off成功
    3.参数值为off
    4.恢复参数默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Guc_Queryplan_Case0109开始')
        self.dbuser = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_guc_queryplan(self):
        text = '--step1:show参数默认值;expect:参数默认值on--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show enable_sonic_optspill;')
        self.log.info(sql_cmd)
        self.default_value = sql_cmd.splitlines()[2].strip()
        self.log.info(self.default_value)

        text = '--step2:修改参数默认值为off;expect:修改成功--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              'enable_sonic_optspill =off')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:查询修改后参数值;expect:参数默认值off--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show enable_sonic_optspill;')
        self.log.info(sql_cmd)
        self.assertIn('off', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step4:恢复参数默认值;expect:恢复默认值成功--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              'enable_sonic_optspill =off')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('Opengauss_Function_Guc_Queryplan_Case0109结束')
