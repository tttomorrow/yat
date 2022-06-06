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
Case Name   : sm4加密数据，密码为数字+小写字母
Description :
    1.select gs_encrypt('shanxi.xian,yantaqu0569-5','wssx1234','sm4');
Expect      :
    1.ERROR:  The encryption key must be 8~16 bytes and contain at least
    three kinds of characters!
    CONTEXT:  referenced column: gs_encrypt
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_sm4_Case0004 start---')
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_sm4(self):
        logger.info('----1.sm4加数据，密码为数字+小写字母----')
        sql_cmd1 = 'create table table001(name char(6),address text);' \
                   'insert into table001 values(\'lucy\',' \
                   'gs_encrypt(\'shanxi.xian,yantaqu0569-5\',' \
                   '\'wssx1234\',\'sm4\')),(\'张三\',\'shanxi.xian,' \
                   'yantaqu0569-5\'),(\'李四\',\'shanxi.大同,yantaqu0569-5\');'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(sql_msg1)
        self.assertTrue('The encryption key must be 8~16 bytes and contain '
                        'at least three kinds of characters' in sql_msg1)

    def tearDown(self):
        logger.info('----清理表----')
        sql_cmd1 = 'drop table table001;'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(sql_msg1)
        self.assertTrue('DROP TABLE')
        logger.info('----Opengauss_Function_Security_sm4_Case0004 finish----')
