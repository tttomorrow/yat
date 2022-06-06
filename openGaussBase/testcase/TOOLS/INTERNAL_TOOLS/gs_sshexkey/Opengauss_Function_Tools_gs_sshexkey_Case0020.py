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
Case Name   : root用户下，使用gs_sshexkey创建互信,指定--no-deduplicate
Description :
    1、创建hostfile,文件路径{dn1/hostfile},将环境IP写入文件hostfile
    2、向/etc/hosts文件中写入主备节点重复信息
    3、root用户下，执行创建互信命令，指定--no-deduplicate参数
       gs_sshexkey -f {dn1/hostfile} --no-deduplicate
    4、ssh添加的备机IP
    5、查看互信文件是否存在，查看/etc/hosts中节点信息
    6、清理环境、删除互信文件
Expect      :
    1、创建文件成功，添加IP成功
    2、写入节点重复信息成功
    3、执行gs_sshexkey命令成功
    4、ssh可直接连接到备机，互信建立成功
    5、互信文件存在，各节点信息存在至少两个
    6、清理环境成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf('Standby' not in primary_sh.get_db_cluster_status('detail'),
                 'Single node, and subsequent codes are not executed.')
class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryRoot')
        self.ssh_file = os.path.join(macro.DB_INSTANCE_PATH, 'hostfile')
        self.ssh_backup = os.path.join(macro.DB_INSTANCE_PATH, 'ssh_backup')
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        self.ssh_path = '~/.ssh'
        self.etc_path = '/etc/hosts'
        self.etc_path_bak = '/etc/hosts_bak'
        self.mapping_info = '   #Gauss OM IP Hosts Mapping'

        text = "---SetUp:检查数据库状态是否正常   expect:正常---"
        self.logger.info(text)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        "执行失败" + text)

        self.logger.info("------获取备节点ip------")
        shell_cmd = f"cat {self.conf_path} | " \
            f"grep 'replconninfo' | " \
            f"grep -Ev '^#' | " \
            f"tr -s ' '| " \
            f"cut -d ' ' -f 7 | " \
            f"cut -d '=' -f 2"
        self.logger.info(shell_cmd)
        msg = self.user_node.sh(shell_cmd).result()
        self.logger.info(msg)
        self.standby_ip_list = msg.splitlines()

    def cat_hosts(self, path, ip, ipflag=True):
        """
        定义一个函数，查看/etc/hosts中节点配置信息
        param="path":文件路径
        param="IP":待查看IP
        """
        if ipflag:
            cmd = f"cat {path} | grep {ip} | cut -d ' ' -f 1-3 | awk 'NR==1'"
        else:
            cmd = f"cat {path} | grep {ip}"
        self.logger.info(cmd)
        res = self.user_node.sh(cmd).result()
        self.logger.info(res)
        res += self.mapping_info
        return res

    def test_gs_sshexkey(self):
        self.logger.info("Opengauss_Function_Tools_gs_sshexkey_Case0020开始执行")
        self.logger.info("------前置条件:创建备份目录，备份互信文件------")
        self.logger.info("------主节点创建备份文件夹------")
        cmd = f'''mkdir {self.ssh_backup};ls {macro.DB_INSTANCE_PATH}'''
        self.logger.info(cmd)
        res = self.user_node.sh(cmd).result()
        self.logger.info(res)
        self.assertIn('ssh_backup', res)

        self.logger.info("------备节点创建备份文件夹------")
        for i in self.standby_ip_list:
            mk_cmd = f'''ssh {i} <<-EOF mkdir {self.ssh_backup}\n''' + "EOF"
            self.logger.info(mk_cmd)
            mk_res = self.user_node.sh(mk_cmd).result()
            self.logger.info(mk_res)
            self.logger.info("------查看备份文件夹是否创建成功------")
            ls_cmd = f'''ssh {i} <<-EOF ls {macro.DB_INSTANCE_PATH}\n''' \
                     + "EOF"
            self.logger.info(ls_cmd)
            ls_res = self.user_node.sh(ls_cmd).result()
            self.logger.info(ls_res)
            self.assertIn('ssh_backup', ls_res)

        self.logger.info("------主节点查看是否已存在互信文件，如有则备份------")
        check_cmd = f'ls {self.ssh_path}'
        primary_check_res = self.user_node.sh(check_cmd).result()
        self.logger.info(primary_check_res)

        if primary_check_res is not None:
            backup_cmd = f'''cp {self.ssh_path}/* {self.ssh_backup} &&
                ls {self.ssh_backup}'''
            self.logger.info(backup_cmd)
            backup_res = self.user_node.sh(backup_cmd).result()
            self.assertTrue('known_hosts' in backup_res)

        self.logger.info("------备节点查看是否已存在互信文件，如有则备份------")
        for i in self.standby_ip_list:
            standby_check_cmd = f'''ssh {i} <<-EOF ls {self.ssh_path}\n''' \
                                + "EOF"
            standby_check_res = self.user_node.sh(standby_check_cmd).result()
            self.logger.info(standby_check_res)
            self.assertTrue(standby_check_res)

            if standby_check_res is not None:
                    mv_cmd = f'''ssh {i} <<-EOF cp {self.ssh_path}/* \
                        {self.ssh_backup} && ls {self.ssh_backup}\n''' + "EOF"
                    self.logger.info(mv_cmd)
                    mv_res = self.user_node.sh(mv_cmd).result()
                    self.logger.info(mv_res)

        self.logger.info("---备份/etc/hosts文件---")
        hosts_bak = f'\cp {self.etc_path} {self.etc_path_bak} && ' \
            f'ls {self.etc_path_bak}'
        self.logger.info(hosts_bak)
        hosts_bak_res = self.user_node.sh(hosts_bak).result()
        self.logger.info(hosts_bak_res)
        self.assertTrue(self.etc_path_bak in hosts_bak_res.splitlines()[-1])

        text = "---step1:root用户下创建hostfile文件，添加主备IP信息;  expect:成功---"
        self.logger.info(text)
        add_cmd1 = f'''touch {self.ssh_file}
            echo -e '{self.user_node.db_host}' > {self.ssh_file}
            cat {self.ssh_file} | grep {self.user_node.db_host}'''
        self.logger.info(add_cmd1)
        add_res1 = self.user_node.sh(add_cmd1).result()
        self.assertTrue(self.user_node.db_host in add_res1, '执行失败' + text)

        for i in self.standby_ip_list:
            add_cmd2 = f'''echo -e '{i}' >> {self.ssh_file}
                cat {self.ssh_file}'''
            self.logger.info(add_cmd2)
            add_res2 = self.user_node.sh(add_cmd2).result()
            self.logger.info(add_res2)
            self.assertTrue(i in add_res2, '执行失败' + text)

        text = "---step2:向/etc/hosts文件中写入主备节点重复信息;   expect:成功---"
        self.logger.info(text)
        cat_res1 = self.cat_hosts(path=self.etc_path,
                                  ip=self.user_node.db_host)

        add_hosts1 = f'''echo -e '{cat_res1}' >> {self.etc_path}'''
        self.logger.info(add_hosts1)
        self.user_node.sh(add_hosts1).result()

        res_add_hosts1 = self.cat_hosts(path=self.etc_path,
                                        ip=self.user_node.db_host,
                                        ipflag=False)
        self.assertTrue(res_add_hosts1.count(self.user_node.db_host) >= 2,
                        '执行失败' + text)
        
        for i in self.standby_ip_list:
            cat_res2 = self.cat_hosts(path=self.etc_path, ip=i)
            self.logger.info(cat_res2)

            add_hosts2 = f'''echo -e '{cat_res2}' >> {self.etc_path}'''
            self.logger.info(add_hosts2)
            self.user_node.sh(add_hosts2).result()

            res_add_hosts2 = self.cat_hosts(path=self.etc_path, ip=i,
                                            ipflag=False)
            self.assertTrue(res_add_hosts2.count(i) >= 2, '执行失败' + text)

        text = "---step3:执行gs_sshexkey创建互信，指定--no-deduplicate " \
               "expect:创建互信成功，/etc/hosts中节点信息不去重---"
        self.logger.info(text)
        gs_cmd = f'''gs_sshexkey -f {self.ssh_file} \
            --skip-hostname-set --no-deduplicate'''
        execute_cmd = f'''source {macro.DB_ENV_PATH}
            expect <<EOF
            set timeout 300
            spawn {gs_cmd}
            expect "*assword:"
            send "{self.user_node.ssh_password}\\n"
            expect eof\n''' + '''EOF'''
        self.logger.info(execute_cmd)
        gs_res = self.user_node.sh(execute_cmd).result()
        self.logger.info(gs_res)
        self.assertIn('Successfully created SSH trust', gs_res)

        text = "------step4:ssh连接备机   expect:无需密码可正常连接------"
        self.logger.info(text)
        for i in self.standby_ip_list:
            ssh_cmd = f'''ssh {i} <<-EOF hostname\n''' + "EOF"
            self.logger.info(ssh_cmd)
            ssh_res = self.user_node.sh(ssh_cmd).result()
            self.logger.info(ssh_res)
            self.assertTrue('bash' not in ssh_res or
                            "can't be established" not in ssh_res)

        text = "---step5:查看互信文件是否存在，查看/etc/hosts中节点信息"\
               "expect:互信文件存在，/etc/hosts中存在节点信息>=2个"
        self.logger.info(text)
        check_cmd = f'cd {self.ssh_path} && ls'
        self.check_res = self.user_node.sh(check_cmd).result()
        self.logger.info(self.check_res)
        self.assertTrue(self.check_res)

        check_ip = self.cat_hosts(path=self.etc_path,
                                  ip=self.user_node.db_host,
                                  ipflag=False)
        self.assertTrue(check_ip.count(self.user_node.db_host) >= 2,
                        '执行失败' + text)

    def tearDown(self):
        self.logger.info("---step6:清理环境,删除hostfile文件,恢复原有互信文件;  expect:成功---")
        self.logger.info("---恢复原有/etc/hosts文件---")
        recov_hosts = f'cp {self.etc_path_bak} {self.etc_path} &&' \
            f'rm -rf {self.etc_path_bak} &&' \
            f'ls {self.etc_path_bak}'
        self.logger.info(recov_hosts)
        recov_hosts_res = self.user_node.sh(recov_hosts).result()
        self.logger.info(recov_hosts_res)

        rm_cmd1 = f'''rm -rf {self.ssh_path}/* &&
            rm -rf {self.ssh_file} &&
            rm -rf {macro.DB_INSTANCE_PATH}/gs_ssh* &&
            cp {self.ssh_backup}/*  {self.ssh_path}/ &&
            rm -rf {self.ssh_backup}'''
        self.logger.info(rm_cmd1)
        rm_res1 = self.user_node.sh(rm_cmd1).result()

        for i in self.standby_ip_list:
            rm_cmd2 = f'''ssh {i} <<EOF 
                rm -rf {self.ssh_path}/* &&
                rm -rf {self.ssh_file} &&
                cp {self.ssh_backup}/* {self.ssh_path}/ &&
                rm -rf {self.ssh_backup}
                ls {macro.DB_INSTANCE_PATH} | grep {self.ssh_file} &&
                ls {macro.DB_INSTANCE_PATH} | grep {self.ssh_backup}\n''' \
                + "EOF"
            self.logger.info(rm_cmd2)
            rm_res2 = self.user_node.sh(rm_cmd2).result()
            self.logger.info(rm_res2)
            self.assertTrue('bash' not in rm_res2 and
                            'hostfile' not in rm_res2 and
                            'ssh_backup' not in rm_res2)

        self.logger.info("Opengauss_Function_Tools_gs_sshexkey_Case0020执行结束")
        self.assertNotIn('bash', rm_res1)
        self.assertIn('No such file or directory',
                      recov_hosts_res.splitlines()[-1])
