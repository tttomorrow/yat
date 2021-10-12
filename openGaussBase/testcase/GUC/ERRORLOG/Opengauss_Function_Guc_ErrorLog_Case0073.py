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
Case Name   : 参数log_min_duration_statement的值设置设为2min，24h
Description :
    1.修改参数log_min_duration_statement的值为1s：gs_guc reload -N all -I all -c
    "log_min_duration_statement=1s",查看参数：show log_min_duration_statement；
    2.修改参数log_min_duration_statement的值为1h：gs_guc reload -N all -I all -c
    "log_min_duration_statement=1h",查看参数：show log_min_duration_statement；
    3.修改参数log_min_duration_statement的值为1d：gs_guc reload -N all -I all -c
    "log_min_duration_statement=1d",查看参数：show log_min_duration_statement；
Expect      :
    1.返回值：1s
    2.返回值：1h
    3.返回值：1d
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0073 start--')
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
        self.logger.info('-----设置参数log_min_duration_statement值为1s----')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_min_duration_statement=1s"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-----查看log_min_duration_statement修改后的值-----')
        sql_cmd2 = 'show log_min_duration_statement;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_min_duration_statement', '1s',
                                '(1 row)', flag='1')
        self.logger.info('-----设置参数log_min_duration_statement值为1h----')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
                      f'all -c "log_min_duration_statement=1h"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-----查看log_min_duration_statement修改后的值-----')
        sql_cmd2 = 'show log_min_duration_statement;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_min_duration_statement', '1h',
                                '(1 row)', flag='1')
        self.logger.info('-----设置参数log_min_duration_statement值为1d----')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
                      f'all -c "log_min_duration_statement=1d"'''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-----查看log_min_duration_statement修改后的值-----')
        sql_cmd2 = 'show log_min_duration_statement;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_min_duration_statement', '1d',
                                '(1 row)', flag='1')

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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0073 finish--')
