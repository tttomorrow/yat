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
Case Name   : 参数keep_sync_window无效值测试
Description :
        1.依次修改参数值为-1, 2147483648
        2.依次修改参数值为空值，null
        3.修改参数值为小数
        4.查询参数值
        5.恢复默认值
Expect      :
        1.合理报错
        2.合理报错
        3.合理报错
        4.参数值为0
        5.无须恢复默认值
History     :
"""

import re
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0005 start-')
        self.constant = Constant()
        self.common = Common()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.default_value = self.common.show_param('keep_sync_window')

    def test_keep_sync_window(self):
        text = '--step1:依次修改参数值为-1, 2147483648;expect:合理报错--'
        self.log.info(text)
        invalid_value = [-1, 2147483648]
        pattern = 'ERROR: The value .* is outside the valid range for ' \
                  'parameter "keep_sync_window" \(0 .. 2147483647\)'
        for i in invalid_value:
            result = self.pri_sh.execute_gsguc("reload",
                                               '',
                                               f"keep_sync_window={i}",
                                               get_detail=True)

            msg = re.search(pattern, result, re.S)
            self.assertIsNotNone(msg, '执行失败' + text)

        text = '--step2:依次修改参数值为空值，null;expect:合理报错--'
        self.log.info(text)
        invalid_value = ["''", 'null']
        for i in invalid_value:
            result = self.pri_sh.execute_gsguc("reload",
                                               '',
                                               f"keep_sync_window={i}",
                                               get_detail=True)
            assert_res = 'ERROR: The parameter "keep_sync_window" ' \
                         'requires an integer value'
            self.assertTrue(assert_res in result, '执行失败' + text)

        text = '--step3:修改参数值为小数，null;expect:合理报错--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc("reload",
                                           '',
                                           f"keep_sync_window=10.25",
                                           get_detail=True)
        assert_res = 'ERROR: Valid units for this parameter ' \
                     '"keep_sync_window" are "s", "min", "h", and "d".'
        self.assertTrue(assert_res in result, '执行失败' + text)

        text = '--step4:查询参数值;expect:参数值为0--'
        self.log.info(text)
        sql_cmd = self.common.show_param('keep_sync_window')
        self.log.info(sql_cmd)
        self.assertEqual('0', sql_cmd, '执行失败' + text)

    def tearDown(self):
        text = '--step5:恢复默认值;expect:无须恢复默认值--'
        self.log.info(text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0005 finish-')
