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
Case Name   : 修改端口号，修改xml静态文件中port，查询数据库状态及节点信息
Description :
    1、修改xml文件中端口号;
       sed -i 's/40406/55555/g' {xml}
    2、刷新静态配置文件;
       gs_om -t generateconf -X {xml} --distribute
    3、查看数据库节点信息;
       gs_om -t view
    4、将节点信息输出到文件中;
       gs_om -t view -o output.txt
    5、清理环境;
Expect      :
    1、修改端口号成功;
    2、刷新静态配置文件成功;
    3、显示数据库状态详细信息，输出信息中存在port字段，端口号正确为修改后port;
    4、文件中有输出信息，存在port字段，指定节点端口号正确为修改后port;
    5、清理环境成功;
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
        logger.info("======Opengauss_Function_Tools_gs_om_Case0105开始执行======")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.primary_node = Node('PrimaryRoot')
        self.user_node = Node('PrimaryDbUser')

        logger.info("======获取端口信息======")
        sql_cmd = f'''show port;'''
        show_port_res = self.commonsh.execut_db_sql(sql_cmd)
        self.node_port = show_port_res.splitlines()[-2].strip()
        logger.info(self.node_port)
        self.rep_port = int(self.node_port) + 10000
        logger.info(self.rep_port)

    def test_server_tools(self):
        logger.info("======步骤1:修改xml文件中端口号======")
        sed = f"""sed -i 's/{self.node_port}/{self.rep_port}/g' \
            {macro.DB_XML_PATH}"""
        logger.info(sed)
        shell_res = self.primary_node.sh(sed).result()
        self.assertFalse(shell_res)

        logger.info("======步骤2:刷新静态配置文件======")
        refresh_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t generateconf -X {macro.DB_XML_PATH} --distribute'''
        logger.info(refresh_cmd)
        refresh_res = self.user_node.sh(refresh_cmd).result()
        logger.info(refresh_res)
        self.assertIn('Successfully distributed static configuration files',
                      refresh_res)

        logger.info("======步骤3:查看数据库节点信息======")
        new_port_list = []
        shell_res = self.commonsh.get_db_cluster_status(param='other',
                                                        args='view')
        logger.info(shell_res)
        res = shell_res.splitlines()

        for i in res:
            if 'datanodePort' in i:
                new_port_list.append(i.split(':')[1].strip())
        logger.info(new_port_list)
        logger.info("======获取port字段信息成功======")

        try:
            if self.rep_port == new_port_list[0] and \
                    self.rep_port == new_port_list[1]:
                logger.info("======备机端口信息一致======")
        except Exception as e:
            logger.info("======备机端口信息不一致======")
            raise e
        finally:
            logger.info("======步骤3执行结束======")

        logger.info("======步骤4:结合参数view，指定-o，校验文件中是否有输出信息======")
        shell_res = self.commonsh.get_db_cluster_status(
            param='other', args=f'view -o {output_path}')
        logger.info(shell_res)
        cat_res = self.user_node.sh(
            f'''cat {output_path} | grep datanodePort''').result()
        logger.info(cat_res)
        self.assertEqual(str(self.rep_port),
                         cat_res.splitlines()[-1].split(':')[1].strip())

    def tearDown(self):
        logger.info("======步骤5:清理环境，恢复原有port信息======")
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

        clear_cmd = f'''rm -rf {output_path}'''
        logger.info(clear_cmd)
        self.user_node.sh(clear_cmd)
        logger.info("======Opengauss_Function_Tools_gs_om_Case0105执行结束======")
