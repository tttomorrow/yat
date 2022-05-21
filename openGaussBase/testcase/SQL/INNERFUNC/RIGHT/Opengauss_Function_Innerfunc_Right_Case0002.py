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
Case Name   : right函数入参是中文
Description : 
    1.创建不同编码格式的数据库
    2.分别在数据库中执行right函数对中文进行截取
Expect      : 
    1.创建成功
    2.函数返回结果正确
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
        logger.info("--------Opengauss_Function_Innerfunc_Right_Add_Case0002.py开始执行--------")
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_right(self):
        sql_cmd = [r'''SELECT right('我们是好人',0) AS RESULT;''',
                   r'''SELECT right('甘肃中滩',-1)AS RESULT;''',
                   r'''SELECT right('我们 是 好人啊啊啊',9) AS RESULT;''',
                   r'''SELECT right('甘肃 中滩',1)AS RESULT;''',
                   r'''SELECT right('甘肃 中滩',3)AS RESULT;''']
        result = ['', '肃中滩', '们 是 好人啊啊啊', '滩', '中滩']

        db_create = f"""drop database if exists aaa;
                        create database aaa encoding = 'utf-8';"""
        msg1 = self.commonsh.execut_db_sql(db_create)
        logger.info(msg1)
        self.assertTrue('CREATE' in msg1)

        for j in range(len(sql_cmd)):
            cmd1 = f'''source {self.DB_ENV_PATH};
                       gsql -d aaa -p {self.userNode.db_port} -c "{sql_cmd[j]}"'''
            msg2 = self.userNode.sh(cmd1).result()
            logger.info(msg2)
            self.assertTrue(msg2.splitlines()[-2].strip() == result[j])

        db_drop = f'''drop database aaa;'''
        msg3 = self.commonsh.execut_db_sql(db_drop)
        logger.info(msg3)
        self.assertTrue('DROP' in msg3)

    def tearDown(self):
        logger.info('--------Opengauss_Function_Innerfunc_Right_Add_Case0002.py执行结束--------')