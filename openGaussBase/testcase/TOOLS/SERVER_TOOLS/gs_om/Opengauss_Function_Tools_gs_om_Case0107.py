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
Case Name   : 使用guc方式修改集群端口,switchover主备切换,查询数据库状态，校验节点信息
Description :
    1、guc方式修改集群所有节点port,重启数据库;
       gs_guc set -N all -D {dn1} -c "port=new_port"
    2、需同步修改xml文件中端口号保持一致;
       sed -i 's/40406/55555/g' {xml}
       gs_om -t generateconf -X {xml} --distribute
    3、主备正常情况下，进行主备切换;
       gs_ctl -D {cluster/dn1} switchover
       gs_om -t refreshconf
       gs_om -t sop && gs_om -t start
    4、结合--detail参数，查看数据库状态及节点详细信息，校验是否有port字段，校验备机IP是否发生变化，校验备机port端口号
    5、结合--all参数，查看数据库状态及所有节点信息，校验是否有port字段，校验备机IP是否发生变化，校验备机port端口号
    6、结合-h,-o参数，查看指定数据库节点状态及信息（-h指定切换后的备机），校验是否有输出文件，
       输出文件中是否有port字段，校验备机IP是否发生变化，校验备机port端口号
    7、query查询数据状态及相关信息，校验备机IP是否发生变化，校验备机port端口号
    8、恢复原有集群状态;
    9、恢复集群原有端口;
    10、清理环境;
