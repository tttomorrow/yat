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
Case Type   : GUC参数--连接认证
Case Name   : 修改指定数据库，用户，会话级别的参数application_name为空值
Description :
        1.查询application_name默认值
        2.在gsql中分别设置数据库、用户、会话、级别application_name为空值
        3.清理环境
Expect      :
        1.显示默认值gsql
        2.设置成功
        3.清理环境完成
History     :
"""
import time
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

commonsh = CommonSH('dbuser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0125start-')
        self.Constant = Constant()
        self.userNode = Node('dbuser')

    def test_application_name(self):
        self.log.info('步骤1:查询application_name默认值')
        sql_cmd = commonsh.execut_db_sql('''show application_name;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('步骤2:set方法修改参数值')
        sql_cmd = commonsh.execut_db_sql("set application_name to '';"
                                         "show application_name ")
        self.log.info(sql_cmd)
        self.assertIn('', sql_cmd)
        self.log.info('步骤3:创建测试用户')
        sql_cmd = commonsh.execut_db_sql(f'''drop user if exists test_spur0223 
            cascade;
            create user test_spur0223 password '{macro.COMMON_PASSWD}';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.log.info('步骤4:修改用户级别参数并查询')
        sql_cmd = commonsh.execut_db_sql(f'''alter user test_spur0223 set 
            application_name to '';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        sql_cmd = '''show application_name;'''
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gsql " \
                     f"-d {self.userNode.db_name} " \
                     f"-p {self.userNode.db_port} " \
                     f"-U test_spur0223  " \
                     f"-W '{macro.COMMON_PASSWD}' " \
                     f"-c '{sql_cmd}'"
        self.log.info(sql_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertEqual('gsql', msg.split('\n')[2].strip())
        self.log.info('步骤5:修改数据库级别参数并查询')
        sql_cmd = commonsh.execut_db_sql(f'''alter database postgres set 
            application_name to '';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        sql_cmd = '''show application_name;'''
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gsql " \
                     f"-d {self.userNode.db_name} " \
                     f"-p {self.userNode.db_port} " \
                     f"-c '{sql_cmd}'"
        self.log.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertEqual('gsql', msg.split('\n')[2].strip())

    def tearDown(self):
        self.log.info('---------清理环境---------')
        sql_cmd = commonsh.execut_db_sql(f'''drop user if exists test_spur0223 
            cascade;''')
        self.log.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''alter database postgres reset 
            application_name;''')
        self.log.info(sql_cmd)
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0125finish-')
