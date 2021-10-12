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
Case Name   : 语法一gs_om -t status查询数据库状态信息，参数组合测试，校验port信息
Description :
    1、结合参数--detail,-o,-l,将状态详细信息同时输出到指定文件及log中，
       校验文件及日志中是否有输出信息，输出信息中是否有port字段，校验port端口号;
    2、结合参数--all,-o,-l,将所有节点信息同时输出到指定文件及log中，
       校验文件及日志中是否有输出信息，输出信息中是否有port字段，校验port端口号;
    3、结合参数--h,-o,-l,将指定节点状态信息同时输出到指定文件及log中，
       校验文件及日志中是否有输出信息，输出信息中是否有port字段，校验port端口号;
    4、结合参数--h,--detail,输出指定节点状态详细信息，实际以--detail参数输出信息为主，
       校验输出信息是否有port字段，校验port端口号;
    5、结合参数--h,--all,输出指定节点状态信息，实际以-h参数输出信息为准，
       校验输出信息是否有port字段，校验port端口号;
    6、结合参数--detail,--all,输出所有节点详细状态信息，实际以--detail参数输出信息为主，
       校验输出信息是否有port字段，校验port端口号;
    7、清理环境;
Expect      :
    1、文件及日志中有输出信息，显示状态详细信息，存在port字段，备机端口号正确;
    2、文件及日志中有输出信息，显示所有节点信息，存在port字段，备机端口号正确;
    3、文件及日志中有输出信息，显示指定节点信息，存在port字段，指定节点端口号正确;
    4、显示数据库状态详细信息，输出信息中存在port字段，端口号正确;
    5、显示数据库所有节点信息，输出信息中存在port字段，端口号正确;
    6、显示数据库状态详细信息，输出信息中存在port字段，端口号正确;
    7、清理环境成功;
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
        logger.info("======Opengauss_Function_Tools_gs_om_Case0095开始执行======")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')

    def test_server_tools(self):
        logger.info("======获取端口信息======")
        sql_cmd = f'''show port;'''
        show_port_res = self.commonsh.execut_db_sql(sql_cmd)
        node_port = show_port_res.splitlines()[-2].strip()
        logger.info(node_port)

        logger.info("====步骤1:结合参数--detail,-o,-l,将状态详细信息同时输出到指定文件及log中====")
        shell_res = self.commonsh.get_db_cluster_status(param='other',
            args=f'status --detail -o {output_path} -l {log_path}')
        logger.info(shell_res)

        cat_res = self.user_node.sh(
            f'''cat {output_path} | grep port''').result()
        logger.info(cat_res)
        self.assertIn('port', cat_res)

        output_cmd = f'''cat {output_path} | grep {node_port}'''
        logger.info(output_cmd)
        output_res = self.user_node.sh(output_cmd).result()
        logger.info(output_res.splitlines()[0].split()[3].strip())
        self.assertEqual(node_port,
                         output_res.splitlines()[-1].split()[3].strip())

        clear_output = f'''rm -rf {output_path}'''
        self.user_node.sh(clear_output)

        logger.info("=====步骤2:结合参数--all,-o,-l,将所有节点信息同时输出到指定文件及log中=====")
        shell_res = self.commonsh.get_db_cluster_status(param='other',
            args=f'status --all -o {output_path} -l {log_path}')
        logger.info(shell_res)
        output_cmd = f'''cat {output_path} | grep instance_port'''
        logger.info(output_cmd)
        output_res = self.user_node.sh(output_cmd).result()
        logger.info(output_res)
        self.assertEqual('instance_port',
                         output_res.splitlines()[-1].split(':')[0].strip())
        self.assertEqual(node_port,
                         output_res.splitlines()[-1].split(':')[1].strip())

        clear_output = f'''rm -rf {output_path}'''
        self.user_node.sh(clear_output)

        logger.info("======步骤3:结合参数-h,-o,-l,将指定节点状态信息同时输出到指定文件及log中======")
        shell_name = f'''hostname'''
        hostname = self.standby_node.sh(shell_name).result()
        logger.info(hostname)

        shell_res = self.commonsh.get_db_cluster_status(param='other',
            args=f'status -h {hostname} -o {output_path} -l {log_path}')
        logger.info(shell_res)
        output_res = self.user_node.sh(output_cmd).result()
        logger.info('instance_port', output_res.split(':')[0].strip())
        logger.info(node_port, output_res.split(':')[1].strip())

        clear_output = f'''rm -rf {output_path}'''
        self.user_node.sh(clear_output)

        logger.info("=====步骤4:结合参数-h,--detail,输出节点状态详细信息======")
        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'status -h {hostname} --detail')
        logger.info(shell_res)
        self.assertEqual('port', shell_res.splitlines()[8].split()[2].strip())
        self.assertEqual(show_port_res.splitlines()[-2].strip(),
                         shell_res.splitlines()[-1].split()[3].strip())

        logger.info("======步骤5:结合参数-h,--all,输出节点状态信息======")
        new_list_hostname = []
        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'status -h {hostname} --all')
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
            logger.info("======步骤5执行结束======")

        logger.info("======步骤6:结合参数--detail,--all,输出所有节点详细状态信息======")
        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args='status --detail --all')
        logger.info(shell_res)
        self.assertEqual('port', shell_res.splitlines()[8].split()[2].strip())
        self.assertEqual(show_port_res.splitlines()[-2].strip(),
                         shell_res.splitlines()[-1].split()[3].strip())

    def tearDown(self):
        logger.info("======步骤7:清理环境======")
        clear_cmd = f'''rm -rf {log_path} {output_path}'''
        logger.info(clear_cmd)
        self.user_node.sh(clear_cmd)
        logger.info("======Opengauss_Function_Tools_gs_om_Case0095执行结束======")
