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
Case Type   : 系统内部使用工具 gs_sshexkey
Case Name   : root用户下，使用gs_sshexkey创建互信,ip文件包含其他信息
Description :
    1、创建hostfile,文件路径{dn1/hostfile},将环境IP和其他信息写入文件hostfile
    2、root用户下，执行创建互信命令,gs_sshexkey -f {dn1/hostfile} -W {db_password}
    3、清理环境、删除互信文件
Expect      :
    1、创建文件成功，添加IP成功
    2、执行gs_sshexkey命令失败
    3、清理环境成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()
primary_sh = CommonSH('PrimaryDbUser')
ssh_file = os.path.join(macro.DB_INSTANCE_PATH, 'hostfile')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.commonsh = CommonSH('PrimaryDbUser')
        self.primary_node = Node('PrimaryRoot')
        self.standby_node = Node('Standby1Root')
        self.IP2 = self.standby_node.db_host
        self.IP1 = self.primary_node.db_host
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_gs_sshexkey(self):
        logger.info("Opengauss_Function_Tools_gs_sshexkey_Case0016开始执行")
        logger.info("======步驟1：普通用户下创建hostfile文件，添加主备IP&其他信息======")
        add_cmd = f'''touch {ssh_file}
            echo -e 'IP1:{self.IP1}\nIP2:{self.IP2}' > {ssh_file}
            cat {ssh_file} | grep {self.IP1}
            cat {ssh_file} | grep {self.IP2}
            '''
        logger.info(add_cmd)
        add_res = self.primary_node.sh(add_cmd).result()
        logger.info(add_res)
        self.assertTrue(self.IP1 in add_res and self.IP2 in add_res)

        logger.info("======步驟2：执行gs_sshexkey命令,失败======")
        gs_cmd = f'''source {macro.DB_ENV_PATH}
            gs_sshexkey -f {ssh_file}
            '''
        logger.info(gs_cmd)
        gs_res = self.primary_node.sh(gs_cmd).result()
        logger.info(gs_res)
        self.assertIn('The IP address is invalid', gs_res)

    def tearDown(self):
        logger.info("======步驟3：清理环境，删除hostfile文件======")
        rm_cmd = f'''rm -rf {ssh_file}'''
        logger.info(rm_cmd)
        rm_res = self.primary_node.sh(rm_cmd).result()
        self.assertNotIn('bash', rm_res)
        logger.info("===Opengauss_Function_Tools_gs_sshexkey_Case0016执行结束===")
