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
Case Type   : security_aes128
Case Name   : gs_encrypt函数与gs_encrypt_aes128函数互解密
Description :
    1.gs_encrypt函数对数据加密，gs_decrypt_aes128对数据解密
    2.gs_ecrypt_aes128对数据加密，gs_decrypt函数对数据解密
    3.aes128加密方式加密，sm4方式解密
    4.sm4加密方式加密，aes128方式解密
Expect      :
    1.数据解密成功
    2.数据解密成功
    3.数据解密失败
    4.数据解密失败
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Security_aes128_Case0009 start---')
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.logfile_name = os.path.join(macro.PG_LOG_PATH, 'dn_6001')
        self.string = 'MPPDAQ'
    
    def test_aes128(self):
        text = '------step1:gs_encrypt函数对数据加密，gs_decrypt_aes128对数据' \
               '解密 expect:数据解密成功------'
        self.log.info(text)
        sql_cmd1 = f'select gs_encrypt(\'{self.string}\',' \
            f'\'{macro.COMMON_PASSWD}\',\'aes128\');'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.log.info(msg1)
        ciphertext = msg1.splitlines()[-2].strip()
        self.log.info(ciphertext)
        sql_cmd2 = f'select gs_decrypt_aes128(\'{ciphertext}\',' \
            f'\'{macro.COMMON_PASSWD}\');'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.common.equal_sql_mdg(msg2, 'gs_decrypt_aes128', f'{self.string}',
                                  '(1 row)', flag='1')
        text = '------step2:gs_encrypt_aes128函数对数据加密，gs_decrypt对数据' \
               '解密 expect:数据解密成功------'
        self.log.info(text)
        sql_cmd3 = f'select gs_encrypt_aes128(\'{self.string}\',' \
            f'\'{macro.COMMON_PASSWD}\');'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.log.info(msg3)
        ciphertext = msg3.splitlines()[-2].strip()
        self.log.info(ciphertext)
        sql_cmd4 = f'select gs_decrypt(\'{ciphertext}\',' \
            f'\'{macro.COMMON_PASSWD}\',\'aes128\');'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.common.equal_sql_mdg(msg4, 'gs_decrypt', f'{self.string}',
                                  '(1 row)', flag='1')
        text = '----step3:aes128加密方式加密，sm4方式解密 expect:数据解密失败----'
        self.log.info(text)
        sql_cmd5 = f'select gs_encrypt(\'{self.string}\',' \
            f'\'{macro.COMMON_PASSWD}\',\'aes128\');'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        self.log.info(msg5)
        ciphertext = msg5.splitlines()[-2].strip()
        self.log.info(ciphertext)
        sql_cmd6 = f'select gs_decrypt(\'{ciphertext}\',' \
            f'\'{macro.COMMON_PASSWD}\',\'sm4\');'
        msg6 = self.sh_primy.execut_db_sql(sql_cmd6)
        self.log.info(msg6)
        self.assertNotIn(f'{self.string}', msg6, '执行失败:' + text)
        text = '----step4:sm4加密方式加密，aes128方式解密 expect:数据解密失败----'
        self.log.info(text)
        sql_cmd7 = f'select gs_encrypt(\'{self.string}\',' \
            f'\'{macro.COMMON_PASSWD}\',\'aes128\');'
        msg7 = self.sh_primy.execut_db_sql(sql_cmd7)
        self.log.info(msg7)
        ciphertext = msg7.splitlines()[-2].strip()
        self.log.info(ciphertext)
        sql_cmd8 = f'select gs_decrypt(\'{ciphertext}\',' \
            f'\'{macro.COMMON_PASSWD}\',\'sm4\');'
        msg8 = self.sh_primy.execut_db_sql(sql_cmd8)
        self.log.info(msg8)
        self.assertNotIn(f'{self.string}', msg8, '执行失败:' + text)
    
    def tearDown(self):
        self.log.info(
            '---Opengauss_Function_Security_aes128_Case0009 finish---')
