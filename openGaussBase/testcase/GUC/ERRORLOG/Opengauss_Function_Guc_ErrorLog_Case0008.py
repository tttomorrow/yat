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
Case Type   : GUC
Case Name   : 用gs_guc set方式设置参数log_destination的值为csvlog
Description :
    1.设置参数log_destination的值为csvlog：gs_guc set -N all -I all -c
    "log_destination='csvlog'"
    2.重启数据库，查看参数修改结果：show log_destination;
    3.恢复参数默认值
Expect      :
    1.参数设置成功
    2.数据库重启成功，返回值为csvlog
    3.参数默认值恢复成功
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0008 start--')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('---------修改参数log_destination的值为csvlog---------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -N all -I all -c ' \
                      f'"log_destination=\'csvlog\'";' \
                      f'gs_om -t stop && gs_om -t start'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = 'show log_destination;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'log_destination', 'csvlog', '(1 row)',
                                  flag='1')

    def tearDown(self):
        self.logger.info('-----------恢复配置-----------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_destination=\'stderr\'"'
        self.logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg1)
        sql_cmd2 = 'show log_destination;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'log_destination', 'stderr', '(1 row)',
                                  flag='1')
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0008 finish--')
