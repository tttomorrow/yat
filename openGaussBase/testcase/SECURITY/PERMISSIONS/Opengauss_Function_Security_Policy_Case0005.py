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
Case Type   : policy
Case Name   : 设置failed_login_attempts=0,自动锁定功能不生效
Description :
    步骤 1.设置failed_login_attempts=0，重启数据库生效
    步骤 2.初始用户执行：create user wf with password '$PASSWORD';
    步骤 3.用wf用户登录，输入错误的密码，登录1000次
Expect      :
    步骤 1.设置成功，数据库重启成功
    步骤 2.CREATE ROLE
    步骤 3.账号未被自动锁定
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Policy(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '----Opengauss_Function_Security_Policy_Case0005 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
        self.Constant = Constant()
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.configure = 'failed_login_attempts=0'
        self.common.config_set_modify(self.configure)
        status_msg = self.sh_primy.get_db_cluster_status()
        self.logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

    def test_policy(self):
        self.logger.info('-------create user ----------')
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';'
        sql_cmd2 = '''select user;'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U wf -W ' \
                      f'{self.new_password} -c "{sql_cmd2}"'
        self.logger.info(excute_cmd2)
        msg2 = ''
        for i in range(1000):
            msg2 = self.userNode.sh(excute_cmd2).result()
            self.logger.info(msg2)
        self.assertIn(self.Constant.INVALID_USERNAME_OR_PASSWD_TYPE, msg2)

    def tearDown(self):
        self.logger.info('-----------恢复配置，并清理环境-----------')
        self.configure = 'failed_login_attempts=10'
        self.common.config_set_modify(self.configure)
        status_msg = self.sh_primy.get_db_cluster_status()
        self.logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        sql_cmd1 = 'alter user wf account unlock;' \
                   'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info('Opengauss_Function_Security_Policy_Case0005 finish')
