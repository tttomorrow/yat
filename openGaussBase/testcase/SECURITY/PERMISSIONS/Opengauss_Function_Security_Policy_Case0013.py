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
Case Name   : 设置password_lock_time=0，账户在短时间内自动解锁
Description :
    1.修改参数failed_login_attempts=0
    2.多次输错密码
Expect      :
    1.修改成功
    2.账号自动解锁，用户可以登录
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-------Opengauss_Function_Security_Policy_Case0013 start------')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()

    def test_policy(self):
        self.logger.info(
            '-----------查看failed_login_attempts默认值为10 -----------')
        sql_cmd0 = 'show failed_login_attempts;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'failed_login_attempts', '10',
                                  '(1 row)', flag='1')
        self.logger.info('----------password_lock_time修改后的值为0--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "password_lock_time=0"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = f'show password_lock_time;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'password_lock_time', '0', '(1 row)',
                                flag='1')
        self.logger.info('------------创建用户----------')
        sql_cmd3 = f'create user wf with password \'{macro.COMMON_PASSWD}\';'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.logger.info('----------错误密码登录，账号锁定-------------')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U wf -W ' \
                      f'{self.new_password} -c "\\q"'
        self.logger.info(excute_cmd4)
        msg4 = ''
        for i in range(11):
            msg4 = self.userNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
        self.assertNotIn(self.constant.ACCOUNT_LOCKED_TYPE, msg4)
        self.logger.info('---------再次用正确密码登录数据库，并执行sql语句-------')
        sql_cmd6 = 'select user;'
        excute_cmd6 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U wf -W ' \
                      f'{macro.COMMON_PASSWD} -c "{sql_cmd6}"'
        self.logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        self.logger.info(msg6)
        self.common.equal_sql_mdg(msg6, 'current_user', 'wf', '(1 row)',
                                flag='1')

    def tearDown(self):
        self.logger.info('----------恢复配置，清理环境----------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "password_lock_time=1"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = 'show password_lock_time;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'password_lock_time', '1d', '(1 row)',
                                flag='1')
        sql_cmd3 = 'drop user wf;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find('DROP ROLE') > -1)
        self.logger.info(
            '------Opengauss_Function_Security_Policy_Case0013 finish------')
