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
Case Name   : 普通用户下，使用gs_sshexkey创建互信,-l指定日志路径(无权限)
Description :
    1、创建hostfile,文件路径{dn1/hostfile},将环境IP写入文件hostfile
    2、普通用户下，执行创建互信命令,添加-l参数指定日志路径
       gs_sshexkey -f {dn1/hostfile} -W {db_password} -l {dn1/logfile}(无权限)
    3、清理环境、删除互信文件
Expect      :
    1、创建文件成功，添加IP成功
    2、执行gs_sshexkey命令失败,无法创建日志文件
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
ssh_log = os.path.join(macro.DB_INSTANCE_PATH, 'gs_log/gs_sshexkey.log')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.commonsh = CommonSH('PrimaryDbUser')
        self.root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.IP2 = self.standby_node.db_host
        self.IP1 = self.primary_node.db_host
        self.ssh_file = os.path.join('/home',
                                     self.primary_node.ssh_user,
                                     'hostfile')
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_gs_sshexkey(self):
        logger.info(f"====={os.path.basename(__file__)}开始执行=====")
        logger.info("======步驟1：普通用户下创建hostfile文件，添加主备IP信息======")
        add_cmd = f'''touch {self.ssh_file}
            echo -e '{self.IP1}\n{self.IP2}' > {self.ssh_file}
            cat {self.ssh_file} | grep {self.IP1}
            cat {self.ssh_file} | grep {self.IP2}
            '''
        logger.info(add_cmd)
        add_res = self.primary_node.sh(add_cmd).result()
        logger.info(add_res)
        self.assertTrue(self.IP1 in add_res and self.IP2 in add_res)

        logger.info("======创建log无权限路径======")
        mk_cmd = f'''mkdir {macro.DB_INSTANCE_PATH}/gs_log'''
        self.root_node.sh(mk_cmd)

        logger.info("======步驟2：执行gs_sshexkey命令======")
        gs_cmd = f'''gs_sshexkey -f {self.ssh_file} -l {ssh_log}'''
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
        self.assertIn('Permission denied', gs_res)

    def tearDown(self):
        logger.info("======步驟3：清理环境，删除hostfile文件&log文件======")
        rm_cmd1 = f'''rm -rf {self.ssh_file}'''
        logger.info(rm_cmd1)
        rm_res1 = self.primary_node.sh(rm_cmd1).result()
        rm_res2 = self.standby_node.sh(rm_cmd1).result()
        self.assertNotIn('bash', rm_res1)
        self.assertNotIn('bash', rm_res2)

        rm_cmd2 = f'''rm -rf {macro.DB_INSTANCE_PATH}/gs_log'''
        logger.info(rm_cmd2)
        self.root_node.sh(rm_cmd2).result()
        logger.info(f"====={os.path.basename(__file__)}执行结束=====")
