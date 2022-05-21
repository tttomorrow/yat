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
Case Name   : set session命令设置客户端编码集
Description :
    1. 查看client_encoding默认值UTF8
    2. set session命令设置客户端编码集为SQL_ASCII
    3. 查看当前值及该参数运行时的具体信息
    4. 恢复默认值
Expect      : 
    1. 默认值utf8
    2. 设置成功
    3. 运行值与设置值相同
    4. 恢复成功
History     : 
"""

import unittest

from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---Opengauss_Function_DML_Set_Case0029开始---''')

    def test_set(self):
        cmd0 = "show client_encoding;"
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        init = msg0.splitlines()[2].strip()
        client = ['SQL_ASCII', 'UTF8']
        self.var = client if init == 'UTF8' else list(reversed(client))

        cmd = f"""
        set session names '{self.var[0]}';
        show client_encoding;
        select setting from pg_settings where name='client_encoding';
        set session names '{self.var[1]}';
        show client_encoding;
        select setting from pg_settings where name='client_encoding';"""
        self.log.info(cmd)
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        lines = msg.splitlines()
        self.assertTrue(msg.count('SET') == 2)
        self.assertTrue(lines[3].find(self.var[0]) > -1)
        self.assertTrue(lines[-7].find(self.var[1]) > -1)

    def tearDown(self):
        self.log.info('''---Opengauss_Function_DML_Set_Case0029结束---''')
