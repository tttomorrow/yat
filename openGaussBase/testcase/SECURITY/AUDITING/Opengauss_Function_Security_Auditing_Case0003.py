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
Case Type   : security-auditing
Case Name   : 开启用户登录、退出的审计功能，audit_login_logout默认值7
Description :
    步骤 1.设置gs_guc reload -N all -I all -c "audit_login_logout=7"
    步骤 2.正确的用户、密码，登录数据库；
    步骤 3.错误的用户、密码，登录数据库
    步骤 4.创建用户：create user user03 with password "{macro.COMMON_PASSWD}"；
    步骤 5.删除用户：drop user user03 ;
    步骤 6.查看审计日志select * from pg_query_audit('{start_time}','{end_time}')
    where type like 'login%' or type like '%logout%' and username = 'user03';
    时间设在最接近登录数据库的时间
Expect      :
    步骤 1.设置成功，show audit_login_logout;返回7
    步骤 2.登录成功
    步骤 3.登录失败
    步骤 4.创建成功
    步骤 5.删除成功
    步骤 6.只查询到登录成功、失败和注销的记录
History     :
"""
import unittest
from time import sleep

from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Logger = Logger()


class Auditing(unittest.TestCase):
    def setUp(self):
        Logger.info('Opengauss_Function_Security_Auditing_Case0003 start')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
    
    def test_security(self):
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        sql_cmd1 = f'show audit_login_logout;' \
            f'create user user03 with password ' \
            f'\'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        msg1_list = msg1.splitlines()
        Logger.info(msg1_list)
        if msg1_list[0].strip() == "audit_login_logout" and msg1_list[
            2].strip() != '7':
            excute_set1 = f'source {self.DB_ENV_PATH};' \
                f'gs_guc reload -N all -I all -c ' \
                f'"audit_login_logout=7"'
            set_msg1 = self.userNode.sh(excute_set1).result()
            Logger.info(set_msg1)
            sql_set1 = f'show audit_login_logout;'
            sql_msg1 = self.sh_primy.execut_db_sql(sql_set1)
            self.common.equal_sql_mdg(sql_msg1, 'audit_login_logout', '7',
                                      '(1 row)', flag='1')
        new_password2 = macro.COMMON_PASSWD.lower() + "qaz"
        sleep(30)
        login_success_cmd = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U user03 -W ' \
            f'"{macro.COMMON_PASSWD}" -c "\\q";'
        Logger.info(login_success_cmd)
        login_success_msg = self.userNode.sh(login_success_cmd).result()
        self.assertTrue(login_success_msg == '')
        sleep(3)
        login_fail_cmd = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U user03 -W ' \
            f'"{new_password2}" -c "\\q"'
        Logger.info(login_fail_cmd)
        login_fail_msg = self.userNode.sh(login_fail_cmd).result()
        Logger.info(login_fail_msg)
        self.assertIn('Invalid username/password,login denied', login_fail_msg)
        sleep(30)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',' \
            f'\'{end_time}\');'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd3}"'
        Logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        Logger.info(msg3)
        self.assertTrue(
            msg3.find('failed,authentication for user(user03)failed') > -1)
        self.assertTrue(msg3.find('success,the current user is:user03') > -1)
        self.assertTrue(msg3.find('user_logout') > -1)
    
    def tearDown(self):
        sql_cmd1 = 'drop user user03;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        Logger.info(msg1)
        Logger.info('Opengauss_Function_Security_Auditing_Case0003 end')
