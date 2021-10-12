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
Case Type   : 系统内部工具
Case Name   : 使用guc方式修改集群端口，查询数据库状态，校验节点信息
Description :
    1、guc方式修改集群所有节点port,重启数据库;
       gs_guc set -N all -D {dn1} -c "port=new_port"
    2、结合--detail参数，查看数据库状态及节点详细信息，校验是否有port字段，校验备机port端口号
    3、结合--all参数，查看数据库状态及所有节点信息，校验是否有port字段，校验备机port端口号
    4、结合-h,-o参数，查看指定数据库节点状态及信息，校验是否有输出文件，输出文件中是否有port字段，校验备机port端口号
    5、query查询数据状态及相关信息，校验备机port端口号
    6、恢复原有集群端口;
    7、清理环境;
Expect      :
    1、修改集群端口号成功，重启数据库成功;
    2、显示状态详细信息，存在port字段，备机端口号为修改后port;
    3、显示数据库所有节点信息，存在port字段，备机端口号为修改后port;
    4、显示指定节点状态信息，指定节点为备机，存在port字段，端口号为修改后port;
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
conf_path = os.path.join(macro.DB_INSTANCE_PATH, macro.DB_PG_CONFIG_NAME)
output_path = os.path.join(macro.DB_INSTANCE_PATH, 'output.txt')
primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Tools(unittest.TestCase):

    def setUp(self):
        logger.info("======Opengauss_Function_Tools_gs_om_Case0106开始执行======")
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
        logger.info("======步骤1:guc方式修改所有节点port，重启数据库，校验修改成功======")
        guc_res = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'port={self.rep_port}')
        logger.info(guc_res)
        self.commonsh.restart_db_cluster()
        logger.info("======查看修改后的端口号======")
        show_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.user_node.db_name} -p {self.rep_port} \
            -c "show port"'''
        show_res = self.user_node.sh(show_cmd).result()
        logger.info(show_res)
        self.assertEqual(self.rep_port,
                         int(show_res.splitlines()[-2].strip()))

        logger.info("======步骤2:结合--detail参数，查看数据库状态及节点信息======")
        shell_res = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(shell_res)

        logger.info("======校验port字段信息======")
        self.assertIn('port', shell_res.splitlines()[8])

        logger.info("======校验切换后的port是否正确======")
        self.assertEqual(show_res.splitlines()[-2].strip(),
                         shell_res.splitlines()[-1].split()[3].strip())

        logger.info("======步骤3:结合--all参数，查看数据库状态及节点信息======")
        new_port_list = []
        shell_res = self.commonsh.get_db_cluster_status(param='all')
        logger.info(shell_res)
        res = shell_res.splitlines()

        for i in res:
            if 'instance_port' in i:
                new_port_list.append(i.split(':')[1].strip())
                logger.info(new_port_list)
                logger.info("======获取port字段信息成功======")
        try:
            for port in new_port_list:
                if port == show_res.splitlines()[-2].strip():
                    logger.info("======端口信息一致======")
        except Exception as e:
            logger.info("======端口信息不一致======")
            raise e
        finally:
            logger.info("======步骤2执行结束======")

        logger.info("======步骤4:结合-h,-o参数，-h指定备机，查看状态信息======")
        shell_name = f'''hostname'''
        hostname = self.standby_node.sh(shell_name).result()
        logger.info(hostname)

        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'status -h {hostname} -o {output_path}')
        logger.info(shell_res)

        logger.info("======当前指定节点为备节点======")
        cat_res = self.user_node.sh(
            f'''cat {output_path} | grep instance_role''').result()
        logger.info(cat_res)
        self.assertIn('instance_role', cat_res)

        logger.info("======当前节点port为修改后port======")
        port_res = self.user_node.sh(
            f'''cat {output_path} | grep instance_port''').result()
        logger.info(port_res)
        self.assertIn(show_res.splitlines()[-2].strip(), port_res)

        logger.info("====步骤5:结合参数query，查看数据库状态信息，校验port字段，校验port端口====")
        shell_res = self.commonsh.get_db_cluster_status(param='other',
                                                        args='query')
        logger.info(shell_res)
        self.assertEqual('port', shell_res.splitlines()[8].split()[2].strip())

        logger.info("======校验修改后端口正确======")
        self.assertIn(show_res.splitlines()[-2].strip(),
                      shell_res.splitlines()[10])

        logger.info("======步骤6:恢复原有集群端口======")
        recov = self.commonsh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'port={self.node_port}')
        logger.info(recov)
        self.commonsh.restart_db_cluster()

    def tearDown(self):
        logger.info("======步骤7:清理环境======")
        clear_cmd = f'''rm -rf {output_path}'''
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
        logger.info("======Opengauss_Function_Tools_gs_om_Case0106执行结束======")
