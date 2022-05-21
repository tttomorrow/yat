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
Case Type   : CheckHandles
Case Name   : 在3节点查询句柄信息并打印
Description :
            1.获取打开句柄总数
            2.获取统计各进程打开句柄数
Expect      :
            1.获取打开句柄总数
            2.获取统计各进程打开句柄数
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from yat.test import Node


@unittest.skipIf(1 == CommonSH("PrimaryDbUser").get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class CheckHandles(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info("Opengauss_Function_Guc_Resolve_Problems_Case0001")
        self.common = Common()
        self.cmd1 = r"lsof|awk '{{print $2}}'|wc -l"
        self.cmd2 = r"lsof -n|awk '{{print $2}}'" \
                    r"|sort|uniq -c|sort -nr|head -10"
        self.cmd3 = r"for arg in `lsof -n|awk '{{print $2}}'|sort|uniq " \
                    r"-c|sort -nr|head -10|awk '{{print $2}}'`; " \
                    r"do echo $arg; ps -ef|grep $arg|grep -v grep; done"

        self.node_list = [Node("PrimaryRoot"), Node("Standby1Root"),
                          Node("Standby2Root")]

    def test_check_handles(self):
        for node in self.node_list:
            self.logger.info("***************************")
            self.logger.info(node.ssh_host)
            self.logger.info(f"打开句柄总数: ")
            self.common.get_sh_result(node, self.cmd1)

            self.logger.info(f"统计各进程打开句柄数: ")
            self.common.get_sh_result(node, self.cmd2)

            self.logger.info(f"for 循环执行结果: ")
            self.common.get_sh_result(node, self.cmd3)

        self.logger.info("**********************************************")