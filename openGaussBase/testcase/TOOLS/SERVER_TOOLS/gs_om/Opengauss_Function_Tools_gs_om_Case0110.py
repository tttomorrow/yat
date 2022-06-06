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
Case Type   : 系统内部工具
Case Name   : 制造unknown状态，修改备机port，状态恢复后是否可以查到正确的port
Description :
    1、查看集群状态，校验备节点端口号;
    2、移动集群中主节点用户下互信文件, mv ~/.ssh/* ssh_backup/
    3、guc方式修改备节点端口号，重启数据库;
    4、恢复环境原有互信关系;
    5、结合方式一查看集群状态，校验备节点端口号;
    6、恢复原有集群端口;
    7、清理环境;
Expect      :
    1、查看集群状态正常;
    2、移动互信文件成功;
    3、修改备机端口号成功，重启数据库失败;
    4、恢复原有互信关系成功;
    5、显示数据库状态信息，存在port字段，备机端口号为修改后port;
    6、恢复原有集群端口成功;
    7、清理环境成功;
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
ssh_path = os.path.join(macro.DB_INSTANCE_PATH, 'ssh_backup')
primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Tools(unittest.TestCase):

    def setUp(self):
        logger.info("======Opengauss_Function_Tools_gs_om_Case0110开始执行======")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.constant = Constant()

        logger.info("======获取端口信息======")
        self.sql_cmd = f'''show port;'''
        show_port_res = self.commonsh.execut_db_sql(self.sql_cmd)
        self.node_port = show_port_res.splitlines()[-2].strip()
        logger.info(self.node_port)
        self.rep_port = int(self.node_port) + 10000
        logger.info(self.rep_port)

    def test_server_tools(self):
        logger.info("======步骤1:查询数据库状态，校验备节点端口号======")
        show_res = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(show_res)
        self.assertIn(self.node_port, show_res.splitlines()[11])

        logger.info("======步骤2:移动集群中主节点用户下互信文件======")
        mkdir_path = f'''mkdir {ssh_path};
            mv ~/.ssh/* {ssh_path};
            ls {macro.DB_INSTANCE_PATH}'''
        logger.info(mkdir_path)
        mkdir_res = self.user_node.sh(mkdir_path).result()
        logger.info(mkdir_res)
        self.assertIn('ssh_backup', mkdir_res)

        logger.info("======步骤3:guc方式修改备节点port，重启数据库======")
        guc_cmd = f'''source {macro.DB_ENV_PATH};
            gs_guc set -D {macro.DB_INSTANCE_PATH} \
            -c "port={self.rep_port}"'''
        logger.info(guc_cmd)
        guc_res = self.standby_node.sh(guc_cmd).result()
        logger.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res)
        status = self.commonsh.restart_db_cluster()
        self.assertFalse(status)

        logger.info("======步骤4:恢复原有环境互信文件=======")
        recove_cmd = f'''mv {ssh_path}/* ~/.ssh/;
            ls ~/.ssh/'''
        logger.info(recove_cmd)
        recov_res = self.user_node.sh(recove_cmd).result()
        logger.info(recov_res)
        self.assertTrue(recov_res is not False)

        logger.info("======步骤5:结合--detail参数，查看数据库状态及节点信息======")
        shell_res = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(shell_res)
        logger.info("======校验修改后端口正确======")
        self.assertIn(str(self.rep_port), shell_res.splitlines()[11])

        logger.info("======步骤6:恢复原有集群端口======")
        guc_cmd = f'''source {macro.DB_ENV_PATH};
            gs_guc set -D {macro.DB_INSTANCE_PATH} \
            -c "port={self.node_port}"'''
        logger.info(guc_cmd)
        guc_res = self.standby_node.sh(guc_cmd).result()
        logger.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res)
        status = self.commonsh.restart_db_cluster()
        self.assertTrue(status)

    def tearDown(self):
        logger.info("======步骤7:清理环境======")
        logger.info("======恢复原有环境互信文件=======")
        recove_cmd = f'''if [ "$(ls -A ~/.ssh/)" ]
                         then
                             echo "ssh file recovery!"
                         else   
                             mv {ssh_path}/*  ~/.ssh/;
                         fi
                         ls ~/.ssh/'''
        logger.info(recove_cmd)
        recov_res = self.user_node.sh(recove_cmd).result()
        logger.info(recov_res)

        logger.info("======删除互信文件备份文件======")
        clear_cmd = f'''rm -rf {ssh_path}'''
        logger.info(clear_cmd)
        self.user_node.sh(clear_cmd)

        status_msg = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(status_msg)
        self.assertTrue('Normal' in status_msg.splitlines()[2])

        if self.node_port not in status_msg.splitlines()[11]:
            cmd = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'port={self.node_port}')
            logger.info(cmd)
            self.commonsh.restart_db_cluster()
            status_msg = self.commonsh.get_db_cluster_status(param='detail')
            logger.info(status_msg)
        else:
            logger.info("======端口号正常======")
        logger.info("======Opengauss_Function_Tools_gs_om_Case0110执行结束======")
