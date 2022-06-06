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
Case Type   : security-policy
Case Name   : 设置密码不可重用次数设置为1
Description :
    1.登录数据库gsql -d $database -p $port -r
    2.gs_guc reload -N all -I all -c "password_reuse_max = 1"，
    3.创建用户user002,create user user002 with password "{macro.COMMON_PASSWD}";
    4.修改用户密码，alter user user002 with passwd "{macro.COMMON_PASSWD}"
    5.再次修改用户密码，alter user user002 with passwd "{macro.COMMON_PASSWD}"
    6.删除用户
Expect      :
    1.登录数据库成功
    2.show password_reuse_max ;显示结果为1
    3.创建成功
    4.修改成功
    5.修改成功
    6.删除成功
History     :
"""
import random
import string
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_Security_Policy_Case0067 start----')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        str_lst = []
        for j in range(10):
            str_lst.append(random.choice(string.ascii_lowercase))
        part_lst = str_lst[:6]
        str_passwd = "".join(part_lst)
        self.new_password = str_passwd.capitalize() + "@" + "989"
        self.Constant = Constant()

    def test_policy(self):
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "password_reuse_max=1"'
        msg0 = self.userNode.sh(excute_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = 'show password_reuse_max;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'password_reuse_max', '1', '(1 row)',
                                  flag="1")
        sql_cmd2 = f'create user user002 with password ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'alter user user002 with password \'' \
                   f'{self.new_password}\';' \
                   f'alter user user002 with password \'' \
                   f'{macro.COMMON_PASSWD}\';'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertTrue('CREATE ROLE' in msg2 and 'ALTER ROLE'
                        in msg2 and 'ALTER ROLE' in msg2)

    def tearDown(self):
        logger.info('-----------恢复配置-----------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c "password_reuse_max=0"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        sql_cmd2 = 'show password_reuse_max;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'password_reuse_max', '0', '(1 row)',
                                  flag="1")
        msg3 = self.sh_primy.execut_db_sql("drop user user002;")
        logger.info(msg3)
        logger.info(
            '-----Opengauss_Function_Security_Policy_Case0067 finish------')
