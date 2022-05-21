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
Case Name   : char_length函数入参是中文字符
Description : 
    1.使用char_length函数对中文字符进行处理
Expect      : 
    1.返回结果正确
History     : 
"""

import unittest
import sys
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

Log = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        Log.info('--Opengauss_Function_Innerfunc_Char_Length_Case0001开始--')
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_right(self):
        encoding = ['SQL_ASCII', 'UTF-8']
        sql_cmd = ["select char_length('   你!');",
                   "select char_length('你好');",
                   "select char_length('你说很高兴我能够遇见你aa@1');"]
        result = [["7", "6", "37"], ["5", "2", "15"]]

        for i in range(2):
            Log.info('----创建数据库----')
            db_create = f"""drop database if exists aaa;
                            create database aaa encoding = '{encoding[i]}';"""
            msg1 = self.commonsh.execut_db_sql(db_create)
            Log.info(msg1)
            self.assertTrue('CREATE' in msg1)
            Log.info('----连接新建的编码类型的库执行sql语句----')
            for j in range(len(sql_cmd)):
                cmd1 = f'''source {self.DB_ENV_PATH};
                           gsql -d aaa -p {self.userNode.db_port} \
                           -c "{sql_cmd[j]}"'''
                msg2 = self.userNode.sh(cmd1).result()
                Log.info(msg2)
                self.assertTrue(msg2.splitlines()[-2].strip() == result[i][j])
            Log.info('----删除数据库----')
            db_drop = f'drop database aaa;'
            msg3 = self.commonsh.execut_db_sql(db_drop)
            Log.info(msg3)
            self.assertTrue('DROP' in msg3)

    def tearDown(self):
        Log.info('-Opengauss_Function_Innerfunc_Char_Length_Case0001.py结束--')
