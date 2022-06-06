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
Case Type   : guc参数
Case Name   : 修改参数archive_timeout，并观察预期结果
Description :
    1、查看archive_timeout默认值
    2、修改archive_timeout，校验其预期结果
    3、恢复默认值
Expect      :
    1、显示默认值
    2、参数修改成功，预期结果正常
    3、恢复默认值
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0026_开始---')
        self.userNode = Node('dbuser')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()

    def test_guc(self):
        text = '--step1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("archive_timeout")
        self.log.info(self.default_value)

        text = '--step2.1.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_timeout=10s")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step2.2.校验参数是否修改成功;expect:修改成功--'
        self.log.info(text)
        sql_cmd = self.sh_user.execut_db_sql(f'show archive_timeout;')
        self.log.info(sql_cmd)
        self.assertIn('10', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step3.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_timeout ="
                                              f"{self.default_value}")
        self.log.info(guc_msg1)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param("archive_timeout")
        self.log.info(self.recovery_value)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0026_结束---')
