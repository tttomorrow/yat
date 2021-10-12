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
Case Type   : 函数与操作符-字符处理函数和操作符
Case Name   : btrim函数处理中文字符
Description : 描述
    步骤1：对数据库编码格式进行设置，使用utf8
    步骤2：执行sql语句，btrim函数入参给中文字符串
Expect      : 
    步骤1：编码格式设置成功
    步骤2：btrim函数对中文字符串处理成功
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Function(unittest.TestCase):

    def setUp(self):
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')
        self.log = Logger()
        self.log.info('---Opengauss_Function_Innerfunc_Btrim_Case0006开始---')

    def test_Btrim(self):
        self.log.info('------------execute sql -----------')
        cmd1 = self.commonsh.execut_db_sql('''drop database if exists ddd;
            create database ddd encoding 'utf8';
            ''')
        self.log.info(cmd1)

        cmd2 = '''select btrim(\
            '函数和操作符、几何函数和操作符、网络地址函数和操作符','操作符函数');
            '''
        cmd3 = f'''source {macro.DB_ENV_PATH};
            gsql -d ddd -p {self.user.db_port} -c "{cmd2}"
            '''
        self.log.info(cmd3)
        msg2 = self.user.sh(cmd3).result()
        self.log.info(msg2)
        self.assertTrue(msg2.splitlines()[2].strip() ==
            "和操作符、几何函数和操作符、网络地址函数和")

    def tearDown(self):
        cmd = self.commonsh.execut_db_sql('drop database ddd;')
        self.log.info(cmd)
        self.log.info('---Opengauss_Function_Innerfunc_Btrim_Case0006结束---')