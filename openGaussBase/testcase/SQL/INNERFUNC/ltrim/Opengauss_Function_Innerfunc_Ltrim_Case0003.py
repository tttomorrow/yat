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
Case Type   : 功能测试
Case Name   : ltrim函数入参是中文
Description : 
    1.创建不同编码格式的数据库
    2.分别在数据库中执行ltrim函数对中文进行截取
Expect      : 
    1.创建成功
    2.函数返回结果正确
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.log.info("----Opengauss_Function_Innerfunc_Ltrim_Case0003开始----")

    def test_ltrim(self):
        sql_cmd = ["select ltrim('大江大河','我');",
                   "select ltrim('大江大河','大');",
                   "select ltrim('大江大河','江');",
                   "select ltrim('大江大河','河');"]
        result = ['大江大河', '江大河', '大江大河', '大江大河']

        db_create = f"""drop database if exists aaa;
                        create database aaa encoding = 'sql_ascii';"""
        msg1 = self.commonsh.execut_db_sql(db_create)
        self.log.info(msg1)
        self.assertTrue('CREATE' in msg1)

        for j in range(4):
            cmd1 = f'''source {self.DB_ENV_PATH};
                       gsql -d aaa -p {self.user.db_port} -c "{sql_cmd[j]}"'''
            msg2 = self.user.sh(cmd1).result()
            self.log.info(msg2)
            self.assertTrue(msg2.splitlines()[-2].strip() == result[j])

        db_drop = f'''drop database aaa;'''
        msg3 = self.commonsh.execut_db_sql(db_drop)
        self.log.info(msg3)
        self.assertTrue('DROP' in msg3)

    def tearDown(self):
        self.log.info("----Opengauss_Function_Innerfunc_Ltrim_Case0003结束----")
