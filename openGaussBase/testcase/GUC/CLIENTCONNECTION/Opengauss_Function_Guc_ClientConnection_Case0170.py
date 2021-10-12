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
Case Name   : 使用alter database方法设置参数deadlock_timeout为5,观察预期结果
Description :
        1.查询deadlock_timeout默认值
        2.创建数据库
        3.修改参数值为5并查询
        4.删除数据库
Expect      :
        1.显示默认值1s
        2.数据库创建成功
        3.设置成功，显示5ms
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
            '---Opengauss_Function_Guc_ClientConnection_Case0170start-----')
        self.constant = Constant()
        self.user_node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_deadlock_timeout(self):
        # 查询默认值
        sql_cmd = commonsh.execut_db_sql('show deadlock_timeout;')
        LOG.info(sql_cmd)
        self.assertEqual('1s', sql_cmd.split("\n")[-2].strip())
        # 创建数据库
        sql_cmd = commonsh.execut_db_sql('drop database if exists test_spdb170;'
                                       'create database test_spdb170;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        # 修改数据库级别参数
        sql_cmd = commonsh.execut_db_sql('alter database test_spdb170 set '
                                       'deadlock_timeout to 5;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 查询
        sql_cmd2 = 'show deadlock_timeout;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d test_spdb170' \
                      f' -p {self.user_node.db_port}' \
                      f' -c "{sql_cmd2}" '
        LOG.info(sql_cmd2)
        msg1 = self.user_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertEqual('5ms', msg1.split("\n")[-2].strip())

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        sql_cmd = commonsh.execut_db_sql('drop database if exists test_spdb170;')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0170执行完成---')
