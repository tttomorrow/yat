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
Case Name   : root用户下，使用gs_sshexkey创建互信,-l指定日志路径
Description :
    1、创建hostfile,文件路径{dn1/hostfile},将环境IP写入文件hostfile
    2、root用户下，执行创建互信命令,添加-l参数指定日志路径
       gs_sshexkey -f {dn1/hostfile} -l {dn1/logfile}
    3、清理环境、删除互信文件
Expect      :
    1、创建文件成功，添加IP成功
    2、执行gs_sshexkey命令成功，输出写入日志中
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
ssh_log = os.path.join(macro.DB_INSTANCE_PATH, 'gs_sshexkey.log')
conf_path = os.path.join(macro.DB_INSTANCE_PATH, macro.DB_PG_CONFIG_NAME)


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.commonsh = CommonSH('PrimaryDbUser')
        self.primary_node = Node('PrimaryRoot')
        self.IP1 = self.primary_node.db_host
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
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
            logger.info(add_res2)
            self.assertTrue(i in add_res2)

        logger.info("======步驟2：执行gs_sshexkey命令,指定日志路径======")
        gs_cmd = f'''gs_sshexkey -f {ssh_file} -l {ssh_log}'''
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

        logger.info("======查看是否生成log文件及是否有内容======")
        cat_cmd = f'''cat {macro.DB_INSTANCE_PATH}/gs_ssh* | \
            grep "Successfully created SSH trust"'''
        cat_res = self.primary_node.sh(cat_cmd).result()
        self.assertIn('Successfully created SSH trust', cat_res)

    def tearDown(self):
        logger.info("======步驟3：清理环境，删除hostfile文件&log文件&恢复环境原有互信关系======")
        logger.info("======备节点清理环境======")
        for i in self.standby_ip_list:
            logger.info("======删除hostfile文件======")
            rm_cmd1 = f'''ssh {i} <<EOF rm -rf {ssh_file}\n''' + "EOF"
            logger.info(rm_cmd1)
            rm_res1 = self.primary_node.sh(rm_cmd1).result()
            logger.info(rm_res1)

            logger.info("======清理生成的日志信息======")
            rm_cmd3 = f'''ssh {i} <<EOF rm -rf 
                {macro.DB_INSTANCE_PATH}/gs_ssh* \n''' + "EOF"
            logger.info(rm_cmd3)
            rm_res3 = self.primary_node.sh(rm_cmd3).result()
            logger.info(rm_res3)

        logger.info("======主节点清理环境======")
        rm_cmd4 = f'''rm -rf {ssh_file}'''
        logger.info(rm_cmd4)
        rm_res4 = self.primary_node.sh(rm_cmd4).result()
        logger.info(rm_res4)

        rm_cmd6 = f'''rm -rf {macro.DB_INSTANCE_PATH}/gs_ssh*'''
        logger.info(rm_cmd6)
        rm_res6 = self.primary_node.sh(rm_cmd6).result()
        logger.info(rm_res6)
        logger.info(f"====={os.path.basename(__file__)}执行结束=====")


