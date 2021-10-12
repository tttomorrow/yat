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
Case Type   : 函数和操作符-安全函数
Case Name   : 函数以keystr为密钥对decrypt字符串进行解密，返回解密后的字符串
Description : 函数以keystr为密钥对decrypt字符串进行解密，返回解密后的字符串
Expect      : 返回正常，解密成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0002开始-')
        self.primary_dbuser = Node('PrimaryDbUser')
        self.commonsh = CommonSH()

    def test_security_function(self):
        self.log.info('---------步骤1.输入密钥字符串，返回解密后的字符串---------')
        sql_cmd = self.commonsh.execut_db_sql(f'select '
                                              f'gs_decrypt_aes128((select '
                                              f'gs_encrypt_aes128'
                                              f'(\'MPPDB\',\'Asdf1234\')),'
                                              f'\'Asdf1234\');')
        self.log.info(sql_cmd)
        self.assertIn('MPPDB', sql_cmd)

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0002结束-')
