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
Case Name   : 检验aes128加密数据的密码长度
Description :
    1.校验8位密码加密
    2.校验16位密码加密
    3.校验7密码加密
    4.校验17密码加密
Expect      :
    1.返回密文
    2.返回密文
    3.返回报错：ERROR:  The encryption key must be 8~16 bytes and contain at
    least three kinds of characters!
    4.返回报错：ERROR:  The encryption key must be 8~16 bytes and contain at
    least three kinds of characters!
    3.报语法错误
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_aes128_Case0007 start---')
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_aes128(self):
        logger.info('----1.校验8位密码加密----')
        sql_cmd0 = 'create table table001(name char(6),address text);' \
                   'insert into table001 values(\'lucy\',' \
                   'gs_encrypt(\'shanxi.xian,yantaqu0569-5\',' \
                   '\'1QAZ2wsx\',\'aes128\')),(\'张三\',\'shanxi.xian,' \
                   'yantaqu0569-5\'),(\'李四\',\'shanxi.大同,yantaqu0569-5\');'
        sql_msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        logger.info(sql_msg0)
        sql_cmd1 = 'select address from table001 where name = \'lucy\';'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(sql_msg1)
        return_msg1 = sql_msg1.splitlines()
        self.assertTrue(return_msg1[0].strip() == 'address' and
                        return_msg1[2].strip() != 'shanxi.xian,yantaqu0569-5')
        logger.info('----2.校验16位密码加密----')
        sql_cmd2 = 'select gs_encrypt(\'shanxi.xian,yantaqu0569-5\',' \
                   '\'1QAZ2wsx3edc4rfv\',\'aes128\');'
        sql_msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(sql_msg2)
        return_msg2 = sql_msg2.splitlines()
        self.assertTrue(return_msg2[0].strip() == 'gs_encrypt' and
                        return_msg2[2].strip() != 'shanxi.xian,yantaqu0569-5')
        logger.info('----3.校验7位密码加密----')
        sql_cmd3 = 'select gs_encrypt(\'shanxi.xian,yantaqu0569-5\',' \
                   '\'1QAZ2ws\',\'aes128\');'
        sql_msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(sql_msg3)
        self.assertTrue('The encryption key must be 8~16 bytes and contain '
                        'at least three kinds of characters' in sql_msg3)
        logger.info('----4.校验17位密码加密----')
        sql_cmd4 = 'select gs_encrypt(\'shanxi.xian,yantaqu0569-5\',' \
                   '\'1QAZ2wsx3edc4rfv@\',\'aes128\');'
        sql_msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(sql_msg4)
        self.assertTrue('The encryption key must be 8~16 bytes and contain '
                        'at least three kinds of characters' in sql_msg4)

    def tearDown(self):
        logger.info('-------清理表-------')
        sql_cmd1 = 'drop table table001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.find('DROP TABLE') > -1)
        logger.info('---Opengauss_Function_Security_aes128_Case0007 finish---')
