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
Case Type   : Separation_rights
Case Name   : 三权分立后系统管理员失去AUDITADMIN属性
Description :
    1.开启三权分立，设置enableSeparationOfDuty=on，重启数据库
    2.sysadmin01用户登录数据库SELECT * FROM pg_query_audit('2021-01-11 08:00:00',
    '2021-01-11 23:47:33');
Expect      :
    1.参数设置成功
    2.无法查询审计记录，peimission denied
History     :
"""
import time
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-----Opengauss_Function_Security_Separation_Case0030 start------')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_policy(self):
        self.logger.info('--------设置参数enableSeparationOfDuty为on--------')
        excute_cmd1 = f' source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH} -c' \
                      f' "enableSeparationOfDuty=on";' \
                      f'gs_om -t stop && gs_om -t start'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('----------创建管理员用户------------')
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd2 = f'CREATE USER sysadmin01 WITH SYSADMIN password ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.logger.info('-------------查看审计日志------------')
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql("SELECT sysdate;")
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\');'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U sysadmin01 -W ' \
                      f'{macro.COMMON_PASSWD} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(
            msg3.find('ERROR:  permission denied to query audit') > -1)

    def tearDown(self):
        self.logger.info('-----------清理环境-----------')
        sql_cmd1 = f'drop user sysadmin01;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH} -c ' \
                      f'"enableSeparationOfDuty=off";' \
                      f'gs_om -t stop && gs_om -t start'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.logger.info(
            '----Opengauss_Function_Security_Separation_Case0030 finish----')
