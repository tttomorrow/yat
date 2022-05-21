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
Case Type   : 数据库系统
Case Name   : 设置recovery_min_apply_delay为非法值
Description :
    1.设置recovery_min_apply_delay参数为-1
    2.设置recovery_min_apply_delay参数为4294967295
    3.设置recovery_min_apply_delay参数为小数
    4.设置recovery_min_apply_delay参数为字母符号
Expect      :
    1.设置失败
    2.设置失败
    3.设置失败
    4.设置失败
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class RecoveryDelay(unittest.TestCase):
    db_primary_user_node = Node(node='PrimaryDbUser')
    commshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0007 start---")
        self.constant = Constant()

    def test_recovery_delay(self):
        self.log.info('-----设置recovery_min_apply_delay参数为-1----')
        result = self.commshpri.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'recovery_min_apply_delay=-1')
        self.assertFalse(result)

        self.log.info('-----设置recovery_min_apply_delay参数为2147483648----')
        result = self.commshpri.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            'recovery_min_apply_delay=2147483648')
        self.assertFalse(result)

        self.log.info('-----设置recovery_min_apply_delay参数为小数----')
        sql = f"alter SYSTEM set recovery_min_apply_delay to '1.5' "
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn('ALTER', result)

        self.log.info('-----设置recovery_min_apply_delay参数为字母符号----')
        result = self.commshpri.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            "recovery_min_apply_delay='qw_fr'")
        self.assertFalse(result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0007 end--")