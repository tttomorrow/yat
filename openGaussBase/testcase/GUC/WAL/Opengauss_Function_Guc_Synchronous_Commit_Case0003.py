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
Case Name   : 普通用户使用alter user命令设置参数值synchronous_commit为2
Description :
        1.查询synchronous_commit默认值
        2.创建用户
        3.普通用户使用alter user命令修改参数为2
        4.普通用户重新连接数据库，查看参数值
        5.重新连接数据库不使用test1_user003用户，查看参数值
        6.恢复参数默认值
        7.删除用户
Expect      :
        1.单机环境显示默认值为off，双机为on
        2.用户创建成功
        3.未退出会话，查看参数值为off
        4.参数值生效，为remote_apply
        5.修改的参数值只对用户test1_user003生效，其他用户查看单机环境显示默认值为off，双机为on
        6.恢复参数默认值成功
        7.删除成功
History     :
"""
import sys
import unittest
import time

sys.path.append(sys.path[0] + "/../")
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
        logger.info('------------------------Opengauss_Function_Guc_Synchronous_Commit_Case0003开始执行-----------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_synchronous_commit(self):
        # 查看参数默认值且创建普通用户
        sql_cmd1 = commonsh.execut_db_sql(f'''show synchronous_commit;
                                       drop user if exists test1_user003 cascade;
                                       create user test1_user003 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        flag = (constant.SYNCHRONOUS_COMMIT_DEFAULT[0] in sql_cmd1 or constant.SYNCHRONOUS_COMMIT_DEFAULT[1] in sql_cmd1)
        self.assertTrue(flag)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        # 普通用户使用alter user命令修改参数为2；未退出会话，查看参数值
        sql_cmd2 = ('''alter user test1_user003 set synchronous_commit to 2;
                    show synchronous_commit;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test1_user003 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.ALTER_ROLE_SUCCESS_MSG, msg1)
        flag = (constant.SYNCHRONOUS_COMMIT_DEFAULT[0] in msg1 or constant.SYNCHRONOUS_COMMIT_DEFAULT[1] in msg1)
        self.assertTrue(flag)
        time.sleep(3)
        # 普通用户重新连接数据库，查看参数值，参数值生效，为remote_apply
        sql_cmd3 = '''show synchronous_commit;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test1_user003 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('remote_apply', msg1)
        # 重新连接数据库，查看参数值，为off，修改的参数值只对用户test1_user003生效
        sql_cmd4 = ('''show synchronous_commit;''')
        excute_cmd1 = f'''
                                           source {self.DB_ENV_PATH};
                                           gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd4}"
                                           '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        flag = (constant.SYNCHRONOUS_COMMIT_DEFAULT[0] in sql_cmd4 or constant.SYNCHRONOUS_COMMIT_DEFAULT[1] in sql_cmd4)
        self.assertTrue(flag)
        # 恢复参数默认值
        sql_cmd5 = ('''alter user test1_user003 set synchronous_commit to off;''')
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test1_user003 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd5}"
                                   '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.ALTER_ROLE_SUCCESS_MSG, msg1)
        
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除用户
        sql_cmd5 = commonsh.execut_db_sql('''drop user test1_user003 cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_Guc_Synchronous_Commit_Case0003执行结束--------------------------')
