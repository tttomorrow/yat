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
Case Name   : 设定用户开始时间小于结束时间
Description :
    1.用系统管理员用户或初始用户登录数据库
    2.创建一个用户，起始时间小于结束时间：CREATE USER wf WITH PASSWORD '*****'
    VALID BEGIN '$start_time' VALID UNTIL '$end_time';
    3.创建的用户登录数据库
    4.时间过期后登录数据库
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

from utils.Constant import Constant


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Security_Policy_Case0019 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.primaryRoot = Node(node='PrimaryRoot')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
        self.user = 'user_policy_0019'
        self.constant = Constant()
        self.common = Common()
        self.file_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')
        self.default_param = self.common.show_param('log_directory')

    def test_policy(self):
        self.logger.info('-------pre1:配置log_directory为新路径------')
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                                    f'log_directory=\'{self.file_path}\'')
        self.logger.info('----------pre2:获取当前时间----------')
        now_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        sleep(5)
        start_time = now_time_msg.splitlines()[2].strip()
        date_return_cmd = 'date -d "+2 day" "+%Y-%m-%d %H:%M:%S"'
        end_time = self.primaryRoot.sh(date_return_cmd).result()
        self.logger.info(end_time)
        
        text = '----step1-2:创建一个用户，起始时间小于结束时间;expect:成功----'
        self.logger.info(text)
        sql_cmd1 = f'create user {self.user} with password ' \
                   f'\'{macro.COMMON_PASSWD}\' VALID BEGIN \'{start_time}\' ' \
                   f'VALID UNTIL \'{end_time}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertEqual(self.constant.CREATE_ROLE_SUCCESS_MSG, msg1,
                        text + '执行失败')
        text = '----step3:创建的用户登录数据库;expect:成功----'
        self.logger.info(text)
        sql_cmd2 = 'select user;'
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-U {self.user} -W {macro.COMMON_PASSWD} -c "{sql_cmd2}"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'current_user', f'{self.user}',
                                  '(1 row)', flag='1')
        text = '----step4:时间过期后登录数据库;expect:成功----'
        self.logger.info(text)
        date_return_cmd = 'date -d "+49 hour" "+%Y-%m-%d %H:%M:%S"'
        date_return_msg = self.primaryRoot.sh(date_return_cmd).result()
        mod_date_cmd = f'date -s "{date_return_msg}"'
        self.logger.info(mod_date_cmd)
        mod_date_msg = self.primaryRoot.sh(mod_date_cmd).result()
        self.logger.info(mod_date_msg)
        excute_cmd3 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U {self.user} -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertIn('The account is not within the period of validity',
                      msg3, text + '执行失败')

    def tearDown(self):
        text1 = '----1.恢复时间;expect:成功---'
        self.logger.info(text1)
        shell_cmd1 = f'hwclock -s'
        self.logger.info(shell_cmd1)
        msg1 = self.primaryRoot.sh(shell_cmd1).result()
        text2 = '----2.删除用户;expect:成功---'
        self.logger.info(text2)
        sql_cmd2 = f'drop user {self.user};'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        text3 = '----3.恢复log_directory路径;expect:成功---'
        self.logger.info(text3)
        self.sh_primy.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f'log_directory=\'{self.default_param}\'')
        text4 = '----4.删除文件;expect:成功---'
        self.logger.info(text4)
        clear_cmd = f'rm -rf  {self.file_path};' \
            f'ls {self.file_path}'
        msg3 = self.primaryRoot.sh(clear_cmd).result()
        self.logger.info(msg3)
        self.assertEqual('', msg1, text1 + '执行失败')
        self.assertEqual(self.constant.DROP_ROLE_SUCCESS_MSG, msg2,
                         text2 + '执行失败')
        self.assertIn('No such file or directory', msg3, text4 + '执行失败')
        self.logger.info(
            '----Opengauss_Function_Security_Policy_Case0019 finish----')
