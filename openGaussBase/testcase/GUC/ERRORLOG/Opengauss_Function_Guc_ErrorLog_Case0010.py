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
Case Name   : 设置参数log_directory的值为合法路径
Description :
    1.logging_collector设置为on时,配置log路径合法:gs_guc reload -N all -I all
    -c "log_directory=''$path"  (path为初始用户有读写权限的路径)
    2.查看值是否被修改：show log_directory；
    3.重启数据库后查看$path下是否有日志文件生成
Expect      :
    1.默认值为安装数据库时配置的路径
    2.返回值为步骤1所配置
    3.数据库重启成功后在$path下，查看到postgresql命名的日志，日志信息可看到数据库重启相关的
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0010 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
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
        excute_cmd0 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{self.log_path}\'"'
        execute_msg0 = self.userNode.sh(excute_cmd0).result()
        self.logger.info(execute_msg0)
        self.logger.info('----查看日志路径----')
        sql_execute = f'show log_directory;'
        msg_log = self.sh_primy.execut_db_sql(sql_execute)
        self.logger.info(msg_log)
        self.common.equal_sql_mdg(msg_log, 'log_directory', self.log_path,
                                '(1 row)', flag='1')
        self.logger.info('--------------查看logging_collector默认值----------')
        sql_cmd0 = 'show logging_collector;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'logging_collector', 'on', '(1 row)',
                                flag='1')
        self.logger.info('-------重启数据库生成日志文件-------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gs_om -t stop && gs_om -t start'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('-------查看是否生成日志文件-------')
        excute_cmd4 = f'ls -l {self.log_path} |grep "^-" |wc -l'
        msg4 = self.primaryRoot.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue(int(msg4) >= 1)

    def tearDown(self):
        self.logger.info('-------恢复log_directory路径，清理环境-------')
        recover_cmd = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c ' \
                      f'"log_directory=\'{path_return}\'"'
        self.logger.info(recover_cmd)
        recover_msg = self.userNode.sh(recover_cmd).result()
        self.logger.info(recover_msg)
        self.logger.info('-------查看配置是否恢复-------')
        check_path_cmd = 'show log_directory;'
        check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
        self.logger.info(check_path_msg)
        self.assertTrue(macro.PG_LOG_PATH in path_return)
        self.logger.info('-------清理生成的日志文件-------')
        excute_cmd3 = f'rm -rf  {self.log_path};ls {self.log_path}'
        msg3 = self.primaryRoot.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find('No such file or directory') > -1)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0010 finish--')