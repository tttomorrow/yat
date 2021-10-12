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
Case Name   : gs_om命令查看静态配置
Description :
        1.查询数据库详细状态信息：gs_om -t query
        2.查看静态配置：gs_om -t view
Expect      :
        1.状态显示成功
        2.查看成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0010start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('----------查询数据库详细状态信息------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_om -t query;
            '''
        self.logger.info(check_cmd1)
        msg1 = self.dbuser_node.sh(check_cmd1).result()
        self.logger.info(msg1)
        self.assertIn('cluster_state   : Normal', msg1)

        self.logger.info('------------------查看静态配置------------------')
        check_cmd2 = f'''source {macro.DB_ENV_PATH};
            gs_om -t view;
            '''
        self.logger.info(check_cmd2)
        msg2 = self.dbuser_node.sh(check_cmd2).result()
        self.logger.info(msg2)
        self.logger.info('---------从数据库状态信息中获取节点数量----------')
        db_status = self.commonsh.get_db_cluster_status('detail')
        if db_status.count('|') > 0:
            dest_str = db_status.splitlines()[-1].strip()
            self.logger.info(dest_str)
            dest_list = dest_str.split('|')
            self.logger.info(dest_list)
            node_num = len(dest_list)
            self.logger.info(node_num)
        else:
            dest_str = db_status.splitlines()[-1].strip()
            self.logger.info(dest_str)
            node_num = int(dest_str[0].strip())
            self.logger.info(node_num)
        self.logger.info('----------从静态配置文件中获取节点数量-----------')
        msg2_list = msg2.splitlines()
        self.logger.info(msg2_list)
        nodecount = ''
        for i in msg2_list:
            if 'nodeCount' in i:
                nodecount = i
                break
        count = int(nodecount.split(':')[1])
        self.logger.info(count)
        if node_num == count:
            self.logger.info('---------------静态配置检查正常-----------')
        else:
            raise Exception('静态配置异常')

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0010finish--')