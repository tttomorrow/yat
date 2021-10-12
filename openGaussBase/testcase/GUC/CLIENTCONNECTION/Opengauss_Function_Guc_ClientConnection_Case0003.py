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
Case Type   : GUC
Case Name   : 使用alter database方法设置参数search_path(模式搜索顺序),观察预期结果
Description :
        1.查询search_path默认值
        2.创建数据库；创建模式
        3.修改参数值为新模式
        4.删除模式；删除数据库
Expect      :
        1.显示默认值"$user",public
        2.数据库创建成功；模式创建成功
        3.设置成功
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
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0003start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_search_path(self):
        # 查看默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show search_path;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 创建数据库和模式
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists test_spdb;
                                                 create database test_spdb;
                                                 drop schema if exists t_myschema002 cascade;
                                                 create schema t_myschema002;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.CREATE_SCHEMA_SUCCESS_MSG, sql_cmd)
        # 使用alter database设置search_path为t_myschema002
        sql_cmd = self.commonsh.execut_db_sql(f'''alter database test_spdb set search_path to 't_myschema002';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 连接test_spdb数据库查询该参数修改后的值
        sql_cmd2 = '''show search_path;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d test_spdb -p {self.userNode.db_port} -c "{sql_cmd2}"
                             '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn('t_myschema002', msg1)

    def tearDown(self):
        self.log.info('----------------清理环境-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop schema if exists t_myschema002 cascade;
                                                drop database if exists test_spdb;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0003执行完成---------------')
