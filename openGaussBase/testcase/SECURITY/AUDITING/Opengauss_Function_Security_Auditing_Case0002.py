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
Case Type   : security-auditing
Case Name   : 数据库运行期间关闭审计总开关audit_enabled的值会立即生效
Description :
    步骤 1.修改审计总开关audit_enabled的值为off,gs_guc reload -N all -I all -c "audit_enabled=off"，无需重启数据库
    步骤 2.登录数据库，查看审计日志SELECT * FROM pg_query_audit('$start_time','$end_time');
Expect      :
    步骤 1.修改成功
    步骤 2.在写定的时间内，查不到审计记录
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '------Opengauss_Function_Security_Auditing_Case0002 start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        execute_cmd = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "audit_enabled=off"'
        msg = self.userNode.sh(execute_cmd).result()
        self.logger.info(msg)

        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd1 = 'select current_database();'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)

        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        self.logger.info(end_time)
        sql_cmd2 = f'select * from pg_query_audit(\'{start_time}\',' \
                   f'\'{end_time}\')where type=\'user_logout\';'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd2}"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertFalse(msg2.find('user_logout') > -1)

    def tearDown(self):
        self.logger.info("-------------恢复默认配置-------------")
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f' gs_guc reload -N all -I all -c "audit_enabled=on"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0002 end----')
