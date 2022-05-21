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
Case Name   : 以keystr为密钥对encryptstr字符串进行加密，密码长度不符合要求
Description :
    1.密码为7字节，返回加密后的字符串，合理报错
    2.密码为17字节，返回加密后的字符串，合理报错
    2.密码为0字节，返回加密后的字符串，合理报错
Expect      :
    1.合理报错，并出现密码错误提示信息
    2.合理报错，并出现密码错误提示信息
    3.合理报错，并出现密码错误提示信息
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0004开始-')
        self.primary_dbuser = Node('PrimaryDbUser')
        self.commonsh = CommonSH()

    def test_security_function(self):
        self.log.info('---步骤1.密码为7字节，返回加密后的字符串，合理报错---')
        sql_cmd = self.commonsh.execut_db_sql(f'select gs_encrypt_aes128'
                                              f'(\'MPPDB\',\'Asdf123\');')
        self.log.info(sql_cmd)
        error_msg = 'ERROR:  The encryption key ' \
                    'must be 8~16 bytes and contain ' \
                    'at least three kinds of characters!'
        self.assertIn(error_msg, sql_cmd)

        self.log.info('---步骤2.密码为17字节，返回加密后的字符串，合理报错---')
        sql_cmd = self.commonsh.execut_db_sql(f'select gs_encrypt_aes128'
                                              f'(\'MPPDB\',\'Asdf123'
                                              f'4Asdf12345\');')
        self.log.info(sql_cmd)
        self.assertIn(error_msg, sql_cmd)

        self.log.info('---步骤3.密码为0字节，返回加密后的字符串，合理报错---')
        sql_cmd = self.commonsh.execut_db_sql(f'select gs_encrypt_aes128'
                                              f'(\'MPPDB\',\'\');')
        self.log.info(sql_cmd)
        self.assertIn('ERROR:  The encryption key can not be empty', sql_cmd)

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Innerfunc_Security_Case0004结束-')