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

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info(f"-----{os.path.basename(__file__)}开始执行-----")
        self.commonsh = CommonSH("dbuser")
        self.userNode = Node("dbuser")
        self.link_path = os.path.join("/home", f"{self.userNode.ssh_user}",
                                      "my_link0005")

    def test_directory(self):
        text = "-----前置准备 创建符号链接-----"
        logger.info(text)
        self.soft_link = [f"rm -rf {self.link_path}",
                          f"ln -s /tmp {self.link_path}"]
        for i in range(2):
            msg = self.userNode.sh(self.soft_link[i]).result()
            logger.info(msg)
            self.assertTrue(len(msg.strip()) == 0, "执行失败" + text)

        text = "-----step1+2+3:路径含特殊字符/路径是相对路径/路径是符号连接;expect:-----"
        logger.info(text)
        error_path = ["/&~?!tmp/", "../tmp/", f"{self.link_path}"]
        error_msg = ['illegal string: "&"',
                     "ERROR:  directory path cannot be relative",
                     "is not a directory, please check"]
        for j in range(3):
            sql_cmd = f"create or replace directory dir as '{error_path[j]}';"
            msg1 = self.commonsh.execut_db_sql(sql_cmd)
            logger.info(msg1)
            self.assertTrue(error_msg[j] in msg1, "执行失败" + text)

    def tearDown(self):
        text = "清理环境"
        logger.info(text)
        result = self.userNode.sh(self.soft_link[0]).result()
        logger.info(result)
        self.assertTrue(len(result.strip()) == 0, "执行失败" + text)
        logger.info(f"-----{os.path.basename(__file__)}执行结束-----")