Expect      :
    1、修改集群端口号成功，重启数据库成功;
    2、修改xml文件端口号成功，刷新静态配置文件成功;
    3、主备切换成功，动态配置文件刷新成功，数据库重启成功;
    4、显示状态详细信息，原有主备状态发生改变，存在port字段，备机端口号正确（即原主机port为现备机port）;
    5、显示数据库所有节点信息，原有主备状态发生改变，存在port字段，备机端口号正确（即原主机port为现备机port）;
    6、显示指定节点状态信息，指定节点现为备机，存在port字段，端口号为原有主机port;
    7、显示数据库状态信息，原有主备状态发生改变，存在port字段，备机端口号正确;
    8、恢复原有集群状态成功;
    9、恢复集群原有端口成功;
    10、清理环境成功;
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
        logger.info("======Opengauss_Function_Tools_gs_om_Case0098开始执行======")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.primary_node = Node('PrimaryRoot')
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
        exchange_port = show_res.splitlines()[-2].strip()
        logger.info(show_res)
        self.assertEqual(self.rep_port, int(exchange_port))

        logger.info("======步骤2:修改xml文件中端口号======")
        sed = f"""sed -i 's/{self.node_port}/{self.rep_port}/g' \
            {macro.DB_XML_PATH}"""
        logger.info(sed)
        shell_res = self.primary_node.sh(sed).result()
        self.assertFalse(shell_res)

        logger.info("======刷新静态配置文件======")
        refresh_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t generateconf -X {macro.DB_XML_PATH} --distribute'''
        logger.info(refresh_cmd)
        refresh_res = self.user_node.sh(refresh_cmd).result()
        logger.info(refresh_res)
        self.assertIn('Successfully distributed static configuration files',
                      refresh_res)

        logger.info("======步骤3:switchover进行主备切换，刷新动态配置文件，重启数据库======")
        switch_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl -D {macro.DB_INSTANCE_PATH} switchover;
            gs_om -t refreshconf'''
        logger.info(switch_cmd)

        switch_res = self.standby_node.sh(switch_cmd).result()
        logger.info(switch_res)
        self.assertIn(self.constant.SWITCH_SUCCESS_MSG, switch_res)
        self.assertIn(self.constant.REFRESHCONF_SUCCESS_MSG, switch_res)
        self.commonsh.restart_db_cluster()

        logger.info("======步骤4:结合--detail参数，查看数据库状态及节点信息======")
        shell_res = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(shell_res)

        logger.info("======校验port字段信息======")
        self.assertIn('port', shell_res.splitlines()[8])

        logger.info("======校验主备切换成功 & port正确======")
        self.assertTrue('Standby' in shell_res.splitlines()[10]
                        and exchange_port in shell_res.splitlines()[10])

        logger.info("======步骤5:结合--all参数，查看数据库状态及节点信息======")
        new_status_list = []
        new_port_list = []
        shell_res = self.commonsh.get_db_cluster_status(param='all')
        logger.info(shell_res)

        res = shell_res.splitlines()
        for param in res:
            if 'instance_role' in param:
                new_status_list.append(param)
            if 'instance_port' in param:
                new_port_list.append(param)
        logger.info(new_status_list)
        logger.info(new_port_list)

        logger.info("======校验主备切换成功 && port正确======")
        try:
            if 'Standby' in new_status_list[0]:
                logger.info("======主备切换成功======")
        except Exception as e:
            logger.info("======主备未切换成功======")
            raise e
        finally:
            logger.info("======主备切换校验完成======")

        try:
            if exchange_port == new_port_list[0].split(':')[1].strip():
                logger.info("======端口信息一致======")
        except Exception as e:
            logger.info("======端口信息不一致======")
            raise e
        finally:
            logger.info("======端口校验完成======")

        logger.info("======步骤6:结合-h,-o参数，-h指定切换后的备机，查看状态信息======")
        shell_name = f'''hostname'''
        hostname = self.user_node.sh(shell_name).result()
        logger.info(hostname)

        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'status -h {hostname} -o {output_path}')
        logger.info(shell_res)

        logger.info("======当前指定节点为切换后的备节点，主备切换成功======")
        cat_res = self.user_node.sh(
            f'''cat {output_path} | grep instance_role''').result()
        logger.info(cat_res)
        self.assertIn('instance_role', cat_res)

        logger.info("======当前节点port为原主节点port======")
        port_res = self.user_node.sh(
            f'''cat {output_path} | grep instance_port''').result()
        logger.info(port_res)
        self.assertIn(exchange_port, port_res)

        logger.info("====步骤7:结合参数query，查看数据库状态信息，校验port字段，校验port端口====")
        shell_res = self.commonsh.get_db_cluster_status(param='other',
                                                        args='query')
        logger.info(shell_res)
        self.assertEqual('port', shell_res.splitlines()[8].split()[2].strip())

        logger.info("======校验主备切换成功 && port端口正确======")
        self.assertTrue('Standby' in shell_res.splitlines()[10]
                        and exchange_port in shell_res.splitlines()[10])

        logger.info("======步骤8:恢复原有集群主备状态======")
        recovery_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl -D {macro.DB_INSTANCE_PATH} switchover;
            gs_om -t refreshconf'''
        logger.info(recovery_cmd)

        recovery_res = self.user_node.sh(recovery_cmd).result()
        logger.info(recovery_res)
        self.assertIn(self.constant.SWITCH_SUCCESS_MSG, recovery_res)
        self.assertIn(self.constant.REFRESHCONF_SUCCESS_MSG, recovery_res)
        self.commonsh.restart_db_cluster()

        logger.info("======步骤9:恢复原有集群端口======")
        recov = self.commonsh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'port={self.node_port}')
        logger.info(recov)

        logger.info("======恢复xml中原有集群端口======")
        recovery = f"""sed -i 's/{self.rep_port}/{self.node_port}/g' \
            {macro.DB_XML_PATH}"""
        logger.info(recovery)
        shell_res = self.primary_node.sh(recovery).result()
        self.assertFalse(shell_res)

        refresh_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t generateconf -X {macro.DB_XML_PATH} --distribute'''
        logger.info(refresh_cmd)
        refresh_res = self.user_node.sh(refresh_cmd).result()
        logger.info(refresh_res)
        self.assertIn('Successfully distributed static configuration files',
                      refresh_res)
        self.commonsh.restart_db_cluster()

    def tearDown(self):
        logger.info("======步骤10:清理环境======")
        clear_cmd = f'''rm -rf {output_path}'''
        logger.info(clear_cmd)
        self.user_node.sh(clear_cmd)

        status_msg = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(status_msg)
        self.assertTrue('Normal' in status_msg.splitlines()[2])

        if self.constant.STANDBY_NORMAL in status_msg.splitlines()[10]:
            logger.info("======状态不正常，恢复主备状态======")
            recover_cmd = f'''source {macro.DB_ENV_PATH};
                gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast;
                gs_om -t refreshconf;
                '''
            logger.info(recover_cmd)
            recover_msg = self.user_node.sh(recover_cmd).result()
            logger.info(recover_msg)
            self.commonsh.restart_db_cluster()
        else:
            logger.info("======主备节点正常======")

        if self.node_port not in status_msg.splitlines()[11]:
            cmd = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'port={self.node_port}')
            logger.info(cmd)
            self.commonsh.restart_db_cluster()
            status_msg = self.commonsh.get_db_cluster_status(param='detail')
            logger.info(status_msg)
        logger.info("======Opengauss_Function_Tools_gs_om_Case0098执行结束======")
