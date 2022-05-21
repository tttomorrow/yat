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
Case Name   : 使用alter user方法设置参数partition_lock_upgrade_timeout为3000,
              观察预期结果
Description :
        1.查询partition_lock_upgrade_timeout默认值
        2.创建用户
        3.修改参数值为3000
        4.删除用户
Expect      :
        1.显示默认值1800
        2.用户创建成功
        3.设置成功
        4.删除成功
History     :
"""
import unittest
import time

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
            '----Opengauss_Function_Guc_ClientConnection_Case0197start-----')
        self.constant = Constant()
        self.user_node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_partition_lock_upgrade_timeout(self):
        # 查询默认值
        sql_cmd = commonsh.execut_db_sql('show partition_lock_upgrade_timeout;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 创建用户
        sql_cmd = commonsh.execut_db_sql(f'''drop user if exists test_spur0197
            cascade;
            create user test_spur0197 password '{macro.COMMON_PASSWD}';
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        # 修改用户级别参数
        sql_cmd = commonsh.execut_db_sql('''alter user test_spur0197 set
            partition_lock_upgrade_timeout to 3000;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 查询
        sql_cmd = 'show partition_lock_upgrade_timeout';

        excute_cmd1 = f'''source {self.DB_ENV_PATH};\
            gsql -d {self.user_node.db_name} \
            -p{self.user_node.db_port} \
            -U test_spur0197 \
            -W '{macro.COMMON_PASSWD}' \
            -c "{sql_cmd}"\
            '''
        LOG.info(sql_cmd)
        msg1 = self.user_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn('3000', msg1)

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        sql_cmd = commonsh.execut_db_sql('''drop user if exists test_spur0197 
            cascade;
            ''')
        LOG.info(sql_cmd)
        LOG.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0197执行完成---')
