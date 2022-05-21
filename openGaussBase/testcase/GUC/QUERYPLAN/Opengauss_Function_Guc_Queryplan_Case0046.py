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
Case Name   : qrw_inlist2join_optmode参数使用gs_guc set设置为其他数据类型，
                验证其预期结果
Description :
    1.查询qrw_inlist2join_optmode默认值
    2.修改qrw_inlist2join_optmode为99999
    3.修改qrw_inlist2join_optmode为false
    4.清理环境，恢复默认值
Expect      :
    1.查询qrw_inlist2join_optmode默认值成功
    2.修改qrw_inlist2join_optmode为99999失败
    3.修改qrw_inlist2join_optmode为false失败
    4.清理环境，恢复默认值成功
History     :
"""

import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class GucQueryplan(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Guc_Queryplan_Case0046开始执行----')
        self.com = Common()
        self.comsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()

    def test_Guc_queryplan(self):
        LOG.info('--------查看qrw_inlist2join_optmode默认值---------')
        msg = self.comsh.execut_db_sql('show qrw_inlist2join_optmode;')
        LOG.info(msg)
        self.pv = msg.splitlines()[-2].strip()
        LOG.info(self.pv)
        self.assertIn('cost_base', self.pv)

        LOG.info('------修改qrw_inlist2join_optmode为99999--------')
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      'qrw_inlist2join_optmode=99999')
        LOG.info(msg)
        self.assertTrue(self.constant.INCORRECT_VALUES[0] + ' "99999" ' +
                        self.constant.INCORRECT_VALUES[
                            1] + ' "qrw_inlist2join_optmode" ' +
                        self.constant.INCORRECT_VALUES[2])

        LOG.info('------修改qrw_inlist2join_optmode为false--------')
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      'qrw_inlist2join_optmode=false')
        LOG.info(msg)
        self.assertTrue(self.constant.INCORRECT_VALUES[0] + ' false ' +
                        self.constant.INCORRECT_VALUES[
                            1] + ' "qrw_inlist2join_optmode" ' +
                        self.constant.INCORRECT_VALUES[2])

    def tearDown(self):
        LOG.info('----this is tearDown------')
        LOG.info('-------恢复默认值------')
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       f"qrw_inlist2join_optmode='cost_base'")
        LOG.info(msg)
        self.comsh.restart_db_cluster()
        result = self.comsh.get_db_cluster_status()
        self.assertTrue(msg)
        self.assertTrue("Degraded" in result or "Normal" in result, '重启数据库失败')
        LOG.info('----Opengauss_Function_Guc_Queryplan_Case0046执行完成---')
