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
Case Name   : 设定用户开始时间小于结束时间
Description :
    1.用系统管理员用户或初始用户登录数据库
    2.创建一个用户user019，起始时间小于结束时间：CREATE USER wf WITH PASSWORD '*****'
    VALID BEGIN '$start_time' VALID UNTIL '$end_time';
    3.登录用户
    4.时间过期后登录用户
Expect      :
    1.数据库登录成功
    2.用户创建成功
    3.用户登录正常
    4.用户无法登录，提示账号不在有效期内
History     :
"""
import os
import unittest
from time import sleep
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Security_Policy_Case0019 start-')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
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
        self.logger.info('-------配置log_directory为新路径------')
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
        self.logger.info('---------获取时间----------')
        now_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        sleep(5)
        start_time = now_time_msg.splitlines()[2].strip()
        date_return_cmd = 'date -d "+2 day" "+%Y-%m-%d %H:%M:%S"'
        end_time = self.primaryRoot.sh(date_return_cmd).result()
        self.logger.info(end_time)
        self.logger.info('--------------创建用户,并登录 -------------')
        sql_cmd1 = f'create user user019 with password ' \
                   f'\'{macro.COMMON_PASSWD}\' VALID BEGIN \'{start_time}\' ' \
                   f'VALID UNTIL \'{end_time}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue(msg1.find("CREATE ROLE") > -1)
        sql_cmd2 = 'select user;'
        excute_cmd2 = f'source {self.DB_ENV_PATH};gsql -d ' \
                      f'{self.userNode.db_name} -p {self.userNode.db_port}' \
                      f' -U user019 -W {macro.COMMON_PASSWD} -c "{sql_cmd2}"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'current_user', 'user019', '(1 row)',
                                  flag='1')
        self.logger.info('-------------修改时间超过密码有效期,并登录------------')
        date_return_cmd = 'date -d "+49 hour" "+%Y-%m-%d %H:%M:%S"'
        date_return_msg = self.primaryRoot.sh(date_return_cmd).result()
        mod_date_cmd = f'date -s "{date_return_msg}"'
        self.logger.info(mod_date_cmd)
        mod_date_msg = self.primaryRoot.sh(mod_date_cmd).result()
        self.logger.info(mod_date_msg)
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user019 -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "select user;"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(
            msg3.find('The account is not within the period of validity') > -1)

    def tearDown(self):
        self.logger.info('------------恢复时间-------------')
        shell_cmd0 = f'hwclock -s'
        self.logger.info(shell_cmd0)
        msg0 = self.primaryRoot.sh(shell_cmd0).result()
        self.logger.info(msg0)
        self.logger.info('-----------清理环境-----------')
        sql_cmd1 = 'drop user user019;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue(msg1.find('DROP ROLE') > -1)
        self.logger.info('-------恢复log_directory路径，清理环境-------')
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
        self.logger.info(
            '----Opengauss_Function_Security_Policy_Case0019 finish----')
