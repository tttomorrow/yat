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
Case Name   : instr函数入参是中文字符
Description : 
    1.使用instr函数对中文字符进行处理
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

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info("--Opengauss_Function_Innerfunc_Instr_Case0003.py开始执行--")
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_right(self):
        encoding = ['SQL_ASCII', 'UTF-8']
        sql_cmd = ["select instr('I am from一部测试组','m高',1,1);",
                   "select instr('数据库 一 部测试组','一 部',1,1);",
                   "SELECT instr('我和我的家乡','我',1,2)  from sys_dummy;"]
        result = [["0", "11", "7"], ["0", "5", "3"]]

        for i in range(2):
            logger.info('--创建数据库--')
            db_create = f'drop database if exists aaa;' \
                f'create database aaa encoding = \'{encoding[i]}\';'
            msg1 = self.commonsh.execut_db_sql(db_create)
            logger.info(msg1)
            self.assertTrue('CREATE' in msg1)
            logger.info('--连接新建的编码类型的库执行sql语句--')
            for j in range(len(sql_cmd)):
                cmd1 = f'source {self.DB_ENV_PATH};' \
                    f'gsql -d aaa -p {self.userNode.db_port}' \
                    f' -c "{sql_cmd[j]}" '
                msg2 = self.userNode.sh(cmd1).result()
                logger.info(msg2)
                self.assertTrue(msg2.splitlines()[-2].strip() == result[i][j])
            logger.info('--删除数据库--')
            db_drop = f'drop database aaa;'
            msg3 = self.commonsh.execut_db_sql(db_drop)
            logger.info(msg3)
            self.assertTrue('DROP' in msg3)

    def tearDown(self):
        logger.info('--Opengauss_Function_Innerfunc_Instr_Case0003.py执行结束--')
