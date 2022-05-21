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
Case Name   : 修改参数syslog_ident的值为合法字符串
Description :
    1.修改参数syslog_ident的值为tpcc:gs_guc reload -N all -I all -c
    "syslog_ident='tpcc'"
    2.重启数据库，生成日志文件于/var/log/下，查看日志日志消息的标识
Expect      :
    1.返回值：postgres
    2.日志消息的标识为tpcc
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Errorlog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0051 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info("---------设置参数log_destination的值为syslog-----")
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_destination=\'syslog\'"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-------查看log_destination修改后的值为syslog-------')
        sql_cmd2 = 'show log_destination;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_destination', 'syslog', '(1 row)',
                                  flag='1')
        self.logger.info('-------配置文件中添加代码-------')
        excute_cmd3 = f'echo "local5.*  /var/log/postgresql5" >> ' \
                      f'/etc/*syslog.conf;service rsyslog restart'
        msg3 = self.primaryRoot.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('----修改参数syslog_facility,syslog_ident----')
        excute_cmd4 = f'source {self.DB_ENV_PATH};gs_guc reload -N all -I ' \
                      f'all -c "syslog_facility=local5";' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"syslog_ident=\'pg_sign_table\'"'
        self.logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('--------查看参数是否修改成功---------')
        check_cmd1 = 'show syslog_facility;'
        check_msg1 = self.sh_primy.execut_db_sql(check_cmd1)
        self.logger.info(check_msg1)
        self.common.equal_sql_mdg(check_msg1, 'syslog_facility', 'local5',
                                  '(1 row)', flag='1')
        check_cmd2 = 'show syslog_ident;'
        check_msg2 = self.sh_primy.execut_db_sql(check_cmd2)
        self.logger.info(check_msg2)
        self.common.equal_sql_mdg(check_msg2, 'syslog_ident', 'pg_sign_table',
                                  '(1 row)', flag='1')
        self.logger.info('-------重启数据库生成日志文件-------')
        excute_cmd5 = f'source {self.DB_ENV_PATH};' \
                      f'gs_om -t stop && gs_om -t start'
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.logger.info('-------查看是否生成日志文件-------')
        excute_cmd6 = f'ls /var/log/postgresql5'
        msg6 = self.primaryRoot.sh(excute_cmd6).result()
        self.logger.info(msg6)
        self.assertTrue(msg6.find('/var/log/postgresql5') > -1)
        self.logger.info('-------查看日志内容中的标示符-------')
        excute_cmd7 = f'cat /var/log/postgresql5'
        msg7 = self.primaryRoot.sh(excute_cmd7).result()
        self.logger.info(msg7)
        self.assertTrue(msg7.count('pg_sign_table') >= 2)

    def tearDown(self):
        self.logger.info('-------恢复配置，清理环境-------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"syslog_facility=local0";' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"syslog_ident=\'postgres\'"'
        self.logger.info(excute_cmd0)
        msg0 = self.userNode.sh(excute_cmd0).result()
        self.logger.info(msg0)
        self.logger.info('-------查看参数syslog_facility值恢复-------')
        sql_cmd0_1 = 'show syslog_facility;'
        msg0_1 = self.sh_primy.execut_db_sql(sql_cmd0_1)
        self.logger.info(msg0_1)
        self.common.equal_sql_mdg(msg0_1, 'syslog_facility', 'local0',
                                  '(1 row)',
                                  flag='1')
        excute_cmd1 = f' source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"log_destination=\'stderr\'"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-------查看log_destination是否恢复为stderr-------')
        sql_cmd2 = 'show log_destination;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_destination', 'stderr', '(1 row)',
                                  flag='1')
        self.logger.info('-------删除生成的日志文件-------')
        execute_cmd3_1 = 'rm -rf /var/log/postgresql5'
        msg3_1 = self.primaryRoot.sh(execute_cmd3_1).result()
        self.logger.info(msg3_1)
        execute_cmd3_2 = 'sed -i \'$d\' /etc/*syslog.conf'
        msg3_2 = self.primaryRoot.sh(execute_cmd3_2).result()
        self.logger.info(msg3_2)
        execute_cmd3_3 = 'service rsyslog restart'
        msg3_3 = self.primaryRoot.sh(execute_cmd3_3).result()
        self.logger.info(msg3_3)
        self.logger.info('-------检查日志文件被删除-------')
        execute_cmd4 = 'ls /var/log/postgresql5'
        msg4 = self.primaryRoot.sh(execute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue(msg4.find('No such file or directory') > -1)
        self.logger.info('-------检查配置文件中内容被删除-------')
        execute_cmd5 = 'cat /etc/*syslog.conf |grep "local5.*  ' \
                       '/var/log/postgresql5"'
        msg5 = self.primaryRoot.sh(execute_cmd5).result()
        self.logger.info(msg5)
        self.assertFalse(msg5.find('local5.*  /var/log/postgresql5') > -1)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0051 finish--')
