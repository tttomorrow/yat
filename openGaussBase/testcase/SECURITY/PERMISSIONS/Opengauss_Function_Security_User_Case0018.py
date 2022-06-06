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
Case Type   : security-user
Case Name   : 主节点账户手动锁定，备节点账户仍然可以连接
Description :
    1.创建用户
    create user user001 password '$password';
    2.主机：锁定账户user001，连接数据库
    alter user user001 lock;
    gsql -d $database -p $port -U user001 -W $password
    3.备机：user001用户使用正确的密码连接数据库
    gsql -d $database -p $port -U user001 -W $password
    4.清理资源：删除用户
Expect      :
    1.创建成功
    2.user001账户被锁定,连接失败
    3.连接成功
    4.清理资源成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common

primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-----Opengauss_Function_Security_User_Case0018 start-----')
        self.common = Common()
        self.constant = Constant()
        self.userNode = Node('PrimaryDbUser')
        self.standbyNode = Node('Standby1DbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.com_user = 'com_security_user_0018'

    def test_lockuser(self):
        text = '-----step1: 创建用户,except:创建成功-----'
        self.logger.info(text)
        sql_cmd1 = f'create user {self.com_user} password ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        self.logger.info(sql_cmd1)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        assert_1 = self.constant.CREATE_ROLE_SUCCESS_MSG in msg1
        self.assertTrue(assert_1, '执行失败：' + text)

        text = '-----step2: 主机：锁定账户user001，连接数据库' \
               'except: user001账户被锁定,连接失败-----'
        self.logger.info(text)
        sql_cmd2 = f'alter user {self.com_user} account lock;'
        self.logger.info(sql_cmd2)
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        excute_cmd3 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} ' \
                      f'-p {self.userNode.db_port} ' \
                      f'-U {self.com_user} ' \
                      f'-W {macro.COMMON_PASSWD}'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        assert_2 = self.constant.ALTER_ROLE_SUCCESS_MSG in msg2 and  \
                   self.constant.ACCOUNT_LOCKED_TYPE in msg3
        self.assertTrue(assert_2, '执行失败：' + text)

        text = '-----step3: 备机：user001用户使用正确的密码连接数据库,' \
               'except: 连接成功-----'
        self.logger.info(text)
        excute_cmd4 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.standbyNode.db_name} ' \
                      f'-p {self.standbyNode.db_port} ' \
                      f'-U {self.com_user} ' \
                      f'-W {macro.COMMON_PASSWD} ' \
                      f'-c "\\du"'
        self.logger.info(excute_cmd4)
        msg4 = self.standbyNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        assert_4 = 'List of roles' in msg4
        self.assertTrue(assert_4, '执行失败：' + text)

    def tearDown(self):
        text = '------step4:清理资源：删除用户，expect:清理资源成功-------'
        self.logger.info(text)
        sql_cmd1 = f'drop user {self.com_user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, msg1)
        self.logger.info(
            '----Opengauss_Function_Security_User_Case0018 finish----')