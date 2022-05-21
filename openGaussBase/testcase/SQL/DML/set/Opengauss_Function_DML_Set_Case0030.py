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
Case Name   : 使用set local命令设置客户端编码集在事务外不生效，事务内生效
Description :
    1. 事务外set local命令设置客户端编码集
    2. 事务内set local命令设置客户端编码集
    3. 事务内set local命令设置客户端编码集后回滚
    4. 设置会话级client_encoding为GBK再reset
Expect      :
    1. 设置不生效
    2. 事务内设置生效，事务结束后恢复
    3. 事务内设置生效，回滚后恢复
    4. 修改成功，reset后恢复utf8
History     :
"""

import unittest

from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---Opengauss_Function_DML_Set_Case0030开始---''')
        cmd0 = "show client_encoding;"
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.init = msg0.splitlines()[2].strip()
        client = ['SQL_ASCII', 'UTF8']
        self.var = client if self.init == 'UTF8' else list(reversed(client))

    def test_encode1(self):
        cmd = f"set local names '{self.var[0]}'; show client_encoding;"
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue(self.var[1] in msg)

    def test_encode2(self):
        cmd = f"""start transaction;
                 set local names '{self.var[0]}';
                 show client_encoding;
                 commit;
                 show client_encoding;"""
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        lines = msg.splitlines()
        self.assertTrue(self.var[0] in lines[4] and self.var[1] in lines[-2])

    def test_encode3(self):
        cmd = """start transaction;
                 set local names 'SQL_ASCII';
                 show client_encoding;
                 rollback;
                 show client_encoding;"""
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        lines = msg.splitlines()
        self.assertTrue('SQL_ASCII' in lines[4] and self.init in lines[-2])

    def test_encode4(self):
        cmd = """set session names 'GBK';
                show client_encoding;
                reset client_encoding;
                show client_encoding;"""
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        lines = msg.splitlines()
        self.assertTrue('GBK' in lines[3] and self.var[1] in lines[-2])

    def tearDown(self):
        self.log.info('''---Opengauss_Function_DML_Set_Case0030结束---''')