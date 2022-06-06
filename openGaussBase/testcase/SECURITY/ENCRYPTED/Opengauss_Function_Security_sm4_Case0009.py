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
Case Name   : sm4加密，加密数据为非字符串类型
Description :
    1.加密数据为bool类型
    2.加密类型为数值类型
Expect      :
    1.加密失败
    2.加密成功
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
            '---Opengauss_Function_Security_sm4_Case0009 start---')
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.logfile_name = os.path.join(macro.PG_LOG_PATH, 'dn_6001')
        self.num = 12345
    
    def test_aes128(self):
        text = '----step1:加密数据为bool类型 expect:数据加密失败----'
        self.log.info(text)
        sql_cmd1 = f'select gs_encrypt(true,\'{macro.COMMON_PASSWD}\',' \
            f'\'sm4\');'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.log.info(msg1)
        self.assertIn(f'No function matches the given name', msg1,
                      '执行失败:' + text)
        text = '----step2:加密数据为数值型 expect:数据加密成功----'
        self.log.info(text)
        sql_cmd2 = f'select gs_encrypt({self.num},\'{macro.COMMON_PASSWD}\',' \
            f'\'sm4\');'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.log.info(msg2)
        ciphertext = msg2.splitlines()[-2].strip()
        self.log.info(ciphertext)
        sql_cmd3 = f'select gs_decrypt(\'{ciphertext}\',' \
            f'\'{macro.COMMON_PASSWD}\',\'sm4\');'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.log.info(msg3)
        self.assertIn(f'{self.num}', msg3, '执行失败:' + text)
    
    def tearDown(self):
        self.log.info(
            '---Opengauss_Function_Security_sm4_Case0009 finish---')
