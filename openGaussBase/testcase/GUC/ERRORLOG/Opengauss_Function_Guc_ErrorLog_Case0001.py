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
Case Type   : GUC_ErrorLog
Case Name   : 查看log_destination默认值为stderr
Description :
    1.查看log_destination默认值；
Expect      :
    1.默认值stderr；
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Errorlog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0001 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('--------------查看 log_destination默认值----------')
        sql_cmd0 = 'show log_destination;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'log_destination', 'stderr', '(1 row)',
                                flag='1')

    def tearDown(self):
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0001 finish--')
