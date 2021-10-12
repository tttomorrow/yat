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
Case Name   : 设置参数log_rotation_size值为2097151KB
Description :
    1.设置参数log_rotation_size值为2097151：gs_guc reload -N all -I all -c
    "log_rotation_size=2097151"
    2.清空log_directory，重启数据库使$path下生成日志文件：
    gs_om -t stop && gs_om -t start
    3.构造日志信息文件大于2097151KB，执行sql语句，查看日志文件
Expect      :
    1.设置成功
    2.重启数据库成功，生成日志文件
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
        Logger.info('----Opengauss_Function_Guc_ErrorLog_Case0037 start----')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')

    def test_errorlog(self):
        Logger.info('------查看log_directory默认路径------')
        global path_return
        check_path_cmd = 'show log_directory;'
        check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
        Logger.info(check_path_msg)
        path_return = check_path_msg.splitlines()[2].strip()
        Logger.info(path_return)
        self.assertTrue(path_return.find(macro.PG_LOG_PATH) > -1)
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
        Logger.info('-------修改log_rotation_size的值为2097151------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'\'log_rotation_size=2097151\''
        Logger.info(excute_cmd1)
        excute_msg1 = self.userNode.sh(excute_cmd1).result()
        Logger.info(excute_msg1)
        sql_cmd1 = 'show log_rotation_size;'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        Logger.info(sql_msg1)
        self.common.equal_sql_mdg(sql_msg1, 'log_rotation_size', '2097151kB',
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
        Logger.info('------构造文件大小大于2097151KB,查看是否生成新的日志文件------')
        excute_cmd4 = f'dd if=/dev/zero of={self.log_path}/{excute_msg3} ' \
                      f'bs=2KB count=2097152;'
        Logger.info(excute_cmd4)
        excute_msg4 = self.userNode.sh(excute_cmd4).result()
        Logger.info(excute_msg4)
        sql_cmd5 = 'create table errorlog0031(id int);' \
                   'insert into errorlog0031 values(5);' \
                   'drop table errorlog0031;'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        Logger.info(msg5)
        Logger.info('-------查看生成了新的日志文件-------')
        excute_cmd6 = f'ls {self.log_path}'
        excute_msg6 = self.primaryRoot.sh(excute_cmd6).result()
        Logger.info(excute_msg6)
        self.assertTrue(len(excute_msg6.split()) == 2)

    def tearDown(self):
        Logger.info('--------恢复配置，清理环境--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{path_return}\'";' \
                      f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                      f'-c "log_statement=none";gs_guc reload -N all -I all ' \
                      f'-c "log_rotation_size=20MB"'
        Logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg1)
        Logger.info('-------查看参数配置是否恢复-------')
        sql_cmd2 = 'show log_directory;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        Logger.info(msg2)
        msg_return = msg2.splitlines()[2].strip()
        Logger.info(msg_return)
        self.assertTrue(macro.PG_LOG_PATH in msg_return)
        sql_cmd3 = 'show log_statement;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        Logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'log_statement', 'none', '(1 row)',
                                  flag='1')
        sql_cmd4 = 'show log_rotation_size;'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        Logger.info(msg4)
        self.common.equal_sql_mdg(msg4, 'log_rotation_size', '20MB', '(1 row)',
                                  flag='1')
        Logger.info('--------清理生成的日志文件-------')
        excute_cmd3 = f'rm -rf {self.log_path};ls {self.log_path}'
        Logger.info(excute_cmd3)
        msg3 = self.primaryRoot.sh(excute_cmd3).result()
        Logger.info(msg3)
        self.assertTrue(msg3.find("No such file or directory") > -1)
        Logger.info('--Opengauss_Function_Guc_ErrorLog_Case0037 finish--')
