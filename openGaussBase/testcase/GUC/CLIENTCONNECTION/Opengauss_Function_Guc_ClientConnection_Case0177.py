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
Case Name   : 使用alter user方法设置参数lockwait_timeout为600000,观察预期结果
Description :
        1.查询lockwait_timeout默认值
        2.创建用户
        3.修改参数值为600000并查询
        4.删除用户
Expect      :
        1.显示默认值20min
        2.用户创建成功
        3.设置成功显示10min
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

LOG = Logger()
commonsh = CommonSH('dbuser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '-----Opengauss_Function_Guc_ClientConnection_Case0177start----')
        self.constant = Constant()
        self.user_node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_lockwait_timeout(self):
        # 查询默认值
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertEqual('20min', sql_cmd.split("\n")[-2].strip())
        # 创建用户
        sql_cmd = commonsh.execut_db_sql(f'''drop user if exists test_spur0177
            cascade;create user test_spur0177 password '{macro.COMMON_PASSWD}';
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        # 修改用户级别参数
        sql_cmd = commonsh.execut_db_sql('''alter user test_spur0177 
            set lockwait_timeout to 600000;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 查询
        sql_cmd2 = 'show lockwait_timeout;'
        excute_cmd1 = f'''source {self.DB_ENV_PATH};\
            gsql -d {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -U test_spur0177 \
            -W '{macro.COMMON_PASSWD}' \
            -c "{sql_cmd2}"
            '''
        LOG.info(sql_cmd2)
        msg1 = self.user_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn('10min', msg1)

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        sql_cmd = commonsh.execut_db_sql('''drop user if exists test_spur0177 
            cascade;
            ''')
        LOG.info(sql_cmd)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0177执行完成---')
