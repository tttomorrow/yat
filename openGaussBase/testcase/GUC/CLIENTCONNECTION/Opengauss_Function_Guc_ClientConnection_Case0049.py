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
Case Name   : 使用alter database方法设置参数check_function_bodies为off观察预期结果
Description :
        1.查询check_function_bodies默认值
        2.创建数据库
        3.修改参数值为off
        4.查询修改后的参数值并创建函数，函数无参数，返回值有参数
        5.删除数据库
Expect      :
        1.显示默认值为on
        2.数据库创建成功
        3.设置成功
        4.函数创建成功
        5.删除成功
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
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0049start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_check_function_bodies(self):

         # 查看默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show check_function_bodies;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
         # 创建数据库
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists test_spdb049;
                                                 create database test_spdb049;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        # 修改数据库级别参数
        sql_cmd = self.commonsh.execut_db_sql(f'''alter database test_spdb049 set check_function_bodies to off ;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 查询修改后的参数值并创建函数
        sql_cmd2 = '''show check_function_bodies;
        CREATE or replace FUNCTION bad049() RETURNS void LANGUAGE sql AS 'SELECT \$1';'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d test_spdb049 -p {self.userNode.db_port} -c "{sql_cmd2}"
                             '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn('off', msg1)
        self.assertIn(self.Constant.CREATE_FUNCTION_SUCCESS_MSG, msg1)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop FUNCTION bad049;
                                               drop database if exists test_spdb049;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0049执行完成---------------')
