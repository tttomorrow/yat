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
Case Name   : 普通用户下，使用gs_sshexkey创建互信,指定--skip-hostname-set
Description :
    1、创建hostfile,文件路径{dn1/hostfile},将环境IP写入文件hostfile
    2、普通用户下，执行创建互信命令，指定--skip-hostname-set参数
       gs_sshexkey -f {dn1/hostfile} -W {db_password} --skip-hostname-set
    3、ssh添加的备机IP
    4、查看互信文件是否存在，查看/etc/hosts中是否存在IP与其hostname的映射关系
    5、清理环境、删除互信文件
Expect      :
    1、创建文件成功，添加IP成功
    2、执行gs_sshexkey命令成功
    3、ssh可直接连接到备机，互信建立成功
    4、互信文件存在，不存在映射关系
    5、清理环境成功
History     :
    删除备机ssh文件及断言
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()
primary_sh = CommonSH('PrimaryDbUser')
etc = '/etc/hosts'
etc_backup = '/etc/hosts_bak'
mapping = '#Gauss OM IP Hosts Mapping'


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.commonsh = CommonSH('PrimaryDbUser')
        self.root_primary_node = Node('PrimaryRoot')
        self.root_standby_node = Node('Standby1Root')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.IP2 = self.standby_node.db_host
        self.IP1 = self.primary_node.db_host
        self.ssh_file = os.path.join('/home',
                                     self.primary_node.ssh_user,
                                     'hostfile')
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("======获取备节点ip======")
        shell_cmd = f"cat {self.conf_path} | " \
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
        logger.info("======步驟1：普通用户下创建hostfile文件，添加主备IP信息======")
        add_cmd1 = f'''touch {self.ssh_file}
                       echo -e '{self.IP1}' > {self.ssh_file}
                       cat {self.ssh_file} | grep {self.IP1}'''
        logger.info(add_cmd1)
        add_res1 = self.primary_node.sh(add_cmd1).result()
        self.assertTrue(self.IP1 in add_res1)

        for i in self.standby_ip_list:
            add_cmd2 = f'''echo -e '{i}' >> {self.ssh_file}
                           cat {self.ssh_file}'''
            logger.info(add_cmd2)
            add_res2 = self.primary_node.sh(add_cmd2).result()
            logger.info(add_res2)
            self.assertTrue(i in add_res2)

        logger.info("======备份/etc/hosts,且清理/etc/hosts文件中的映射关系======")
        backup_etc = f'''cp {etc} {etc_backup}'''
        logger.info(backup_etc)
        back_res = self.root_primary_node.sh(backup_etc).result()
        logger.info(back_res)

        for i in self.standby_ip_list:
            clear_cmd = f'''sed -i "/{i}/d" {etc}'''
            clear_res1 = self.root_primary_node.sh(clear_cmd).result()
            logger.info(clear_res1)

        logger.info("======步驟2：执行gs_sshexkey命令======")
        gs_cmd = f'''gs_sshexkey -f {self.ssh_file} --skip-hostname-set'''
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
        self.standby_hostname = self.standby_node.sh('hostname').result()
        self.assertEqual(self.standby_hostname, ssh_res.split('\n')[-1])

        logger.info("======步驟4：查看/etc/hosts文件中是否存在IP与hostname映射关系======")
        for i in self.standby_ip_list:
            cat_cmd = f'''cat {etc} | grep {i}'''
            cat_res = self.primary_node.sh(cat_cmd).result()
            logger.info(cat_res)
            self.assertEqual('', cat_res)

        logger.info("======查看互信文件是否存在======")
        check_cmd = 'cd ~/.ssh;ls'
        self.check_res = self.primary_node.sh(check_cmd).result()
        logger.info(self.check_res)
        self.assertTrue(self.check_res)

    def tearDown(self):
        logger.info("======步驟5：清理环境======")
        logger.info("======恢复环境原有映射关系======")
        backup_etc = f'''mv {etc_backup} {etc};ls {etc};chmod 755 {etc};'''
        logger.info(backup_etc)
        back_res = self.root_primary_node.sh(backup_etc).result()
        logger.info(back_res)
        logger.info("======重新建立用户互信======")
        gs_cmd = f'''gs_sshexkey -f {self.ssh_file} --skip-hostname-set'''
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
        logger.info("======删除hostfile文件======")
        rm_cmd1 = f'''rm -rf {self.ssh_file}'''
        rm_res1 = self.primary_node.sh(rm_cmd1).result()
        self.assertIn('Successfully created SSH trust', gs_res)
        self.assertNotIn('bash', rm_res1)
        self.assertIn(etc, back_res)
        logger.info(f"====={os.path.basename(__file__)}执行结束=====")
