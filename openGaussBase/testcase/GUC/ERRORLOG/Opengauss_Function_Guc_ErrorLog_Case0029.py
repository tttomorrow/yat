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
Case Type   : GUC_ErrorLog
Case Name   : 参数log_rotation_age的值设置为1
Description :
    1.修改参数log_rotation_age的值为1：gs_guc reload -N all -I all -c
    "log_rotation_age=1"，log_directory路径下为空，执行重启数据库
    2.时间保持在一天内，执行sql，查看日志目录
    3.设置时间为一天后，再次查看日志目录
Expect      :
    1.参数设置成功，生成日志文件
    2.执行sql语句后，无新生成日志文件，仅一个日志文件
    3.生成新的日志文件
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
        Logger.info('----Opengauss_Function_Guc_ErrorLog_Case0029 start----')
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
        Logger.info('-------修改log_directory路径------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{self.log_path}\'"'
        Logger.info(excute_cmd0)
        execute_msg0 = self.userNode.sh(excute_cmd0).result()
        Logger.info(execute_msg0)
        Logger.info('-------修改log_statement的值------')
        mod_statement = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                        f'{macro.DB_INSTANCE_PATH} -c "log_statement=mod"'
        Logger.info(mod_statement)
        mod_msg = self.userNode.sh(mod_statement).result()
        Logger.info(mod_msg)
        sql_cmd0 = 'show log_statement;'
        sql_msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        Logger.info(sql_msg0)
        self.common.equal_sql_mdg(sql_msg0, 'log_statement', 'mod',
                                  '(1 row)', flag='1')
        Logger.info('-------查看log_rotation_age的值是否为1d------')
        sql_cmd1 = 'show log_rotation_age;'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        Logger.info(sql_msg1)
        value1_return = sql_msg1.splitlines()[2].strip()
        if value1_return != '1d':
            Logger.info('-------修改参数log_rotation_age的值为1d------')
            excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                          f'gs_guc reload -N all -I all -c ' \
                          f'\'log_rotation_age=1d\''
            Logger.info(excute_cmd1)
            excute_msg1 = self.userNode.sh(excute_cmd1).result()
            Logger.info(excute_msg1)
            sql_cmd2 = 'show log_rotation_age;'
            sql_msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
            Logger.info(sql_msg2)
            self.common.equal_sql_mdg(sql_msg1, 'log_rotation_age', '1d',
                                      '(1 row)', flag='1')
        del_cmd2 = f'rm -rf {self.log_path}/*'
        del_msg2 = self.primaryRoot.sh(del_cmd2).result()
        Logger.info(del_msg2)
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
        Logger.info('-------执行sql语句-------')
        sql_cmd5 = 'drop table if exists errorlog0031;'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        Logger.info(msg5)
        Logger.info('-------查看日志文件，无新生成的日志文件-------')
        excute_cmd6 = f'ls {self.log_path}'
        excute_msg6 = self.primaryRoot.sh(excute_cmd6).result()
        Logger.info(excute_msg6)
        self.assertTrue(len(excute_msg6.split()) == 1)
        Logger.info('-------修改时间为1天后，执行sql语句-------')
        date_return_cmd = 'date -d "+25 hour" "+%Y-%m-%d %H:%M:%S"'
        date_return_msg = self.primaryRoot.sh(date_return_cmd).result()
        mod_date_cmd = f'date -s "{date_return_msg}"'
        Logger.info(mod_date_cmd)
        mod_date_msg = self.primaryRoot.sh(mod_date_cmd).result()
        Logger.info(mod_date_msg)
        sql_cmd8 = 'drop table if exists errorlog0031;'
        msg8 = self.sh_primy.execut_db_sql(sql_cmd8)
        Logger.info(msg8)
        Logger.info('-------查看日志文件，有新生成的日志文件-------')
        excute_cmd9 = f'ls {self.log_path}'
        excute_msg9 = self.primaryRoot.sh(excute_cmd9).result()
        Logger.info(excute_msg9)
        self.assertTrue(len(excute_msg9.split()) > 1)

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
        Logger.info('--------清理生成的日志文件-------')
        excute_cmd3 = f'rm -rf {self.log_path};ls {self.log_path}'
        Logger.info(excute_cmd3)
        msg3 = self.primaryRoot.sh(excute_cmd3).result()
        Logger.info(msg3)
        self.assertTrue(msg3.find("No such file or directory") > -1)
        Logger.info('--Opengauss_Function_Guc_ErrorLog_Case0029 finish--')
