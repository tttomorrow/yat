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
Case Name   : 各主机间root互信状态不正常时检查操作系统
Description :
    1.创建备份~/.ssh/目录下的文件的目录：mkdir   /data/qumin226/cluster/dn1/ssh
    2.将~/.ssh/目录下的文件的移动到创建的目录下
    3.各主机间root互信状态不正常时检查操作系统：gs_checkos -i   A
    4.恢复互信：将备份的文件放回
Expect      :
    1.创建成功
    2.移动成功
    3.执行失败
    4.恢复互信成功
History     : 
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()
Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('---Opengauss_Function_Tools_gs_checkos_Case0009start---')
        self.ProotNode = Node('PrimaryRoot')
        self.PdbuserNode = Node('PrimaryDbUser')
        self.SrootNode = Node('Standby1Root')
        self.ssh_path = os.path.join(macro.DB_INSTANCE_PATH, 'ssh')

    def test_server_tools(self):
        LOG.info('----1.创建备份目录----')
        mkdir_cmd = f'''if [ -d {self.ssh_path} ]
                                then
                                    rm -rf {self.ssh_path};
                                fi
                                    mkdir {self.ssh_path};
                                '''
        LOG.info(mkdir_cmd)
        mkdir_result = self.ProotNode.sh(mkdir_cmd).result()
        LOG.info(mkdir_result)
        LOG.info('----校验是否创建成功备份目录：查看目录权限----')
        ls_cmd = f"ls -l {self.ssh_path}"
        LOG.info(ls_cmd)
        ls_result = self.ProotNode.sh(ls_cmd).result()
        LOG.info(ls_result)

        LOG.info('----2.备份~/.ssh目录下的文件----')
        mv_cmd1 = f'''mv /root/.ssh/*  {self.ssh_path};'''
        LOG.info(mv_cmd1)
        mv_result1 = self.ProotNode.sh(mv_cmd1).result()
        LOG.info(mv_result1)
        LOG.info('----校验是否成功备份目录下的文件：判断目录大小----')
        du_cmd2 = f'''du -h {self.ssh_path};'''
        LOG.info(du_cmd2)
        du_msg2 = self.ProotNode.sh(du_cmd2).result()
        LOG.info(du_msg2)
        dumsg2_list = du_msg2.split()[0]
        LOG.info(dumsg2_list)
        self.assertTrue(float(dumsg2_list[:-1]) > 0)
        LOG.info('----判断互信是否正常----')
        hostname_cmd = f'''hostname; '''
        hostname1 = self.SrootNode.sh(hostname_cmd).result()
        LOG.info(hostname1)

        ssh_cmd = f'''ssh {hostname1};'''
        ssh_msg = self.ProotNode.sh(ssh_cmd).result()
        LOG.info(ssh_msg)
        self.assertIn('Host key verification failed', ssh_msg)

        LOG.info('----3.互信状态不正常时检查操作系统:失败----')
        checkos_cmd = f'''source {macro.DB_ENV_PATH};
            expect <<EOF
            spawn  gs_checkos  -i  A  -h {hostname1};
            expect "*yes/no)"
            send "yes\\n"
            expect "*assword:"
            send "{self.SrootNode.ssh_password}\\n"
            expect eof\n''' + "EOF"

        LOG.info(checkos_cmd)
        checkos_msg = self.ProotNode.sh(checkos_cmd).result()
        LOG.info(checkos_msg)
        self.assertIn('Failed', checkos_msg)

        LOG.info('----4.恢复互信：将备份的文件放回----')
        mv_cmd2 = f'''mv {self.ssh_path}/*  /root/.ssh/ '''
        mv_result2 = self.ProotNode.sh(mv_cmd2).result()
        LOG.info(mv_result2)

        LOG.info('----查询数据库状态----')
        status_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om -t status --detail ;'
        LOG.info(status_cmd)
        status_msg = self.PdbuserNode.sh(status_cmd).result()
        LOG.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

    def tearDown(self):
        LOG.info('--------------需清理环境-------------------')
        clear_cmd = f'''source {macro.DB_ENV_PATH};
            rm -rf {self.ssh_path};
            '''
        LOG.info(clear_cmd)
        clear_msg = self.ProotNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('--Opengauss_Function_Tools_gs_checkos_Case0009finish--')