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
Case Name   : 字符处理函数translate对特殊字符进行处理
Description : 
    1.创建不同编码格式的数据库
    2.分别在数据库中执行translate函数进行转换
Expect      : 
    1.创建成功
    2.转换成功
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
        logger.info("--------Opengauss_Function_Innerfunc_Translate_Case0010.py开始执行--------")
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_right(self):
        encoding = ['SQL_ASCII', 'UTF-8']
        sql_cmd = ["select translate(case when 1>0 then lower('Ａｂｃ')end,'ａAbc','一二三四');",
                   "select translate('お帰りなさい。','おり','真的');",
                   "select translate('お帰りなさい。','お','真的');",
                   "select translate('お帰りなさい。','お','');",
                   "select translate('真多お帰りなさい。','真多','お帰');",
                   "select translate('×××&&&&￥(((())))お帰りなさい。','×××&&&&￥(((())))','abcdefghijk');",
                   "select translate('×××&&&&￥(((())))お帰りなさい。abc','abc×××&&&&￥())))','(((');"]
        result = [['伡丂七', '真帰皟眪眕眄瀚', '真帰炟眪眕眄瀂', '',
                   'お帰お帰りなさい。', 'abababggggkお帰りなさい。', 'お帰りなさい。((('],
                  ['Ａｂｃ', '真帰的なさい。', '真帰りなさい。', '',
                   'お帰お帰りなさい。', 'aaaddddhiiiiお帰りなさい。', 'お帰りなさい。(((']]

        for i in range(2):
            # 创建数据库
            db_create = f"""drop database if exists aaa;
                            create database aaa encoding = '{encoding[i]}';"""
            msg1 = self.commonsh.execut_db_sql(db_create)
            logger.info(msg1)
            self.assertTrue('CREATE' in msg1)
            for j in range(len(sql_cmd)):
                # 连接新建的编码类型的库执行sql语句
                cmd1 = f'''source {self.DB_ENV_PATH};
                           gsql -d aaa -p {self.userNode.db_port} -c "{sql_cmd[j]}"'''
                msg2 = self.userNode.sh(cmd1).result()
                logger.info(msg2)
                self.assertTrue(msg2.splitlines()[-2].strip() == result[i][j])
            # 删除数据库
            db_drop = f'''drop database aaa;'''
            msg3 = self.commonsh.execut_db_sql(db_drop)
            logger.info(msg3)
            self.assertTrue('DROP' in msg3)

    def tearDown(self):
        logger.info('--------Opengauss_Function_Innerfunc_Translate_Case0010.py执行结束--------')