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
Case Type   : GUC
Case Name   : 系统管理员使用set命令设置synchronous_commit参数值为2
Description :
        1.查询synchronous_commit默认值
        2.创建用户
        3.系统管理员使用set命令修改参数synchronous_commit为2,
        4.重新连接数据库，查看参数值
        5.删除用户
Expect      :
        1.单机环境显示默认值为off，双机为on
        2.用户创建成功
        3.修改成功
        4.单机环境显示默认值为off，双机为on
        5.删除成功
History     :
"""
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('PrimaryDbUser')
constant = Constant()

class GUC_SC(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Guc_Synchronous_Commit_Case0005开始执行-----------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_synchronous_commit(self):
        # 查看参数默认值且创建系统管理员用户
        sql_cmd1 = commonsh.execut_db_sql(f'''show synchronous_commit;
                                       drop user if exists test1_sys005 cascade;
                                       create user test1_sys005 with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        flag = (constant.SYNCHRONOUS_COMMIT_DEFAULT[0] in sql_cmd1 or constant.SYNCHRONOUS_COMMIT_DEFAULT[1] in sql_cmd1)
        self.assertTrue(flag)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        # 系统管理员使用set命令修改参数synchronous_commit为2,查看参数值，显示remote_apply
        sql_cmd2 = ('''set synchronous_commit to 2;
                     show synchronous_commit;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test1_sys005 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.SET_SUCCESS_MSG, msg1)
        self.assertIn('remote_apply', msg1)
        # 重新连接数据库，查看参数值，显示默认值off
        sql_cmd3 = ('''show synchronous_commit;''')
        excute_cmd1 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd3}"
                                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        flag = (constant.SYNCHRONOUS_COMMIT_DEFAULT[0] in msg1 or constant.SYNCHRONOUS_COMMIT_DEFAULT[1] in msg1)
        self.assertTrue(flag)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除用户
        sql_cmd5 = commonsh.execut_db_sql('''drop user test1_sys005 cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_Guc_Synchronous_Commit_Case0005执行结束--------------------------')
