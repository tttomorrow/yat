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
Case Type   : Separation_policy
Case Name   : 设置密码不可重用天数为0
Description :
    1.登录数据库gsql -d $database -p $port -r
    2.创建用户user02,create user user001 with password "$PASSWORD1";
    3.设置不可重用天数默认值为0天，gs_guc reload -D $PATH -c "password_reuse_time=0“
    4.修改2次用户密码，第2次将用户密码改回PASSWORD1
Expect      :
    1.登录数据库成功
    2.创建成功
    3.设置成功
    4.第四次将用户密码改回原密码成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Security_Policy_Case0064 start')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password = ''.join(reversed(macro.COMMON_PASSWD))
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_policy(self):
        self.logger.info("---------预置条件：password_reuse_max=0-----")
        sql_cmd0 = 'show password_reuse_max;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'password_reuse_max', '0', '(1 row)',
                                flag='1')
        self.logger.info('--------修改参数password_reuse_time值为0-------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "password_reuse_time=0"'
        self.logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg1)
        sql_cmd1 = 'show password_reuse_time;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'password_reuse_time', '0', '(1 row)',
                                flag='1')
        self.logger.info('----------创建用户user02 ------')
        sql_cmd2 = f'create user user02 with password \'' \
                   f'{macro.COMMON_PASSWD}\';'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertTrue(msg2.find("CREATE ROLE") > -1)
        self.logger.info("修改2次用户密码，第2次将用户密码改回原密码")
        new_password = macro.COMMON_PASSWD + "qaz"
        sql_cmd3 = f'alter user user02 with password \'{new_password}\';'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find("ALTER ROLE") > -1)
        sql_cmd4 = f'alter user user02 with password \'' \
                   f'{macro.COMMON_PASSWD}\';'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.assertTrue(msg4.find('ALTER ROLE') > -1)

    def tearDown(self):
        self.logger.info('---------清理环境,恢复配置---------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all ' \
                      f'-c "password_reuse_time=60"'
        self.logger.info(excute_cmd2)
        msg1 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg1)
        sql_cmd1 = 'show password_reuse_time;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'password_reuse_time', '60', '(1 row)',
                                flag='1')
        sql_cmd3 = 'drop user user02;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find('DROP ROLE') > -1)
        self.logger.info('Opengauss_Function_Security_Policy_Case0064 finish')
