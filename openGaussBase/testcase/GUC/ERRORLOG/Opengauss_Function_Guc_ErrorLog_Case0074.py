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
Case Type   : GUC_ErrorLog
Case Name   : 参数log_min_duration_statement的值设置设为2min，24h
Description :
    1.修改参数log_min_duration_statement的值为2147483647：gs_guc reload -N all -I
    all -c "log_min_duration_statement=2147483647"
    查看值：show log_min_duration_statement;
Expect      :
    1.参数设置成功,返回2147483647ms
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0074 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('-----查看log_min_duration_statement默认值-----')
        sql_cmd0 = 'show log_min_duration_statement;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'log_min_duration_statement', '30min',
                                '(1 row)', flag='1')
        self.logger.info('--设置参数log_min_duration_statement值为2147483647--')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_min_duration_statement=2147483647"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-----查看log_min_duration_statement修改后的值-----')
        sql_cmd2 = 'show log_min_duration_statement;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_min_duration_statement',
                                '2147483647ms', '(1 row)', flag='1')

    def tearDown(self):
        self.logger.info('--------------恢复配置----------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
                      f'all -c "log_min_duration_statement=30min"'''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-------查看 log_min_duration_statement修改后的值-----')
        sql_cmd2 = 'show log_min_duration_statement;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_min_duration_statement', '30min',
                                '(1 row)', flag='1')
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0074 finish--')
