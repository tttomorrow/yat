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
Case Name   : 使用alter user方法设置参数DateStyle输入输出的年/月/日顺序(YMD),观察预期结果
Description :
        1.查询DateStyle默认值
        2.创建用户
        3.修改参数值为YMD并查询当前日期
        4.删除用户
Expect      :
        1.显示默认值ISO, MDY
        2.用户创建成功
        3.设置成功且当前日期显示顺序为YMD
        4.删除成功
History     :
"""
import sys
import unittest
import time
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0127start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_DateStyle(self):
        
        # 查询默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show DateStyle;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 创建数据库
        sql_cmd = self.commonsh.execut_db_sql(f'''drop user if exists test_spur0127 cascade;
                                                 create user test_spur0127 password '{macro.COMMON_PASSWD}';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        # 修改数据库级别参数值
        sql_cmd = self.commonsh.execut_db_sql(f'''alter user test_spur0127 set DateStyle to 'YMD';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 查询修改后的参数值
        sql_cmd2 = '''show DateStyle;'''
        excute_cmd1 = f'''
                           source {self.DB_ENV_PATH};
                           gsql -d  {self.userNode.db_name}  -p {self.userNode.db_port} -U test_spur0127 -W '{macro.COMMON_PASSWD}' -c"{sql_cmd2}"
                            '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn('ISO, YMD', msg1)
        # 查询当前日期
        sql_cmd3 = '''select current_date;'''
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d  {self.userNode.db_name}  -p {self.userNode.db_port} -U test_spur0127 -W '{macro.COMMON_PASSWD}' -c"{sql_cmd3}"
                                   '''
        self.log.info(sql_cmd3)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        create_date = time.strftime("%Y-%m-%d", time.localtime())
        self.log.info(create_date)
        self.assertTrue(msg1.splitlines()[-2].strip() == create_date)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop user if exists test_spur0127 cascade;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0127执行完成---------------')
