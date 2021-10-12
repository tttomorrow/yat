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
Case Name   : 语法一gs_om -t status查询数据库状态信息，校验port信息
Description :
    1、结合参数--detail,显示状态详细信息，校验是否有port字段，校验备机port端口号;
    2、结合参数--all,显示所有节点信息，校验是否有port字段，校验备机port端口号;
    3、结合参数-h,指定待查询的节点名称，校验是否有port信息，校验指定节点端口号;
    4、结合参数-o，输出到指定的output文件中，校验文件中是否有输出信息，输出信息中是否有port信息，校验port端口号;
    5、结合参数-l，指定日志文件及存放路径，校验日志中是否有输出信息，输出信息是否有port信息，校验port端口号
    6、清理环境;
Expect      :
    1、显示状态详细信息，存在port字段，备机端口号正确;
    2、显示所有节点信息，存在port字段，备机端口号正确;
    3、显示指定节点信息，存在port字段，指定节点端口号正确;
    4、输出output文件，文件中有输出信息，输出信息中存在port信息，端口号正确;
    5、输出日志，日志中有输出信息，输出信息中存在port信息，端口号正确;
    6、清理环境成功;
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()
conf_path = os.path.join(macro.DB_INSTANCE_PATH, macro.DB_PG_CONFIG_NAME)
output_path = os.path.join(macro.DB_INSTANCE_PATH, 'output.txt')
log_path = os.path.join(macro.DB_INSTANCE_PATH, 'status.log')
primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Tools(unittest.TestCase):

    def setUp(self):
        logger.info("======Opengauss_Function_Tools_gs_om_Case0094开始执行======")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')

    def test_server_tools(self):
        logger.info("======获取端口信息======")
        sql_cmd = f'''show port;'''
        show_port_res = self.commonsh.execut_db_sql(sql_cmd)
        node_port = show_port_res.splitlines()[-2].strip()
        logger.info(node_port)

        logger.info("====步骤1:结合参数--detail,显示状态详细信息，校验port字段，校验备机port端口号====")
        shell_res = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(shell_res)
        self.assertEqual('port', shell_res.splitlines()[8].split()[2].strip())
        self.assertEqual(node_port,
                         shell_res.splitlines()[-1].split()[3].strip())

        logger.info("=====步骤2:结合参数--all,显示所有节点信息,校验port字段，校验备机port端口号=====")
        new_list_all = []
        shell_res = self.commonsh.get_db_cluster_status(param='all')
        logger.info(shell_res)
        res = shell_res.splitlines()

        for i in res:
            if 'instance_port' in i:
                new_list_all.append(i.split(':')[1].strip())
                logger.info(new_list_all)
                logger.info("======获取port字段信息成功======")
        try:
            for port in new_list_all:
                if port == node_port:
                    logger.info("======端口信息一致======")
        except Exception as e:
            logger.info("======端口信息不一致======")
            raise e
        finally:
            logger.info("======步骤2执行结束======")

        logger.info("======步骤3:结合参数-h,指定待查询的节点名称======")
        new_list_hostname = []
        shell_name = f'''hostname'''
        hostname = self.standby_node.sh(shell_name).result()
        logger.info(hostname)

        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'status -h {hostname}')
        logger.info(shell_res)
        res = shell_res.splitlines()

        for i in res:
            if 'instance_port' in i:
                new_list_hostname.append(i.split(':')[1].strip())
                logger.info(new_list_hostname)
                logger.info("======获取port字段信息成功======")
        try:
            if node_port == new_list_hostname[0]:
                logger.info("======端口信息一致======")
        except Exception as e:
            logger.info("======端口信息不一致======")
            raise e
        finally:
            logger.info("======步骤3执行结束======")

        logger.info("=====步骤4:结合参数-o，输出到指定的output文件中======")
        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'status --detail -o {output_path}')
        logger.info(shell_res)

        cat_res = self.user_node.sh(
            f'''cat {output_path} | grep port''').result()
        logger.info(cat_res)
        self.assertIn('port', cat_res)

        output_cmd = f'''cat {output_path} | grep {node_port}'''
        logger.info(output_cmd)
        output_res = self.user_node.sh(output_cmd).result()
        logger.info(output_res)
        self.assertEqual(node_port,
                         output_res.splitlines()[-1].split()[3].strip())

        logger.info("======步骤5:结合参数-l，输出到指定日志文件及存放路径======")
        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'status --detail -l {log_path}')
        logger.info(shell_res)

        cat_res = self.user_node.sh(
            f'''cat {macro.DB_INSTANCE_PATH}/status* | grep port''').result()
        logger.info(cat_res)
        self.assertIn('port', cat_res)
        log_cmd = f'cat {macro.DB_INSTANCE_PATH}/status* | grep {node_port}'
        logger.info(log_cmd)
        log_res = self.user_node.sh(log_cmd).result()
        logger.info(log_res.splitlines()[0].split()[3].strip())
        self.assertEqual(node_port,
                         log_res.splitlines()[-1].split()[3].strip())

    def tearDown(self):
        logger.info("======步骤6:清理环境======")
        clear_cmd = f'''rm -rf {log_path} {output_path}'''
        logger.info(clear_cmd)
        self.user_node.sh(clear_cmd)
        logger.info("======Opengauss_Function_Tools_gs_om_Case0094执行结束======")
