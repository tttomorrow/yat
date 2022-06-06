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
Case Name   : 使用alter user方法设置参数default_tablespace,观察预期结果
Description :
        1.查询default_tablespace默认值
        2.创建用户
        3.修改参数值为不存在的名称并查询
        4.删除用户
Expect      :
        1.显示默认值为空
        2.用户创建成功
        3.发出notice，默认值仍然是空
        4.删除成功
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
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0030start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_default_tablespace(self):
        # 查看默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show default_tablespace;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        sql_cmd = self.commonsh.execut_db_sql(f'''drop user if exists test_spur030 cascade;
                                                 create user test_spur030 password '{macro.COMMON_PASSWD}';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant. CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        # 使用alter user设置default_tablespace为t_tablespace030
        sql_cmd = self.commonsh.execut_db_sql(f'''alter user test_spur030 set default_tablespace to 't_tablespace030';''')
        self.log.info(sql_cmd)
        self.assertIn('NOTICE:  tablespace "t_tablespace030" does not exist', sql_cmd)
        time.sleep(3)
        # 查询该参数修改后的值
        sql_cmd2 = '''show default_tablespace;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_spur030 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                             '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn('WARNING:  invalid value for parameter "default_tablespace": "t_tablespace030"', msg1)
        self.assertIn('', msg1)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop user if exists test_spur030 cascade;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0030执行完成---------------')
