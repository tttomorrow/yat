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
Case Type   : 功能测试
Case Name   : to_clob函数转换二进制类型raw最大值
Description :
    步骤 1. 在sql_ascii数据库中执行语句
Expect      :
    步骤 1. 函数返回结果正确
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Toclob(unittest.TestCase):
    def setUp(self):
        self.sh_primy = CommonSH('dbuser')
        self.user = Node('dbuser')
        self.common = Common()
        cmd1 = 'show max_process_memory;'
        msg1 = self.sh_primy.execut_db_sql(cmd1)
        self.old_value = msg1.splitlines()[2].strip()
        self.config = "max_process_memory='25GB'"
        stopstatus, startstatus = self.common.config_set_modify(self.config)
        self.assertTrue(stopstatus)
        self.assertTrue(startstatus)

    def test_rawtoclob(self):
        LOG.info('----Opengauss_Function_Type_Trans_Clob_Case0001开始---')
        cmd2 = '''drop database if exists logdb1;
            create database logdb1 encoding = 'sql_ascii';'''
        msg2 = self.sh_primy.execut_db_sql(cmd2)
        LOG.info(msg2)

        cmd4 = f'''source {macro.DB_ENV_PATH};
            gsql -d logdb1 -p {self.user.db_port} -c "{cmd3}" '''
        LOG.info(cmd4)
        msg4 = self.user.sh(cmd4).result()
        LOG.info(msg4)

        cmd4 = f'''source {macro.DB_ENV_PATH};
            gsql -d logdb1 -p {self.user.db_port} -c "{cmd3}" '''
        LOG.info(cmd4)
        msg4 = self.user.sh(cmd4).result()
        LOG.info(msg4)

        cmd5 = 'drop database if exists logdb1;'
        msg5 = self.sh_primy.execut_db_sql(cmd5)
        LOG.info(msg5)
        self.assertTrue('DROP' in msg5)

    def tearDown(self):
        LOG.info('-----------恢复配置，并重启数据库-----------')
        self.item = 'max_process_memory=' + str(self.old_value)
        stopstatus, startstatus = self.common.config_set_modify(self.item)
        self.assertTrue(stopstatus)
        self.assertTrue(startstatus)
        LOG.info('---Opengauss_Function_Type_Trans_Clob_Case0001结束---')
