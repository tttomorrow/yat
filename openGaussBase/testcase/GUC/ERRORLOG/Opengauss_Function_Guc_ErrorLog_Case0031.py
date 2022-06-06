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
Case Type   : GUC_ErrorLog
Case Name   : 参数log_rotation_age的值设置为35791394
Description :
    1.修改参数log_rotation_age的值为35791394：gs_guc reload -N all -I all -c
    "log_rotation_age=35791394"
    2.log_directory路径下为空，执行重启数据库，生成一个日志文件，设置时间超过设置时间，
    再次重启数据库，查看日志文件
Expect      :
    1.参数设置成功
    2.再次重启数据库，查看日志文件，生成新的生日志文件
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        Logger.info('----Opengauss_Function_Guc_ErrorLog_Case0031 start----')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')
        Logger.info('-------查看log_directory默认路径------')
        self.path_return = ''
        check_path_cmd = 'show log_directory;'
        check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
        Logger.info(check_path_msg)
        self.path_return = check_path_msg.splitlines()[2].strip()
        Logger.info(self.path_return)
        self.assertTrue(self.path_return.find(macro.PG_LOG_PATH) > -1)

    def test_errorlog(self):
        Logger.info(
            '---修改log_directory路径,log_statement的值,log_rotation_age的值---')
        excute_cmd0 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{self.log_path}\'";gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_statement=mod";' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_rotation_age=35791394min"'
        Logger.info(excute_cmd0)
        execute_msg0 = self.userNode.sh(excute_cmd0).result()
        Logger.info(execute_msg0)
        sql_cmd1 = 'show log_rotation_age;'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        Logger.info(sql_msg1)
        self.common.equal_sql_mdg(sql_msg1, 'log_rotation_age', '35791394min',
                                  '(1 row)', flag='1')
        sql_cmd2 = f'rm -rf {self.log_path}/*'
        sql_msg2 = self.primaryRoot.sh(sql_cmd2).result()
        Logger.info(sql_msg2)
        Logger.info('-------重启数据库生成日志文件------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_om -t stop && gs_om -t start'
        excute_msg2 = self.userNode.sh(excute_cmd2).result()
        Logger.info(excute_msg2)
        Logger.info('-------查看是否生成日志文件-------')
        excute_cmd3 = f'ls {self.log_path}'
        excute_msg3 = self.primaryRoot.sh(excute_cmd3).result()
        Logger.info(excute_msg3)
        self.assertTrue(len(excute_msg3.split()) == 1)
        Logger.info('-------修改系统时间大于设定时间，执行sql语句-------')
        date_return_cmd = 'date -d "+35791395 min" "+%Y-%m-%d %H:%M:%S"'
        date_return_msg = self.primaryRoot.sh(date_return_cmd).result()
        mod_date_cmd = f'date -s "{date_return_msg}"'
        Logger.info(mod_date_cmd)
        mod_date_msg = self.primaryRoot.sh(mod_date_cmd).result()
        Logger.info(mod_date_msg)
        sql_cmd5 = 'drop table if exists errorlog0031;'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        Logger.info(msg5)
        Logger.info('-------查看日志文件，有新生成的日志文件-------')
        excute_cmd6 = f'ls {self.log_path}'
        excute_msg6 = self.primaryRoot.sh(excute_cmd6).result()
        Logger.info(excute_msg6)
        self.assertTrue(len(excute_msg6.split()) > 1)
        
    def tearDown(self):
        Logger.info('-------恢复系统时间-------')
        rec_time_cmd = f'hwclock -s'
        Logger.info(rec_time_cmd)
        rec_time_msg = self.primaryRoot.sh(rec_time_cmd).result()
        Logger.info(rec_time_msg)
        Logger.info('--------恢复配置，清理环境--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{self.path_return}\'";' \
                      f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                      f'-c "log_statement=none"'
        Logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg1)
        Logger.info('-------查看log_directory是否恢复-------')
        sql_cmd2 = 'show log_directory;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        Logger.info(msg2)
        msg_return = msg2.splitlines()[2].strip()
        Logger.info(msg_return)
        self.assertTrue(macro.PG_LOG_PATH in msg_return)
        Logger.info('-------查看log_statement是否恢复-------')
        sql_cmd3 = 'show log_statement;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        Logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'log_statement', 'none',
                                  '(1 row)', flag='1')
        Logger.info('-----恢复log_rotation_age的默认值-----')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_rotation_age=1d"'
        msg4 = self.userNode.sh(excute_cmd4).result()
        Logger.info(msg4)
        Logger.info('-------查看log_rotation_age是否恢复-------')
        sql_cmd5 = 'show log_rotation_age;'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        Logger.info(msg5)
        self.common.equal_sql_mdg(msg5, 'log_rotation_age', '1d',
                                  '(1 row)', flag='1')
        Logger.info('-------清理生成的日志文件-------')
        excute_cmd6 = f'rm -rf {self.log_path};ls {self.log_path}'
        Logger.info(excute_cmd6)
        msg6 = self.primaryRoot.sh(excute_cmd6).result()
        Logger.info(msg6)
        self.assertTrue(msg6.find("No such file or directory") > -1)
        Logger.info('--Opengauss_Function_Guc_ErrorLog_Case0031 finish--')
