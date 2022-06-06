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
Case Type   : Separation_policy
Case Name   : 设置failed_login_attempts=9,密码第十次错误，账号自动锁定
Description :
    1.在postgres.conf中设置failed_login_attempts=9，重启数据库生效
    2.初始用户执行：create user wf with password '$PASSWORD';
    3.用wf用户登录，输入错误的密码，登录十次
Expect      :
    1.设置成功，数据库重启成功
    2.CREATE ROLE
    3.第十次登录时，账号被自动锁定
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
common = Common()
sh_primy = CommonSH('PrimaryDbUser')


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_Policy_Case0003 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
        self.Constant = Constant()
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_policy(self):
        logger.info('--------------create user ------------')
        sql_cmd = f'source {self.DB_ENV_PATH};' \
                  f'gs_guc reload -N all -I all -c "failed_login_attempts=9"'
        msg0 = self.userNode.sh(sql_cmd).result()
        logger.info(msg0)
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W {self.new_password}'
        logger.info(excute_cmd2)
        msg2 = ''
        for i in range(10):
            msg2 = self.userNode.sh(excute_cmd2).result()
            logger.info(msg2)
        self.assertIn(self.Constant.ACCOUNT_LOCKED_TYPE, msg2)

    def tearDown(self):
        logger.info('-----------清理环境-----------')
        sql_cmd1 = 'drop user if exists wf cascade;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"failed_login_attempts=10";' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd1}"'
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info('---Opengauss_Function_Security_Policy_Case0003 finish---')
