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
Case Type   : 用户组
Case Name   : 非初始用户（sysadmin用户）创建目录对象
Description :
        1.创建用户组，先赋予LOGIN权限
        2.给test_group4用户赋予CREATEDB权限
        3.切换至test_group4用户，创建数据库
        4.清理环境
Expect      :
        1.创建成功
        2.赋权成功
        3.创建成功
        4.清理环境完成
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Group(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Create_Group_Case0005开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('dbuser')
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建用户组，先赋予LOGIN权限
        sql_cmd1 = commonsh.execut_db_sql(f'''drop group if exists test_group4;
                                       create group test_group4 with LOGIN password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
       # 给test_group4用户赋予CREATEDB权限
        sql_cmd2 = commonsh.execut_db_sql('''alter role test_group4 CREATEDB;''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd2)
        # 切换至test_group4用户，创建数据库
        sql_cmd3 = ('''drop database if exists test_db;
                    create database test_db;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_group4 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertTrue(msg1.find('CREATE DATABASE') > -1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除数据库
        sql_cmd4 = commonsh.execut_db_sql('''drop database test_db;''')
        logger.info(sql_cmd4)
        # 删除group
        sql_cmd5 = commonsh.execut_db_sql('''drop group test_group4;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DDL_Create_Group_Case0005执行结束--------------------------')





