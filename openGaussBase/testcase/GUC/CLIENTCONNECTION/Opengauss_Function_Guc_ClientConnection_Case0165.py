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
Case Name   : 使用alter user方法设置参数gin_fuzzy_search_limit为1000,
              观察预期结果
Description :
        1.查询gin_fuzzy_search_limit默认值
        2.创建用户
        3.修改参数值为1000
        4.删除用户
Expect      :
        1.显示默认值0
        2.用户创建成功
        3.设置成功
        4.删除成功
History     :
"""
import time
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0165start-----')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.user_node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_gin_fuzzy_search_limit(self):
        # 查询默认值
        sql_cmd = self.commonsh.execut_db_sql('''show gin_fuzzy_search_limit;''')
        self.log.info(sql_cmd)
        self.assertEqual('0', sql_cmd.split('\n')[-2].strip())
        # 创建用户
        sql_cmd = self.commonsh.execut_db_sql(f'''drop user if exists
         test_spur0165 cascade;
         create user test_spur0165 password '{macro.COMMON_PASSWD}';
         ''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        # 创建用户
        sql_cmd = self.commonsh.execut_db_sql('''alter user test_spur0165
            set gin_fuzzy_search_limit to 1000;
            ''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 查询
        sql_cmd = '''show gin_fuzzy_search_limit;'''
        excute_cmd1 = f'''source {self.DB_ENV_PATH};
            gsql -d {self.user_node.db_name}\
            -p {self.user_node.db_port}\
            -U test_spur0165\
            -W '{macro.COMMON_PASSWD}'\
            -c "{sql_cmd}"\
            '''
        self.log.info(sql_cmd)
        msg1 = self.user_node.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertEqual('1000', msg1.split('\n')[-2].strip())

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql('''drop user if exists 
            test_spur0165 cascade;
            ''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0165执行完成----')
