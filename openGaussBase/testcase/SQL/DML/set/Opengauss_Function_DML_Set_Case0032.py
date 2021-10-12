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
Case Name   : 使用gs_guc工具设置客户端编码，不生效
Description :
    1. gs_guc set 设置客户端编码集SQL_ASCII
    2. gs_guc reload 设置客户端编码集GBK
Expect      :
    1. 设置不生效
    2. 设置不生效
History     :
"""

import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.commonsh = CommonSH('dbuser')
        self.user_node = Node('dbuser')
        self.log = Logger()
        self.cluster_path = macro.DB_INSTANCE_PATH
        self.log.info('''---Opengauss_Function_DML_Set_Case0032开始---''')

    def test_encode(self):
        cmd0 = "show client_encoding;"
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        init = msg0.splitlines()[2].strip()
        client = ['SQL_ASCII', 'UTF8']
        self.var = client if init == 'UTF8' else list(reversed(client))

        def restart_check():
            self.commonsh.restart_db_cluster()
            status = self.commonsh.get_db_cluster_status()
            self.assertTrue("Normal" in status or 'Degraded' in status)
            # 检查未生效，还是utf8
            cmd = 'show client_encoding;'
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            return msg

        # gs_guc set 设置客户端编码集SQL_ASCII
        cmd1 = f'''source {macro.DB_ENV_PATH}
        gs_guc set -N all -I all -c "client_encoding='{self.var[0]}'"'''
        self.log.info(cmd1)
        msg1 = self.user_node.sh(cmd1).result()
        self.log.info(msg1)
        res = restart_check()
        self.assertTrue(self.var[1] in res)

        # gs_guc reload 设置客户端编码集GBK
        cmd2 = f'''source {macro.DB_ENV_PATH}
        gs_guc reload -D {self.cluster_path} -c "client_encoding = 'GBK'"'''
        self.log.info(cmd2)
        msg2 = self.user_node.sh(cmd2).result()
        self.log.info(msg2)
        res = restart_check()
        self.assertTrue(self.var[1] in res)

    def tearDown(self):
        self.log.info('''---Opengauss_Function_DML_Set_Case0032结束---''')