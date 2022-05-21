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
Case Name   : 语法一gs_om -t status频繁执行状态查询，连续50次查询数据库状态信息，校验port信息
Description :
    1、结合参数--detail,频繁执行50次，
       显示状态详细信息，校验是否有port字段，校验备机port端口号;
    2、结合参数--all,频繁执行50次，
       显示所有节点信息，校验是否有port字段，校验备机port端口号;
Expect      :
    1、显示状态详细信息，存在port字段，端口号正确;
    2、显示所有节点信息，存在port字段，端口号正确;
History     :
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Tools(unittest.TestCase):

    def setUp(self):
        logger.info("======Opengauss_Function_Tools_gs_om_Case0111开始执行======")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        logger.info("======获取端口信息======")
        sql_cmd = f'''show port;'''
        show_port_res = self.commonsh.execut_db_sql(sql_cmd)
        self.node_port = show_port_res.splitlines()[-2].strip()
        logger.info(self.node_port)

    def test_server_tools(self):
        logger.info("====步骤1:结合参数--detail,重复执行命令50次,校验port字段，校验备机port端口号====")
        for i in range(50):
            self.status = self.commonsh.get_db_cluster_status(param='detail')
            logger.info(self.status)

        self.assertEqual('port',
                         self.status.splitlines()[8].split()[2].strip())
        self.assertEqual(self.node_port,
                         self.status.splitlines()[-1].split()[3].strip())

        logger.info("=====步骤2:结合参数--all,显示所有节点信息,校验port字段，校验备机port端口号=====")
        new_list_all = []
        for i in range(50):
            self.shell_res = self.commonsh.get_db_cluster_status(param='all')
            logger.info(self.shell_res)
        res = self.shell_res.splitlines()

        for i in res:
            if 'instance_port' in i:
                new_list_all.append(i.split(':')[1].strip())
                logger.info(new_list_all)
                logger.info("======获取port字段信息成功======")
        try:
            for port in new_list_all:
                if port == self.node_port:
                    logger.info("======端口信息一致======")
        except Exception as e:
            logger.info("======端口信息不一致======")
            raise e
        finally:
            logger.info("======步骤2执行结束======")

    def tearDown(self):
        logger.info("======校验集群状态======")
        status_msg = self.commonsh.get_db_cluster_status(param='detail')
        logger.info(status_msg)
        self.assertTrue('Normal' in status_msg.splitlines()[2])

        if self.node_port not in status_msg.splitlines()[10]:
            cmd = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'port={self.node_port}')
            logger.info(cmd)
            self.commonsh.restart_db_cluster()
            status_msg = self.commonsh.get_db_cluster_status(param='detail')
            logger.info(status_msg)
        else:
            logger.info("======端口号正常======")
        logger.info("======Opengauss_Function_Tools_gs_om_Case0111执行结束======")
