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
Case Name   : 语法三gs_om -t query查询数据库状态信息，校验port信息
Description :
    1、查看openGauss状态详细信息，校验输出信息中是否有port字段，校验port端口号;
    2、结合参数-o,将查询结果输出到指定文件中，校验文件中输出信息;
    3、清理环境;
Expect      :
    1、输出信息，存在port字段，备机端口号正确;
    2、文件中有输出信息，存在port字段，备机端口号正确;
    3、清理环境成功;
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
primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Tools(unittest.TestCase):

    def setUp(self):
        logger.info("======Opengauss_Function_Tools_gs_om_Case0097开始执行======")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')

    def test_server_tools(self):
        logger.info("======获取端口信息======")
        sql_cmd = f'''show port;'''
        show_port_res = self.commonsh.execut_db_sql(sql_cmd)
        node_port = show_port_res.splitlines()[-2].strip()
        logger.info(node_port)

        logger.info("====步骤1:结合参数query，查看数据库状态信息，校验port字段，校验port端口====")
        shell_res = self.commonsh.get_db_cluster_status(param='other',
                                                        args='query')
        logger.info(shell_res)
        self.assertEqual('port', shell_res.splitlines()[8].split()[2].strip())
        self.assertEqual(node_port,
                         shell_res.splitlines()[-1].split()[3].strip())

        logger.info("======步骤2:结合参数query，指定-o，校验文件中是否有输出信息======")
        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'query -o {output_path}')
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

    def tearDown(self):
        logger.info("======步骤3:清理环境======")
        clear_cmd = f'''rm -rf {output_path}'''
        logger.info(clear_cmd)
        self.user_node.sh(clear_cmd)
        logger.info("======Opengauss_Function_Tools_gs_om_Case0097执行结束======")
