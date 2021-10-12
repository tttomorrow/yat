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
Case Type   : Separation_policy
Case Name   : 设置password_lock_time=0.5，到期后被锁定的账户自动解锁
Description :
    1.修改参数failed_login_attempts=0.5
    2.多次输错密码导致账户锁定，将系统时间设置推后>=0.5天，再次用户登录数据库
Expect      :
    1.参数修改成功
    2.修改时间后，再次登录成功
History     :
"""
import os
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
        self.logger.info('Opengauss_Function_Security_Policy_Case0011 start')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
        self.Constant = Constant()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.file_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')

    def test_policy(self):
        self.logger.info('-------查看log_directory默认路径------')
        global path_return
        check_path_cmd = 'show log_directory;'
        check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
        self.logger.info(check_path_msg)
        path_return = check_path_msg.splitlines()[2].strip()
        self.logger.info(path_return)
        self.assertTrue(path_return.find(macro.PG_LOG_PATH) > -1)
        self.logger.info('-------配置log_directory合法路径------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{self.file_path}\'"'
        execute_msg4 = self.userNode.sh(excute_cmd0).result()
        self.logger.info(execute_msg4)
        self.logger.info('----查看日志路径----')
        sql_execute = f'show log_directory;'
        msg_log = self.sh_primy.execut_db_sql(sql_execute)
        self.logger.info(msg_log)
        self.common.equal_sql_mdg(msg_log, 'log_directory', self.file_path,
                                '(1 row)', flag='1')
        self.logger.info('---查看failed_login_attempts默认值为10------')
        sql_cmd0 = 'show failed_login_attempts;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'failed_login_attempts', '10', '(1 row)',
                                flag='1')
        self.logger.info("----------password_lock_time修改后的值为0.5--------")
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'\'password_lock_time=0.5\''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = f'show password_lock_time;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'password_lock_time', '12h', '(1 row)',
                                flag='1')
        self.logger.info('-------------创建用户----------')
        sql_cmd3 = f'create user wf with password \'{macro.COMMON_PASSWD}\';'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.logger.info('------------错误密码登录，账号锁定-------------')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U wf -W ' \
                      f'{self.new_password} -c "\\q"'
        self.logger.info(excute_cmd4)
        msg4 = ''
        for i in range(11):
            msg4 = self.userNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
        self.assertIn(self.Constant.ACCOUNT_LOCKED_TYPE, msg4)
        self.logger.info('----将系统时间设置推后>=0.5天，再次用户登录数据库-------')
        date_return_cmd = 'date -d "+13 hour" "+%Y-%m-%d %H:%M:%S"'
        date_return_msg = self.primaryRoot.sh(date_return_cmd).result()
        mod_date_cmd = f'date -s "{date_return_msg}"'
        self.logger.info(mod_date_cmd)
        mod_date_msg = self.primaryRoot.sh(mod_date_cmd).result()
        self.logger.info(mod_date_msg)
        self.logger.info('--------再次用正确密码登录数据库，并执行sql语句--------')
        sql_cmd6 = 'select user;'
        excute_cmd6 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W' \
                      f' {macro.COMMON_PASSWD} -c "{sql_cmd6}"'
        self.logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        self.logger.info(msg6)
        self.common.equal_sql_mdg(msg6, 'current_user', 'wf', '(1 row)',
                                flag='1')

    def tearDown(self):
        self.logger.info('--------------恢复时间-------------')
        shell_cmd7 = f'hwclock -s'
        self.logger.info(shell_cmd7)
        msg7 = self.primaryRoot.sh(shell_cmd7).result()
        self.logger.info(msg7)
        now_time_new = self.sh_primy.execut_db_sql('SELECT sysdate;')
        self.logger.info(now_time_new)
        self.logger.info('-----------恢复配置，清理环境-----------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "password_lock_time=1"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = f'show password_lock_time;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'password_lock_time', '1d', '(1 row)',
                                flag='1')
        sql_cmd3 = 'drop user wf;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find('DROP ROLE') > -1)
        self.logger.info("-------恢复log_directory路径，清理环境-------")
        recover_cmd = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{path_return}\'"'
        self.logger.info(recover_cmd)
        recover_msg = self.userNode.sh(recover_cmd).result()
        self.logger.info(recover_msg)
        self.logger.info('-------查看配置是否恢复-------')
        check_path_cmd = 'show log_directory;'
        check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
        self.logger.info(check_path_msg)
        self.assertTrue(macro.PG_LOG_PATH in path_return)
        self.logger.info('-------清理生成的日志文件-------')
        clear_cmd = f'rm -rf  {self.file_path};ls {self.file_path}'
        clear_msg = self.primaryRoot.sh(clear_cmd).result()
        self.logger.info(clear_msg)
        self.assertTrue(clear_msg.find('No such file or directory') > -1)
        self.logger.info('Opengauss_Function_Security_Policy_Case0011 finish')
