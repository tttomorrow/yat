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
Case Name   : 创建目录对象，路径不合法，合理报错
Description : 
    1.路径含特殊字符
    2.路径是相对路径
    3.路径是符号链接
Expect      : 
    1.目录创建失败
    2.目录创建失败
    3.目录创建失败
History     : 
"""

import unittest
import sys
import os
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info("--------Opengauss_Function_DDL_Create_Directory_Case0005.py开始执行--------")
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_INSTANCE_PATH

    def test_directory(self):
        logger.info('--------路径含特殊字符。路径是相对路径。路径是符号连接。--------')
        self.soft_link = [f"""rm -rf my_link""", f"""ln -s /tmp my_link"""]
        for i in range(2):
            msg = self.userNode.sh(self.soft_link[i]).result()
            logger.info(msg)
            self.assertTrue(len(msg.strip()) == 0)
        error_path = ['/&~?!tmp/', '../tmp/', '/my_link/']
        error_msg = ['illegal string: "&"',
                     'illegal string: "."',
                     'directory does not exist']
        for j in range(3):
            sql_cmd = "CREATE OR REPLACE DIRECTORY dir as '{}';".format(error_path[j])
            msg1 = self.commonsh.execut_db_sql(sql_cmd)
            logger.info(msg1)
            self.assertTrue(error_msg[j] in msg1)

    def tearDown(self):
        msg2 = self.userNode.sh(self.soft_link[0]).result()
        logger.info(msg2)
        logger.info('--------Opengauss_Function_DDL_Create_Directory_Case0005.py执行结束--------')