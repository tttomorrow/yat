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
Case Type   : 函数和操作符-安全函数
Case Name   : 输入密码与加密时密码不符，返回加密后的字符串,合理报错
Description :
    1.解密时输入密码与加密时密码不符，返回加密后的字符串
    2.解密时keystr为空，返回加密后的字符串
Expect      :
    1.合理报错，提示解密失败
    2.合理报错，提示解密密钥不能为空
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0006开始-')
        self.primary_dbuser = Node('PrimaryDbUser')
        self.commonsh = CommonSH()

    def test_security_function(self):
        self.log.info('---步骤1.输入密码与加密时密码不符，返回加密后的字符串，合理报错---')
        sql_cmd = self.commonsh.execut_db_sql(f'select gs_decrypt_aes128'
                                              f'(\'gwditQLQG8NhFw4OuoKhhQJoX'
                                              f'ojhFlYkjeG0aYdSCtLCnIUgkNwvY'
                                              f'04KbuhmcGZp8jWizBdR1vU9Cspju'
                                              f'zII0lbz12A=\',\'1234\');')
        self.log.info(sql_cmd)
        self.assertIn('ERROR:  decrypt the cipher text failed', sql_cmd)
        self.log.info('---步骤1.解密时keystr为空，返回加密后的字符串，合理报错---')
        sql_cmd = self.commonsh.execut_db_sql(f'select gs_decrypt_aes128'
                                              f'(\'gwditQLQG8NhFw4OuoKhhQJo'
                                              f'XojhFlYkjeG0aYdSCtLCnIU'
                                              f'gkNwvYI04KbuhmcGZp8jWizB'
                                              f'dR1vU9CspjuzI0lbz12A'
                                              f'=\',\'\');')
        self.log.info(sql_cmd)
        self.assertIn('ERROR:  The decryption key can not be empty', sql_cmd)

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0006结束-')
