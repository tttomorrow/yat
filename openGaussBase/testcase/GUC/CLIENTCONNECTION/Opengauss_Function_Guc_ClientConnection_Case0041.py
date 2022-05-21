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
Case Name   : 使用alter user方法设置参数temp_tablespaces为不存在的表空间名称,合理报错
Description :
        1.查询temp_tablespaces默认值
        2.创建用户
        3.修改参数值为不存在名称
        4.删除用户
Expect      :
        1.显示默认值为空
        2.用户创建成功
        3.合理报错
        4.删除成功
History     :
"""
import sys
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
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0041start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_temp_tablespaces(self):

        # 查询默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show temp_tablespaces;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 创建用户
        sql_cmd = self.commonsh.execut_db_sql(f'''drop user if exists test_spdb041 cascade;
                                                 create user test_spdb041 password '{macro.COMMON_PASSWD}';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        # 修改用户级别参数值
        sql_cmd = self.commonsh.execut_db_sql(f'''alter user test_spdb041 set temp_tablespaces to 't_temp_tablespaces041';''')
        self.log.info(sql_cmd)
        self.assertIn('NOTICE:  tablespace "t_temp_tablespaces041" does not exist', sql_cmd)
        sql_cmd2 = '''show temp_tablespaces;'''
        excute_cmd1 = f'''
                                  source {self.DB_ENV_PATH};
                                  gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_spdb041 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                                   '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn('', msg1)

    def tearDown(self):
        self.log.info('----------------清理环境-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop user if exists test_spdb041 cascade;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0041执行完成---------------')
