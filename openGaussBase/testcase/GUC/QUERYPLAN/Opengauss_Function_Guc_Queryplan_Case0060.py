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
Case Type   : GUC参数
Case Name   : cpu_operator_cost参数使用gs_guc set设置为其他数据类型，
                验证其预期结果
Description :
    1.查询cpu_operator_cost默认值
    2.修改cpu_operator_cost为test
    3.修改cpu_operator_cost为'test'
Expect      :
    1.查询cpu_operator_cost默认值成功
    2.修改cpu_operator_cost为test失败
    3.修改cpu_operator_cost为'test'失败
History     :
"""

import sys
import unittest

from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant

LOG = Logger()


class GucQueryplan(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('-----Opengauss_Function_Guc_Queryplan_Case0060-------')
        self.com = Common()
        self.comsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.pv = ''

    def test_Guc_queryplan(self):
        LOG.info('--------查看cpu_operator_cost默认值---------')
        msg = self.comsh.execut_db_sql('show cpu_operator_cost;')
        LOG.info(msg)
        self.pv = msg.splitlines()[-2].strip()

        LOG.info('------修改cpu_operator_cost为test--------')
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      'cpu_operator_cost=test')
        LOG.info(msg)
        self.assertTrue(self.constant.INCORRECT_VALUES[0] + ' test ' +
                        self.constant.INCORRECT_VALUES[
                            1] + ' "cpu_operator_cost" ' +
                        self.constant.INCORRECT_VALUES[2])

        LOG.info("------修改cpu_operator_cost为'test'--------")
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      "cpu_operator_cost='test'")
        LOG.info(msg)
        self.assertTrue(self.constant.INCORRECT_VALUES[0] + " 'test' " +
                        self.constant.INCORRECT_VALUES[
                            1] + ' "cpu_operator_cost" ' +
                        self.constant.INCORRECT_VALUES[2])

    def tearDown(self):
        LOG.info('----this is tearDown------')
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       f"cpu_operator_cost={self.pv}")
        LOG.info(msg)
        stopmsg = self.comsh.stop_db_cluster()
        LOG.info(stopmsg)
        startmsg = self.comsh.start_db_cluster()
        LOG.info(startmsg)
        LOG.info('---Opengauss_Function_Guc_Queryplan_Case0060执行完成---')
