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
Case Name   : 不修改search_path参数值，使用和当前登录数据库同名的模式建表，查询成功
Description :
        1.创建用户
        2.切换至新用户建表，建表指定和当前登录数据库的用户名相同
        3.插入数据
        4.查询表数据
        5.删除表
        6.删除用户
Expect      :
        1.用户创建成功
        2.建表成功
        3.数据插入成功
        4.查询成功
        5.删除成功
        6.删除成功
History     :
"""
import sys
import time
import unittest

from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0016start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_search_path(self):
        # 创建用户
        sql_cmd = self.commonsh.execut_db_sql(f'''show search_path;
                                                drop user if exists user001 cascade;
                                                create user user001 password '{macro.COMMON_PASSWD}';''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        # user001用户下建表且插入数据
        sql_cmd2 = '''drop table if exists user001.sp cascade;
                      create table user001.sp(t text);
                      insert into user001.sp values('first day');
                      select * from user001.sp;'''
        excute_cmd1 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U user001 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                                     '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg1)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg1)
        self.assertIn('first day', msg1)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop table if exists user001.sp cascade;
                                                drop user if exists user001 cascade;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0016执行完成---------------')
