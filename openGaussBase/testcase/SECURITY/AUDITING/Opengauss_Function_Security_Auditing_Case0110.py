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
Case Type   : security
Case Name   : 审计目录下审计文件的最大数量，默认1048576
Description :
    1.登录数据库执行show audit_file_remain_threshold；
Expect      :
    1.返回1048576
History     :
"""
import unittest
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '--Opengauss_Function_Security_Auditing_Case0110 start--')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_systools(self):
        self.logger.info('------查看audit_file_remain_threshold默认值------')
        sql_cmd0 = 'show audit_file_remain_threshold;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'audit_file_remain_threshold',
                                  '1048576', '(1 row)', flag='1')

    def tearDown(self):
        self.logger.info(
            '--Opengauss_Function_Security_Auditing_Case0110 finish--')
