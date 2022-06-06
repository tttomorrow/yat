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
Case Type   : keep_sync_window
Case Name   : gs_guc reload方法设置参数keep_sync_window为有效值
Description :
        1.修改参数值0
        2.查询参数值
        3.修改参数值2147483647
        4.查询参数值
        5.修改参数值1min
        6.查询参数值
        7.恢复默认值
Expect      :
        1.修改成功
        2.参数值为0
        3.修改成功
        4.参数值为2147483647s
        5.修改成功
        6.参数值为1min
        7.恢复默认值成功
History     :
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0002 start-')
        self.constant = Constant()
        self.common = Common()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.default_value = self.common.show_param('keep_sync_window')

    def test_keep_sync_window(self):
        text = '--step1:修改参数值0;expect:修改成功--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"keep_sync_window=0")
        self.assertTrue(result, '执行失败' + text)

        text = '--step2:查询参数值;expect:参数值为0--'
        self.log.info(text)
        sql_cmd = self.common.show_param('keep_sync_window')
        self.log.info(sql_cmd)
        self.assertEqual('0', sql_cmd, '执行失败' + text)

        text = '--step3:修改参数值2147483647;expect:修改成功--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"keep_sync_window=2147483647")
        self.assertTrue(result, '执行失败' + text)

        text = '--step4:查询参数值;expect:参数值为2147483647s--'
        self.log.info(text)
        sql_cmd = self.common.show_param('keep_sync_window')
        self.log.info(sql_cmd)
        self.assertEqual('2147483647s', sql_cmd, '执行失败' + text)

        text = '--step5:修改参数值1min;expect:修改成功--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"keep_sync_window=1min")
        self.assertTrue(result, '执行失败' + text)

        text = '--step6:查询参数值;expect:参数值为1min--'
        self.log.info(text)
        sql_cmd = self.common.show_param('keep_sync_window')
        self.log.info(sql_cmd)
        self.assertEqual('1min', sql_cmd, '执行失败' + text)

    def tearDown(self):
        text = '--step7:恢复默认值;expect:恢复默认值成功--'
        self.log.info(text)
        restore = self.pri_sh.execute_gsguc("reload",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"keep_sync_window="
                                            f"{self.default_value}")
        sql_cmd = self.common.show_param('keep_sync_window')
        self.log.info(sql_cmd)
        self.assertTrue(restore, '执行失败' + text)
        self.assertEqual('0', sql_cmd, '执行失败' + text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0002 finish-')
