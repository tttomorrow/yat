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
Case Name   : 设置参数log_destination的值为syslog,查看日志文件
Description :
    1.设置参数log_destination的值为syslog：gs_guc reload -N all -I all -c
    "log_destination='syslog'"，查看参数设置结果：show log_destination;
    2.操作系统后台服务配置文件中添加代码local0.*  /var/log/postgresql :文件路
    径v：/etc/rsyslog.conf (或者syslog.conf)
    3.重启服务：service rsyslog restart
    4.执行重启数据库操作：gs_om - t stop && gs_om -t start
    5.查看/var/log路径下是否生成postgresql日志文件
Expect      :
    1.参数设置成功，返回值为syslog
    2.配置文件修改完成
    3.服务重启成功
    4.数据库重启成功、
    5.在/var/log路径下生成postgresql日志文件，日志文件中记录数据库重启的相关信息
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Errorlog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0002 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
    
    def test_errorlog(self):
        self.logger.info('----------查看log_destination默认值---------')
        sql_cmd0 = 'show log_destination;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'log_destination', 'stderr', '(1 row)',
                                  flag='1')
        self.logger.info('-----设置参数log_destination的值为syslog-----')
        msg1 = self.sh_primy.execute_gsguc('reload',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'log_destination=\'syslog\'')
        self.logger.info(msg1)
        self.logger.info('-------查看log_destination修改后的值为syslog-------')
        sql_cmd2 = 'show log_destination;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'log_destination', 'syslog', '(1 row)',
                                  flag='1')
        self.logger.info('-------配置文件中添加代码-------')
        excute_cmd3 = f'echo "local0.*  /var/log/wf_postgresql" >> ' \
            f'/etc/*syslog.conf;service rsyslog restart'
        msg3 = self.primaryRoot.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('-------重启数据库生成日志文件-------')
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
            f'gs_om -t stop && gs_om -t start'
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('-------查看是否生成日志文件-------')
        excute_cmd5 = 'ls /var/log/wf_postgresql'
        msg5 = self.primaryRoot.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.assertTrue('/var/log/wf_postgresql' in msg5 and
                        'No such file or directory' not in msg5)
    
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
        execute_cmd3_1 = 'rm -rf /var/log/wf_postgresql'
        msg3_1 = self.primaryRoot.sh(execute_cmd3_1).result()
        self.logger.info(msg3_1)
        execute_cmd3_2 = 'sed -i \'$d\' /etc/*syslog.conf'
        msg3_2 = self.primaryRoot.sh(execute_cmd3_2).result()
        self.logger.info(msg3_2)
        execute_cmd3_3 = 'service rsyslog restart'
        msg3_3 = self.primaryRoot.sh(execute_cmd3_3).result()
        self.logger.info(msg3_3)
        self.logger.info('-------检查日志文件被删除-------')
        execute_cmd4 = 'ls /var/log/wf_postgresql'
        msg4 = self.primaryRoot.sh(execute_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('-------检查配置文件中内容被删除-------')
        execute_cmd5 = 'tail -n 1 /etc/*syslog.conf'
        msg5 = self.primaryRoot.sh(execute_cmd5).result()
        self.logger.info(msg5)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0002 finish--')
