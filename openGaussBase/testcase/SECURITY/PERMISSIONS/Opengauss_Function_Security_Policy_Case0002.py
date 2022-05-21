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
Case Name   : 取消用户revoke权限
Description :
    1.执行 gs_guc set -N all -I all -c "password_lock_time=1"，
    重启数据库（gs_om -t stop && gs_om -t start）
    2.多次输错密码导致账户锁定，用户登录数据库(gsql -d $data_name -p $data_port -U
    $user_name -W $passwd -r)
    3.将系统时间设置推后》=1天，再次用户登录数据库(gsql -d $data_name -p $data_port
    -U $user_name -W $passwd -r)
Expect      :
    1.返回为：10
    2.CREATE ROLE
    3.第十一次登录时，账号被自动锁定
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


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('----Opengauss_Function_Security_Policy_Case0002 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
        self.Constant = Constant()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_policy(self):
        logger.info('---------------create user ------------')
        sql_cmd0 = f'show failed_login_attempts;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'failed_login_attempts', '10',
                                  '(1 row)', flag='1')
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W {self.new_password}'
        logger.info(excute_cmd2)
        msg2 = ''
        for i in range(11):
            msg2 = self.userNode.sh(excute_cmd2).result()
            logger.info(msg2)
        self.assertIn(self.Constant.ACCOUNT_LOCKED_TYPE, msg2)

    def tearDown(self):
        logger.info('-----------清理环境-----------')
        sql_cmd1 = 'drop user wf;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('---Opengauss_Function_Security_Policy_Case0002 finish---')
