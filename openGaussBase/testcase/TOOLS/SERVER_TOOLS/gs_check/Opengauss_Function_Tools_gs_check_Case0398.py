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
Case Type   : 服务端工具
Case Name   : 检查CPU使用率的同时检查防火墙(root类检查项)
Description :
     1.检查CPU使用率的同时检查防火墙(root类检查项)
Expect      :
     1.检查完成
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Tools(unittest.TestCase):

    def setUp(self):
        logger.info('----Opengauss_Function_Tools_gs_check_Case0398start----')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('-------检查CPU使用率的同时检查防火墙(root类检查项)-------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            expect <<EOF
            set timeout -1
            spawn gs_check -i  CheckCPU,CheckFirewall
            expect "*]:"
            send "{self.rootNode.ssh_user}\r"
            expect "*]:"
            send "{self.rootNode.ssh_password}\r"
            expect eof\n''' + "EOF"
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in msg1 or
                self.Constant.GS_CHECK_SUCCESS_MSG2[1] in msg1) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in msg1
        self.assertTrue(flag)

    def tearDown(self):
        logger.info('--------------需清理环境-------------------')
        clear_cmd = f'rm -rf /tmp/check*;' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/../tool/script/gspylib' \
            f'/inspection/output/CheckReport*;'
        logger.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        logger.info(clear_msg)
        logger.info('-----------------产生的文件清理完成------------------')
        logger.info(
            '------Opengauss_Function_Tools_gs_check_Case0398finish------')
