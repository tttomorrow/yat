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
Case Name   : 设置参数log_destination的值为stderr,csvlog,查看日志文件
Description :
    1.设置参数log_destination的值为syslog, gs_guc reload -N all -I all -c
    "log_destination='stderr,csvlog'"；查看值：show log_destination;
    2.执行重启数据库操作：gs_om - t stop && gs_om -t start
    3.查看是否在 $gaussdb_log/$username/pg_log/下生成.csv的log日志,且日志打印在屏幕
Expect      :
    1.参数设置成功，返回值为csvlog,stderr
    2.重启数据库完成
    3.在 $gaussdb_log/$username/pg_log/下生成.scv的log日志,且日志打印在屏幕
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


class Errorlog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0004 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')

    def test_errorlog(self):
        self.logger.info('-------查看log_directory默认路径------')
        global path_return
        check_path_cmd = 'show log_directory;'
        check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
        self.logger.info(check_path_msg)
        path_return = check_path_msg.splitlines()[2].strip()
        self.logger.info(path_return)
        self.assertTrue(path_return.find(macro.PG_LOG_PATH) > -1)
        self.logger.info('-------配置log_directory合法路径------')
        execute_cmd = f'source {self.DB_ENV_PATH};' \
                       f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
                       f'"log_directory=\'{self.log_path}\'"'
        execute_msg = self.userNode.sh(execute_cmd).result()
        self.logger.info(execute_msg)
        self.logger.info('----查看日志路径----')
        sql_execute = f'show log_directory;'
        msg_log = self.sh_primy.execut_db_sql(sql_execute)
        self.logger.info(msg_log)
        self.common.equal_sql_mdg(msg_log, 'log_directory', self.log_path,
                                  '(1 row)', flag='1')
        self.logger.info('--------------查看log_destination默认值----------')
        sql_cmd0 = 'show log_destination;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'log_destination', 'stderr', '(1 row)',
                                  flag='1')
        self.logger.info('----设置参数log_destination的值为stderr,csvlog----')
        msg1 = self.sh_primy.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'log_destination=\'stderr,csvlog\'')
        self.logger.info(msg1)
        self.logger.info('----查看log_destination修改后的值为stderr,csvlog----')
        sql_cmd2 = 'show log_destination;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_destination', 'stderr,csvlog',
                                  '(1 row)', flag='1')
        self.logger.info('-------预删除csv日志文件-------')
        rm_log_file = self.log_path + "/*csv"
        execute_cmd3 = f'rm -rf {rm_log_file}'
        msg3 = self.primaryRoot.sh(execute_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('-------重启数据库生成日志文件-------')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gs_om -t stop && gs_om -t start'
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('-------查看是否生成日志文件-------')
        excute_cmd5 = f'ls -l {self.log_path} |grep "csv" |wc -l'
        msg5 = self.primaryRoot.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.assertTrue(int(msg5) >= 1)

    def tearDown(self):
        self.logger.info('-------恢复配置，清理环境-------')
        msg1 = self.sh_primy.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f'log_destination=\'stderr\'')
        self.logger.info(msg1)
        self.logger.info('-------查看log_destination是否恢复为stderr-------')
        sql_cmd2 = 'show log_destination;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_destination', 'stderr', '(1 row)',
                                  flag='1')
        self.logger.info('-------恢复log_directory路径，清理环境-------')
        recover_cmd = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
                      f'"log_directory=\'{path_return}\'";'
        recover_msg = self.userNode.sh(recover_cmd).result()
        self.logger.info(recover_msg)
        self.logger.info('-------查看配置是否恢复-------')
        check_path_cmd = 'show log_directory;'
        check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
        self.logger.info(check_path_msg)
        self.assertTrue(macro.PG_LOG_PATH in path_return)
        self.logger.info('-------清理生成的日志文件-------')
        clear_cmd = f'rm -rf  {self.log_path};ls {self.log_path}'
        clear_msg = self.primaryRoot.sh(clear_cmd).result()
        self.logger.info(clear_msg)
        self.assertTrue(clear_msg.find('No such file or directory') > -1)
        self.logger.info('-------删除生成的日志文件-------')
        rm_log_file = self.log_path + "/*csv"
        execute_cmd3 = f'rm -rf {rm_log_file}'
        msg3 = self.primaryRoot.sh(execute_cmd3).result()
        self.logger.info(msg3)
        excute_cmd4 = f'ls -l {self.log_path} |grep "csv" |wc -l'
        msg4 = self.primaryRoot.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue(msg4.find('No such file or directory'))
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0004 finish--')
