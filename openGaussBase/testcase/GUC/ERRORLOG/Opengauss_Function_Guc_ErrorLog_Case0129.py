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
Case Name   : 查看参数log_disconnections的默认值为off
Description :
    1.连接数据库，查看log_connections默认参数：show log_disconnections;
    2.重启数据库生成日志文件
    3.登录并退出数据库，后查看pg_log日志：tail -f postgresql-xxx-xx-xx.log
Expect      :
    1.返回值：off
    2.生成名为postgresql的日志文件
    3.日志中未记录客户端结束连接信息
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
        Logger.info('Opengauss_Function_Guc_ErrorLog_Case0129 start')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')

    def test_errorlog(self):
        Logger.info('-------查看log_directory默认路径------')
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
        execute_msg0 = self.userNode.sh(excute_cmd0).result()
        Logger.info(execute_msg0)
        sql_cmd1 = 'show log_disconnections;'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        Logger.info(sql_msg1)
        self.common.equal_sql_mdg(sql_msg1, 'log_disconnections', 'off',
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
        Logger.info('-------登录、退出数据库，查看日志是否有断开连接的记录-------')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p' \
                      f' {self.userNode.db_port} -c "\q"'
        excute_msg4 = self.userNode.sh(excute_cmd4).result()
        Logger.info(excute_msg4)
        excute_cmd4 = f'cat {self.log_path}/postgresql*'
        excute_msg4 = self.userNode.sh(excute_cmd4).result()
        Logger.info(excute_msg4)
        self.assertFalse(excute_msg4.find('LOG:  disconnection:') > -1)

    def tearDown(self):
        Logger.info('-------恢复配置，清理环境-------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                      f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                      f'{path_return}\'"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg1)
        Logger.info('-------查看log_directory是否恢复-------')
        sql_cmd2 = 'show log_directory;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        Logger.info(msg2)
        msg_return = msg2.splitlines()[2].strip()
        Logger.info(msg_return)
        self.assertTrue(macro.PG_LOG_PATH in msg_return)
        Logger.info('-------清理生成的日志文件------')
        excute_cmd3 = f'rm -rf {self.log_path};ls {self.log_path}'
        Logger.info(excute_cmd3)
        msg3 = self.primaryRoot.sh(excute_cmd3).result()
        Logger.info(msg3)
        self.assertTrue(msg3.find("No such file or directory") > -1)
        Logger.info('--Opengauss_Function_Guc_ErrorLog_Case0129 finish--')
