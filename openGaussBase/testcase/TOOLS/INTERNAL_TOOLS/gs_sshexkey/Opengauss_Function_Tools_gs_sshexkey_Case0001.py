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
Case Type   : 系统内部使用工具 gs_sshexkey
Case Name   : root用户下，使用gs_sshexkey对一主一备创建互信
Description :
    1、创建hostfile,文件路径{dn1/hostfile},将环境IP写入文件hostfile
    2、root用户下，执行gs_sshexkey -f {dn1/hostfile}
    3、ssh添加的备机IP
    4、查看互信文件是否存在
    5、清理环境、删除互信文件
Expect      :
    1、创建文件成功，IP写入hostfile成功
    2、执行gs_sshexkey命令成功
    3、ssh可直接连接到备机，互信建立成功
    4、互信文件存在
    5、清理环境成功
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
conf_path = os.path.join(macro.DB_INSTANCE_PATH, macro.DB_PG_CONFIG_NAME)


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.primary_node = Node('PrimaryRoot')
        self.IP1 = self.primary_node.db_host
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("======获取备节点ip======")
        shell_cmd = f"cat {conf_path} | " \
            f"grep 'replconninfo' | " \
            f"grep -Ev '^#' | " \
            f"tr -s ' '| " \
            f"cut -d ' ' -f 7 | " \
            f"cut -d '=' -f 2"
        logger.info(shell_cmd)
        msg = self.primary_node.sh(shell_cmd).result()
        logger.info(msg)
        self.standby_ip_list = msg.splitlines()

    def test_gs_sshexkey(self):
        logger.info(f"====={os.path.basename(__file__)}开始执行=====")
        logger.info("======步驟1：root用户下创建hostfile文件，添加主备IP信息======")
        add_cmd1 = f'''touch {ssh_file}
            echo -e '{self.IP1}' > {ssh_file}
            cat {ssh_file} | grep {self.IP1}'''
        logger.info(add_cmd1)
        add_res1 = self.primary_node.sh(add_cmd1).result()
        self.assertTrue(self.IP1 in add_res1)

        for i in self.standby_ip_list:
            add_cmd2 = f'''echo -e '{i}' >> {ssh_file}
                cat {ssh_file}'''
            logger.info(add_cmd2)
            add_res2 = self.primary_node.sh(add_cmd2).result()
            self.assertTrue(i in add_res2)

        logger.info("======步驟2：执行gs_sshexkey命令======")
        gs_cmd = f'''gs_sshexkey -f {ssh_file}'''
        execute_cmd = f'''source {macro.DB_ENV_PATH}
            expect <<EOF
            set timeout 300
            spawn {gs_cmd}
            expect "*assword:"
            send "{self.primary_node.ssh_password}\\n"
            expect eof\n''' + '''EOF'''
        logger.info(execute_cmd)
        gs_res = self.primary_node.sh(execute_cmd).result()
        logger.info(gs_res)
        self.assertIn('Successfully created SSH trust', gs_res)

        logger.info("======步驟3：ssh连接备机，无需密码可正常连接======")
        for i in self.standby_ip_list:
            ssh_cmd = f'''ssh {i} <<-EOF hostname\n''' + "EOF"
            logger.info(ssh_cmd)
            ssh_res = self.primary_node.sh(ssh_cmd).result()
            logger.info(ssh_res)
            self.assertTrue('bash' not in ssh_res or
                            "can't be established" not in ssh_res)

        logger.info("======步驟4：查看互信文件是否存在======")
        check_cmd = 'ls ~/.ssh'
        self.check_res = self.primary_node.sh(check_cmd).result()
        logger.info(self.check_res)
        self.assertTrue(self.check_res)

    def tearDown(self):
        logger.info("======步驟5：清理环境，删除hostfile文件======")
        logger.info("======备节点清理环境======")
        for i in self.standby_ip_list:
            logger.info("======删除hostfile文件======")
            rm_cmd1 = f'''ssh {i} <<EOF rm -rf {ssh_file}\n''' + "EOF"
            logger.info(rm_cmd1)
            rm_res1 = self.primary_node.sh(rm_cmd1).result()
            logger.info(rm_res1)

        logger.info("======主节点清理环境======")
        rm_cmd3 = f'''rm -rf {ssh_file}'''
        logger.info(rm_cmd3)
        rm_res3 = self.primary_node.sh(rm_cmd3).result()
        logger.info(rm_res3)
        logger.info(f"====={os.path.basename(__file__)}执行结束=====")
