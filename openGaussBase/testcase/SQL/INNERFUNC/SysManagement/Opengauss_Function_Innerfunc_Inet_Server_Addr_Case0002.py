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
Case Type   : 功能测试
Case Name   : 非远程连接模式下查询服务器接收当前连接用的IP地址
Description :
    1.非远程状态，执行命令select inet_server_addr();
Expect      :
    1.返回空
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('--------' +
            'Opengauss_Function_Innerfunc_Inet_Server_Addr_Case0002开始------')
        self.commonsh = CommonSH('dbuser')

    def test_inet(self):
        cmd1 = '''select inet_server_addr();'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.splitlines()[2].strip() == '')

    def tearDown(self):
        self.log.info('--------' +
            'Opengauss_Function_Innerfunc_Inet_Server_Addr_Case0002结束------')