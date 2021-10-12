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
Case Name   : 测试copy非法字符容错，COMPATIBLE_ILLEGAL_CHARS参数为true
Description :
    1. 创建表,表数据copy to到一个文件
    2. COMPATIBLE_ILLEGAL_CHARS参数为true,传入非法字符到文件，然后copy from到表中
    3. 检查表内容
Expect      :
    1. 创建成功，copy to成功
    2. copy from成功，不报错
    3. 非法字符转空格或者?
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
        self.log.info('---Opengauss_Function_DML_Copy_Case0017开始---')

    def test_copy(self):
        self.log.info('---步骤1 创建表,表数据copy to到一个文件---')
        cmd0 = '''drop table if exists tb1;
                create table tb1(p3 varchar(25));
                insert into tb1 values ('hello'),('yo man'),('style');'''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('INSERT') > -1)
        self.log.info('创建一个文件,将表数据拷贝进来')
        self.file = os.path.join(macro.DB_INSTANCE_PATH, 'copy.txt')
        self.user.sh(f"touch {self.file}")
        cmd1 = f"copy tb1 to '{self.file}';delete from tb1;"
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.find('COPY 3') > -1)

        self.log.info('------步骤2 copy from文件中传入非法字符-------')
        illegal = [r'\0', 0xf5, 0Xf6, 0xf7, 0xf8, 0xf9]
        for i in range(6):
            char = illegal[i] if i == 0 else chr(illegal[i])
            cmd1 = f"echo '{char}' > {self.file}"
            self.log.info(cmd1)
            msg1 = self.user.sh(cmd1).result()
            self.log.info(msg1)

            cmd2 = f'''copy tb1 from '{self.file}' \
                       with(compatible_illegal_chars 'true');'''
            msg2 = self.commonsh.execut_db_sql(cmd2)
            self.log.info(msg2)
            self.assertTrue('ERROR' not in msg2)
            cmd3 = f"sed -i '$d' {self.file}"
            self.log.info(cmd3)
            msg3 = self.user.sh(cmd3).result()
            self.log.info(msg3)

        self.log.info('--步骤3 查看表内容，空格换行等均转了空格，其它字符转问号-')
        cmd4 = 'select * from tb1;'
        msg4 = self.commonsh.execut_db_sql(cmd4)
        self.log.info(msg4)
        lines = msg4.splitlines()
        self.assertTrue(lines[2].strip() == '')
        exp = b' \xc3\xb5\n \xc3\xb6\n \xc3\xb7\n'
        self.assertIn(exp, msg4.encode('UTF-8'))

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists tb1 cascade;')
        self.user.sh(f'rm -rf {self.file}')
        self.log.info('---Opengauss_Function_DML_Copy_Case0017结束---')