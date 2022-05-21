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
Case Name   : 设置参数log_destination的值为stderr,csvlog,syslog,查看日志文件
Description :
    1.设置参数log_destination的值：gs_guc reload -N all -I all -c
    "log_destination='stderr,csvlog,syslog'"，查看设置结果：show log_destination;
    2.执行重启数据库操作：gs_om - t stop && gs_om -t start
    3.查看是否/var/log路径下生成postgresql日志文件，$gaussdb_log/$username/pg_log/下
    生成.scv的log日志,且日志打印在屏幕
Expect      :
    1.参数设置成功，返回值为csvlog,stderr,syslog
    2.重启数据库完成
    3.在 /var/log路径下生成postgresql日志文件，$gaussdb_log/$username/pg_log/下生
    成.scv的log日志,且日志打印在屏幕
History     :
"""
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0005 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
    
    def test_errorlog(self):
        self.logger.info('---------查看log_destination默认值--------')
        sql_cmd0 = 'show log_destination;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'log_destination', 'stderr', '(1 row)',
                                  flag='1')
        self.logger.info('--设置参数log_destination的值为stderr,syslog,csvlog--')
        msg1 = self.sh_primy.execute_gsguc('reload',
                                self.constant.GSGUC_SUCCESS_MSG,
                                'log_destination=\'stderr,syslog,csvlog\'')
        self.logger.info(msg1)
        self.logger.info('----查看log_destination修改后的值----')
        sql_cmd2 = 'show log_destination;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_destination',
                                  'stderr,syslog,csvlog', '(1 row)', flag='1')
        self.logger.info('-------配置文件中添加代码-------')
        excute_cmd3_1 = f'echo "local0.*  /var/log/postgresql" >> ' \
            f'/etc/*syslog.conf'
        msg3_1 = self.primaryRoot.sh(excute_cmd3_1).result()
        self.logger.info(msg3_1)
        excute_cmd3_2 = 'service rsyslog restart'
        msg3_2 = self.primaryRoot.sh(excute_cmd3_2).result()
        self.logger.info(msg3_2)
        self.logger.info('-------重启数据库生成日志文件-------')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
            f'gs_om -t stop && gs_om -t start'
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('-------查看是否生成日志文件-------')
        excute_cmd5 = f'ls /var/log/postgresql'
        msg5 = self.primaryRoot.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.assertTrue('/var/log/postgresql' in msg5)
        self.assertFalse('No such file or directory' in msg5)
    
    def tearDown(self):
        self.logger.info('-------恢复配置，清理环境-------')
        msg1 = self.sh_primy.execute_gsguc('reload',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'log_destination=\'stderr\'')
        self.logger.info(msg1)
        self.logger.info('-------查看log_destination是否恢复为stderr-------')
        sql_cmd2 = 'show log_destination;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.logger.info('-------删除生成的日志文件-------')
        execute_cmd3_1 = 'rm -rf /var/log/postgresql'
        msg3_1 = self.primaryRoot.sh(execute_cmd3_1).result()
        self.logger.info(msg3_1)
        execute_cmd3_2 = 'sed -i \'$d\' /etc/*syslog.conf'
        msg3_2 = self.primaryRoot.sh(execute_cmd3_2).result()
        self.logger.info(msg3_2)
        execute_cmd3_3 = 'service rsyslog restart'
        msg3_3 = self.primaryRoot.sh(execute_cmd3_3).result()
        self.logger.info(msg3_3)
        self.logger.info('-------检查日志文件被删除-------')
        execute_cmd4 = 'ls /var/log/postgresql'
        msg4 = self.primaryRoot.sh(execute_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('-------检查配置文件中内容被删除-------')
        execute_cmd5 = 'cat /var/log/postgresql |grep "local0.*  ' \
                       '/var/log/postgresql"'
        msg5 = self.primaryRoot.sh(execute_cmd5).result()
        self.logger.info(msg5)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0005 finish--')
