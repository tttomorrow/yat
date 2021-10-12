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
Case Name   : 普通用户下，使用gs_sshexkey对一主一备创建互信
Description :
    1、创建hostfile,文件路径{dn1/hostfile},将环境IP写入文件hostfile
       touch {dn1/hostfile}
       chmod -R 755 {dn1/hostfile}
       echo -e '{IP1\nIP2}' {dn1/hostfile}
    2、普通用户下，执行gs_sshexkey -f {dn1/hostfile} -W {db_password}
    3、ssh添加的备机IP
    4、查看互信文件是否存在
    5、清理环境、删除互信文件
Expect      :
    1、创建文件成功，添加IP成功
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


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.commonsh = CommonSH('PrimaryDbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.IP2 = self.standby_node.db_host
        self.IP1 = self.primary_node.db_host
        self.ssh_file = os.path.join('/home',
                                     self.primary_node.ssh_user,
                                     'hostfile')
        self.ssh_backup = os.path.join('/home',
                                       self.primary_node.ssh_user,
                                       'ssh_backup')
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_gs_sshexkey(self):
        logger.info("Opengauss_Function_Tools_gs_sshexkey_Case0005开始执行")
        logger.info("======创建备份目录======")
        mk_cmd = f'''mkdir {self.ssh_backup}'''
        mk_res1 = self.primary_node.sh(mk_cmd).result()
        mk_res2 = self.standby_node.sh(mk_cmd).result()
        logger.info(mk_res1)
        logger.info(mk_res2)

        logger.info("======查看是否已存在互信文件，如有则备份======")
        check_cmd = 'ls ~/.ssh'
        check_res = self.primary_node.sh(check_cmd).result()
        logger.info(check_res)
        if check_res is not None:
            mv_cmd = f'''mv ~/.ssh/* {self.ssh_backup};ls {self.ssh_backup}'''
            self.primary_node.sh(mv_cmd)
            self.standby_node.sh(mv_cmd)
        check_res = self.primary_node.sh(check_cmd).result()
        logger.info(check_res)

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

        logger.info("======步驟2：执行gs_sshexkey命令======")
        gs_cmd = f'''gs_sshexkey -f {self.ssh_file}'''
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
        ssh_cmd = f'''ssh {self.IP2} <<-EOF hostname\n''' + "EOF"
        logger.info(ssh_cmd)
        ssh_res = self.primary_node.sh(ssh_cmd).result()
        logger.info(ssh_res)
        standby_hostname = self.standby_node.sh('hostname').result()
        self.assertEqual(standby_hostname, ssh_res.split('\n')[-1])

        logger.info("======步驟4：查看互信文件是否存在======")
        check_cmd = 'cd ~/.ssh;ls'
        self.check_res = self.primary_node.sh(check_cmd).result()
        logger.info(self.check_res)
        self.assertTrue(self.check_res)

    def tearDown(self):
        logger.info("======步驟5：清理环境，删除hostfile文件======")
        rm_cmd1 = f'''rm -rf ~/.ssh/*;rm -rf {self.ssh_file}'''
        logger.info(rm_cmd1)
        rm_res1 = self.primary_node.sh(rm_cmd1).result()
        rm_res2 = self.standby_node.sh(rm_cmd1).result()
        self.assertNotIn('bash', rm_res1)
        self.assertNotIn('bash', rm_res2)

        logger.info("======恢复环境原有互信关系======")
        gs_cmd = f'''cp {self.ssh_backup}/* ~/.ssh/
            rm -rf {self.ssh_backup}'''
        logger.info(gs_cmd)
        gs_res1 = self.primary_node.sh(gs_cmd).result()
        gs_res2 = self.standby_node.sh(gs_cmd).result()
        self.assertNotIn('bash', gs_res1)
        self.assertNotIn('bash', gs_res2)
        logger.info("===Opengauss_Function_Tools_gs_sshexkey_Case0005执行结束===")
