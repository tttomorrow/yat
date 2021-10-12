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
Case Name   : 在postgresql.conf文件中设置client_encoding参数，不生效
Description : 
    1. 修改postgresql.conf中client_encoding为GBK，重启数据库查询
    2. 恢复参数为UTF8
Expect      : 
    1. 不生效
    2. 恢复成功
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('''---Opengauss_Function_DML_Set_Case0033开始---''')
        self.commonsh = CommonSH('dbuser')
        self.user_node = Node('dbuser')

    def test_set(self):
        cmd0 = "show client_encoding;"
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        init = msg0.splitlines()[2].strip()
        client = ['SQL_ASCII', 'UTF8']
        self.var = client if init == 'UTF8' else list(reversed(client))

        def check_value(value):
            cmd = "show client_encoding;"
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            return self.assertTrue(value in msg)

        def restart():
            self.commonsh.restart_db_cluster()
            status = self.commonsh.get_db_cluster_status()
            self.assertTrue("Normal" in status or 'Degraded' in status)

        # 检查默认值是UTF8
        check_value(self.var[1])

        # 修改postgresql.conf文件里的client_encoding为GBK
        path = macro.DB_INSTANCE_PATH+'/postgresql.conf'
        cmd1 = f"sed -i '$a\\client_encoding=GBK' {path}"
        self.log.info(cmd1)
        msg1 = self.user_node.sh(cmd1).result()
        self.log.info(msg1)
        restart()
        check_value(self.var[1])

        # 恢复文件
        cmd1 = f"sed -i '$d' {path}"
        self.log.info(cmd1)
        msg1 = self.user_node.sh(cmd1).result()
        self.log.info(msg1)
        restart()
        check_value(self.var[1])

    def tearDown(self):
        self.log.info('''---Opengauss_Function_DML_Set_Case0033结束---''')