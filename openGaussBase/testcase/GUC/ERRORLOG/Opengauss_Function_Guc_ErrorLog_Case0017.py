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
Case Name   : 设置参数log_filename值为postgresql-Y-m-d_HMS.log
Description :
    1.gs_guc reload -N all -I all -c "log_filename='postgresql-Y-m-d_HMS.log'"
    2.重启数据库后查看关于数据库重启的日志
Expect      :
    1.设置成功
    2.生成的日志'postgresql-%Y-%m-%d.log格式，且日志内容与数据库重启相关
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Errorlog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('==Opengauss_Function_Guc_ErrorLog_Case0017 start==')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')

    def test_errorlog(self):
        self.logger.info('--------------查看logging_collector默认值----------')
        sql_cmd0 = 'show logging_collector;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'logging_collector', 'on', '(1 row)',
                                flag='1')
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
                      f'{self.log_path}\'"'
        execute_msg4 = self.userNode.sh(excute_cmd0).result()
        self.logger.info(execute_msg4)
        self.logger.info('----查看日志路径----')
        sql_execute = f'show log_directory;'
        msg_log = self.sh_primy.execut_db_sql(sql_execute)
        self.logger.info(msg_log)
        self.common.equal_sql_mdg(msg_log, 'log_directory', self.log_path,
                                '(1 row)', flag='1')
        self.logger.info('---------设置log_filename的值---------')
        xcute_cmd2_2 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                       f'{macro.DB_INSTANCE_PATH} -c ' \
                       f'"log_filename=\'wfte-Y-m-d_HMS.log\'"'
        msg1_2 = self.userNode.sh(xcute_cmd2_2).result()
        self.logger.info(msg1_2)
        logfile = self.log_path + '/*'
        self.logger.info('-------预删除日志文件-------')
        excute_cmd2_3 = f'rm -rf  {logfile}'
        msg2_3 = self.primaryRoot.sh(excute_cmd2_3).result()
        self.logger.info(msg2_3)
        self.logger.info('-------重启数据库生成日志文件-------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_om -t stop && gs_om -t start'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('-------查看是否生成日志文件-------')
        excute_cmd4 = f'ls -l {self.log_path}'
        msg4 = self.primaryRoot.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertFalse(msg4 == 'wfte-Y-m-d_HMS.log')
        self.logger.info('-------删除生成的日志-------')
        excute_cmd5 = f'rm -rf {self.log_path};ls {self.log_path}'
        msg5 = self.primaryRoot.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.assertTrue('No such file or directory' in msg5)

    def tearDown(self):
        self.logger.info('-----恢复log_filename的默认值-----')
        rec_name_cmd = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
            f'all -c ' \
            f'"log_filename=\'postgresql-%Y-%m-%d_%H%M%S.log\'"'
        rec_name_msg = self.userNode.sh(rec_name_cmd).result()
        self.logger.info(rec_name_msg)
        self.logger.info('-------查看log_filename是否恢复-------')
        sql_cmd1 = 'show log_filename;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        msg1_list = msg1.splitlines()[-2].split("_")
        self.logger.info(msg1_list)
        self.assertTrue(len(msg1_list) == 2)
        self.logger.info('-------恢复配置，清理环境-------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{path_return}\'"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.logger.info('-------查看log_directory是否恢复-------')
        sql_cmd3 = 'show log_directory;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        msg_return = msg3.splitlines()[2].strip()
        self.logger.info(msg_return)
        self.assertTrue(macro.PG_LOG_PATH in msg_return)
        self.logger.info('-------清理生成的日志文件-------')
        excute_cmd4 = f'rm -rf  {self.log_path};ls {self.log_path}'
        msg4 = self.primaryRoot.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue(msg4.find("No such file or directory") > -1)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0017 finish--')
