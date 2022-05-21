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
Case Name   : gs_dump导出加密后的数据
Description :
    1.创建表table001；
    2.表中插入数据，对address字段加密
    3.gs_dump导出表table001,查看导出的数据，是否加密
Expect      :
    1.创表成功
    2.数据插入完成
    3.导出成功，lucy对应的address显示加密后的密文
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_sm4_Case0002 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.dump_file = os.path.join(macro.DB_INSTANCE_PATH, 'table001.sql')

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
        logger.info('-----3.gs_dump导出表table001,查看导出的数据，是否加密-----')
        exe_cmd3 = f'source {self.DB_ENV_PATH};' \
                   f'gs_dump -f {self.dump_file} -p {self.userNode.db_port} ' \
                   f'{self.userNode.db_name} -t table001 -F p;'
        logger.info(exe_cmd3)
        exe_msg2 = self.userNode.sh(exe_cmd3).result()
        logger.info(exe_msg2)
        exe_cmd3 = f'cat {self.dump_file}'
        exe_msg3 = self.userNode.sh(exe_cmd3).result()
        logger.info(exe_msg3)
        self.assertTrue(sql_msg2_list[2].strip() in exe_msg3)

    def tearDown(self):
        logger.info('-------1.清理表------')
        sql_cmd1 = 'drop table table001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.find('DROP TABLE') > -1)
        logger.info('-------2.删除生成的文件------')
        exe_cmd2 = f'rm -rf {self.dump_file}'
        logger.info(exe_cmd2)
        msg2 = self.userNode.sh(exe_cmd2).result()
        logger.info(msg2)
        exe_cmd3 = f'ls {self.dump_file}'
        logger.info(exe_cmd3)
        msg3 = self.userNode.sh(exe_cmd3).result()
        logger.info(msg3)
        self.assertTrue(msg3.find('No such file or directory') > -1)
        logger.info('----Opengauss_Function_Security_sm4_Case0002 finish----')