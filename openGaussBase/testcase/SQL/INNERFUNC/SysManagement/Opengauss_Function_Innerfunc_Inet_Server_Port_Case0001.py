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
Case Type   : 功能测试
Case Name   : 远程连接模式下返回接收当前连接的端口号
Description :
    1.远程状态，执行命令select inet_server_port();
Expect      :
    1.返回接收当前连接的端口号
History     :
"""
import os
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Innerfunc_'
                      'Inet_Server_Port_Case0001开始--')
        self.commonsh = CommonSH('PrimaryDbUser')
        self.client = Node('PrimaryDbUser')
        self.client_ip = self.client.db_host
        status = self.commonsh.get_db_cluster_status('detail')
        # 适配主备环境，主备下主机作client备机server,单机的话主机也作server
        if 'Standby' in status:
            self.server = Node('Standby1Root')
            self.server_ip = self.server.db_host
            self.server_port = self.server.db_port
        else:
            self.server = self.client
            self.server_ip = self.client.db_host
            self.server_port = self.client.db_port

    def test_inet(self):
        self.log.info('在备机(服务端)的pg_hba里写进主机的连接方式为sha256')
        pg_hba = os.path.join(macro.DB_INSTANCE_PATH, macro.PG_HBA_FILE_NAME)
        sline = f"cat {pg_hba}|grep -n 'local'|grep -n 'all'" \
            f"|grep -n 'trust'|grep -v '#'|cut -d ':' -f 3"
        self.log.info(sline)
        msg1 = self.server.sh(sline).result()
        self.log.info(msg1)
        line = msg1.strip()

        item = f"sed -i '{int(line) + 1}i host {self.client.db_name} " \
            f"{self.client.db_user} {self.client_ip}/32 sha256' $d{pg_hba}"
        self.log.info(item)
        msg2 = self.server.sh(item).result()
        self.log.info(msg2)

        try:
            cmd = 'select inet_server_port();'
            cmd1 = f'''source {macro.DB_ENV_PATH};
                gsql -d {self.client.db_name} -h {self.server_ip} \
                -U {self.client.db_user} -W {self.client.db_password} \
                -p {self.client.db_port} -c "{cmd}"
                '''
            self.log.info(cmd1)
            msg3 = self.client.sh(cmd1).result()
            self.log.info(msg3)
            self.log.info(msg3.splitlines()[2].strip())
            self.log.info(self.server_port)
            self.assertEqual(msg3.splitlines()[2].strip(), self.server_port)
        finally:
            cmd2 = f"sed -i '{int(line) + 1}d' {pg_hba}"
            self.log.info(cmd2)
            msg4 = self.server.sh(cmd2).result()
            self.log.info(msg4)

    def tearDown(self):
        self.log.info('-Opengauss_Function_Innerfunc_'
                      'Inet_Server_Port_Case0001结束-')
