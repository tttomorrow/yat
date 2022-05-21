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
Case Name   : 密码不可重用天数为默认大于60
Description :
    1.设置不可重用天数默认值为61天，gs_guc reload -N all -I all -c
     "password_reuse_time=61"，重启数据库
    2.创建用户user002,create user user001 with password "******";
    3.修改2次用户密码，第2次将用户密码改回原密码
    4.修改系统时间为61天后，将密码修改为原密码
Expect      :
    1.设置成功
    2.创建成功
    3.修改失败，提示密码不可重复
    4.密码修改成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Security_Policy_Case0062 start-')
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
        self.logger.info("-------配置log_directory合法路径------")
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
        self.logger.info("----------预置条件：password_reuse_max=0-------")
        sql_cmd0 = 'show password_reuse_max;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'password_reuse_max', '0', '(1 row)',
                                flag='1')
        self.logger.info('-------修改参数password_reuse_time值为61----------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all ' \
                      f'-c "password_reuse_time=61"'
        self.logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg1)
        sql_cmd1 = 'show password_reuse_time;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'password_reuse_time', '61', '(1 row)',
                                flag='1')
        self.logger.info('-------------创建用户user002 ------------')
        sql_cmd2 = f'create user user002 with password ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertTrue(msg2.find('CREATE ROLE') > -1)
        self.logger.info('修改2次用户密码，第2次将用户密码改回原密码')
        new_password = macro.COMMON_PASSWD + "qaz"
        sql_cmd3 = f'alter user user002 with password \'{new_password}\';'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find("ALTER ROLE") > -1)
        sql_cmd4 = f'alter user user002 with password' \
                   f' \'{macro.COMMON_PASSWD}\';'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.assertTrue(msg4.find("The password cannot be reused") > -1)
        self.logger.info("-------修改时间为61天后，再次修改用户密码为原密码-------")
        date_return_cmd = 'date -d "+62 day" "+%Y-%m-%d %H:%M:%S"'
        date_return_msg = self.primaryRoot.sh(date_return_cmd).result()
        mod_date_cmd = f'date -s "{date_return_msg}"'
        self.logger.info(mod_date_cmd)
        mod_date_msg = self.primaryRoot.sh(mod_date_cmd).result()
        self.logger.info(mod_date_msg)
        sql_cmd3 = f'alter user user002 with password' \
                   f' \'{macro.COMMON_PASSWD}\';'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find("ALTER ROLE") > -1)

    def tearDown(self):
        self.logger.info('----------------恢复时间-------------')
        shell_cmd0 = 'hwclock -s'
        self.logger.info(shell_cmd0)
        msg0 = self.primaryRoot.sh(shell_cmd0).result()
        self.logger.info(msg0)
        self.logger.info('-----------清理环境,恢复配置-----------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all ' \
                      f'-c "password_reuse_time=60"'
        self.logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg1)
        sql_cmd1 = 'show password_reuse_time;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'password_reuse_time', '60', '(1 row)',
                                flag='1')
        sql_cmd3 = 'drop user user002;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find('DROP ROLE') > -1)
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
        self.logger.info('Opengauss_Function_Security_Policy_Case0062 finish')
