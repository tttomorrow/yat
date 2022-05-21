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
Case Type   : 防篡改
Case Name   : 验证历史记录数可配置
Description :
    1.查询参数password_reuse_max值
    2.修改password_reuse_max参数值为3
    3.恢复默认值
Expect      :
    1.显示默认值0
    2.显示设置后的值3
    3.默认值恢复成功
History     : 
"""


import os
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()
        self.default_value = self.common.show_param('password_reuse_max')

    def test_security(self):
        text = '----step1:查询参数password_reuse_max值;  expect:默认值0----'
        self.logger.info(text)
        show_para = self.default_value
        self.logger.info(show_para)
        self.assertEqual("0", show_para, "执行失败:" + text)

        text = '----step2:修改password_reuse_max参数值为3 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter system set password_reuse_max to 3;
            select pg_sleep(2);
            show password_reuse_max;''')
        self.logger.info(sql_cmd)
        self.assertEqual("3", sql_cmd.split("\n")[-2].strip(),
                         "执行失败:" + text)

    def tearDown(self):
        text = '----step3:恢复默认值 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter system set password_reuse_max to {self.default_value};
            select pg_sleep(2);
            show password_reuse_max;''')
        self.logger.info(sql_cmd)
        self.assertEqual("0", sql_cmd.split("\n")[-2].strip(),
                         "执行失败:" + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
