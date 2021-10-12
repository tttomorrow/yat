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
Case Name   : 设置参数syslog_facility值为local3
Description :
    1.设置参数syslog_facility值为local1：gs_guc reload -N all -I all -c
    "syslog_facility=local3"
    2.修改系统配置文件，/etc/rsyslog.conf文件：local1.* /var/log/postgresql3,
    重启服务生效：service rsyslog restart
    3.重启数据库，生成日志文件于/var/log/下，查看日志文件
Expect      :
    1.参数设置成功
    2.修改完配置文件，服务重启成功
    3./var/log下生成postgresql1日志文件，记录数据库重启的相关日志信息
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
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0044 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('--------------查看log_destination默认值----------')
        sql_cmd0 = 'show log_destination;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'log_destination', 'stderr', '(1 row)',
                                flag='1')
        self.logger.info('---------设置参数log_destination的值为syslog-----')
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
        excute_cmd3 = f'echo "local3.*  /var/log/postgresql3" >> ' \
                      f'/etc/*syslog.conf;service rsyslog restart'
        msg3 = self.primaryRoot.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('-----设置参数l设置参数syslog_facility值为local3----')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"syslog_facility=local3"'
        self.logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('-------重启数据库生成日志文件-------')
        excute_cmd5 = f'source {self.DB_ENV_PATH};' \
                      f'gs_om -t stop && gs_om -t start'
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.logger.info('-------查看是否生成日志文件-------')
        excute_cmd6 = f'ls /var/log/postgresql3'
        msg6 = self.primaryRoot.sh(excute_cmd6).result()
        self.logger.info(msg6)
        self.assertTrue(msg6.find('/var/log/postgresql3') > -1)

    def tearDown(self):
        self.logger.info('-------恢复配置，清理环境-------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"syslog_facility=local0"'
        self.logger.info(excute_cmd0)
        msg0 = self.userNode.sh(excute_cmd0).result()
        self.logger.info(msg0)
        self.logger.info('-------查看参数syslog_facility值恢复-------')
        sql_cmd0_1 = 'show syslog_facility;'
        msg0_1 = self.sh_primy.execut_db_sql(sql_cmd0_1)
        self.logger.info(msg0_1)
        self.common.equal_sql_mdg(msg0_1, 'syslog_facility', 'local0', '(1 row)',
                                flag='1')
        excute_cmd1 = f'''
            source {self.DB_ENV_PATH};
            gs_guc reload -N all -I all -c "log_destination='stderr'"
            '''
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
        execute_cmd3_1 = 'rm -rf /var/log/postgresql3'
        msg3_1 = self.primaryRoot.sh(execute_cmd3_1).result()
        self.logger.info(msg3_1)
        execute_cmd3_2 = 'sed -i \'$d\' /etc/*syslog.conf'
        msg3_2 = self.primaryRoot.sh(execute_cmd3_2).result()
        self.logger.info(msg3_2)
        execute_cmd3_3 = 'service rsyslog restart'
        msg3_3 = self.primaryRoot.sh(execute_cmd3_3).result()
        self.logger.info(msg3_3)
        self.logger.info('-------检查日志文件被删除-------')
        execute_cmd4 = 'ls /var/log/postgresql3'
        msg4 = self.primaryRoot.sh(execute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue(msg4.find('No such file or directory') > -1)
        self.logger.info('-------检查配置文件中内容被删除-------')
        execute_cmd5 = 'cat /etc/*syslog.conf |grep "local3.*  ' \
                       '/var/log/postgresql3"'
        msg5 = self.primaryRoot.sh(execute_cmd5).result()
        self.logger.info(msg5)
        self.assertFalse(msg5.find('local3.*  /var/log/postgresql3') > -1)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0044 finish--')
