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
Case Type   : security_sm4
Case Name   : sm4加密数据后，错误的密码解密
Description :
    1.创建表，对插入的数据加密对数据加密
    2.select查询数据,
    3.select查询加密数据，用错误的密码解密步骤2查询出的密文数据，
Expect      :
    1.表创建成功，数据插入如完成
    2.查询出lucy的address加密，显示密文（密文随机）
    3.未查询出来lucy及address信息
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_sm4_Case0006 start---')
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_sm4(self):
        logger.info('----1-2.创建表table001；表中插入数据，对address字段加密----')
        sql_cmd1 = 'create table table001(name char(6),address text);' \
                   'insert into table001 values(\'lucy\',' \
                   'gs_encrypt(\'shanxi.xian,yantaqu0569-5\',' \
                   '\'QAZ2wssx@123\',\'sm4\')),(\'张三\',\'shanxi.xian,' \
                   'yantaqu0569-5\'),(\'李四\',\'shanxi.大同,yantaqu0569-5\');'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(sql_msg1)
        self.assertTrue(sql_msg1.find('INSERT 0 3') > -1)
        sql_cmd2 = 'select address from table001 where name=\'lucy\';'
        sql_msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(sql_msg2)
        sql_msg2_list = sql_msg2.splitlines()
        self.assertTrue(sql_msg2_list[0].strip() == 'address' and
                        sql_msg2_list[2].strip() != 'shanxi.xian,yantaqu0569-5'
                        and sql_msg2_list[-1].strip() == '(1 row)')
        logger.info('----3.用错误的密码解密步骤2查询出的密文数据----')
        sql_cmd3 = f'select address from table001 where address = ' \
                   f'gs_decrypt(\'{sql_msg2_list[2].strip()}\',' \
                   f'\'QAZwsx12\',\'sm4\');'
        logger.info(sql_cmd3)
        sql_msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(sql_msg3)
        self.assertFalse('shanxi.xian,yantaqu0569-5' in sql_msg3)

    def tearDown(self):
        logger.info('-------清理表-------')
        sql_cmd1 = 'drop table table001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.find('DROP TABLE') > -1)
        logger.info('----Opengauss_Function_Security_sm4_Case0006 finish----')