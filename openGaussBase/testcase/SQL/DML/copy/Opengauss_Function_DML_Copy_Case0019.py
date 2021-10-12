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
Case Type   : 功能测试
Case Name   : 测试copy非法字符容错，COMPATIBLE_ILLEGAL_CHARS参数为false
Description :
    1. 创建表,表数据copy to到一个文件
    2. COMPATIBLE_ILLEGAL_CHARS参数为false,写入非法字符到文件，copy from到表中
    3. 检查表内容
Expect      :
    1. 创建成功，copy to成功
    2. copy from导入时遇到非法字符进行报错，中断导入
    3. 换行转了空格，其它字符报错未导入
History     : 
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.log.info('---Opengauss_Function_DML_Copy_Case0019开始---')

    def test_copy(self):
        self.log.info('---步骤1 创建表---')
        cmd0 = '''drop table if exists tb1;
                create table tb1(p3 varchar(25));
                insert into tb1 values ('hello'),('yo man'),('style');'''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('INSERT') > -1)
        self.log.info('创建一个文件,将表数据拷贝进来')
        self.file = os.path.join(macro.DB_INSTANCE_PATH, 'copy.txt')
        self.user.sh(f'rm -rf {self.file};touch {self.file}')
        cmd1 = f"copy tb1 to '{self.file}';delete from tb1;"
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.find('COPY 3') > -1)

        self.log.info('------步骤2 copy from文件中传入非法字符-------')
        illegal = [r'\0', r'\0x3', r'\0x9f', r'\0x81']
        er_info = 'ERROR:  invalid byte sequence'
        for i in range(4):
            cmd1 = f"echo '{illegal[i]}' > {self.file}"
            self.log.info(cmd1)
            msg1 = self.user.sh(cmd1).result()
            self.log.info(msg1)

            cmd2 = f"copy tb1 from '{self.file}' " \
                f"with(compatible_illegal_chars 'false');"
            msg2 = self.commonsh.execut_db_sql(cmd2)
            self.log.info(msg2)
            self.assertTrue(er_info in msg2)

            cmd4 = f"sed -i '$d' {self.file}"
            self.log.info(cmd4)
            msg4 = self.user.sh(cmd4).result()
            self.log.info(msg4)

        self.log.info('----步骤3 查看表内容，非法字符报错未导入----')
        cmd3 = 'select * from tb1;'
        msg3 = self.commonsh.execut_db_sql(cmd3)
        self.log.info(msg3)
        lines = msg3.splitlines()
        self.assertTrue(lines[-1].strip() == '(0 rows)')

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists tb1 cascade;')
        self.user.sh(f'rm -rf {self.file}')
        self.log.info('---Opengauss_Function_DML_Copy_Case0019结束---')