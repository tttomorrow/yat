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
Case Type   : 服务端工具
Case Name   : 使用gs_guc set为"max_connections" 恢复默认值
Description :
    1.查看max_connections默认值
    2.使用gs_guc set为"max_connections" 修改默认值
    3.重启数据库
    4.查看设置后的参数值
    5.使用gs_guc set为"max_connections" 恢复默认值
    6.重启成功
    7.查看设置后的参数值
Expect      :
    1.显示默认值
    2.修改成功
    3.重启成功
    4.显示修改后的值
    5.恢复完成
    6.重启成功
    7.恢复成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0018开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        LOG.info('---------查看max_connections默认值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                       gs_guc check -N all -D {macro.DB_INSTANCE_PATH}\
                        -c "max_connections" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        res = msg.splitlines()[2].strip()
        self.assertIn(res, msg)

        LOG.info('---------使用gs_guc set为"max_connections" 修改默认值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                   gs_guc set -N all -D {macro.DB_INSTANCE_PATH} -c \
                    "max_connections=4900" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("Success to perform gs_guc!", msg)
        LOG.info('------------重启数据库-----------')
        status = f"source {macro.DB_ENV_PATH};" \
            f"gs_om -t status --detail"
        LOG.info(status)
        status_msg = self.dbuser_node.sh(status).result()
        LOG.info(status_msg)
        self.assertTrue("Normal" in status_msg or 'Degraded' in status_msg)
        LOG.info('---------查看设置后的参数值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH}
                      gs_guc check -N all -D {macro.DB_INSTANCE_PATH} \
                      -c "max_connections"'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("max_connections=4900", msg)

    def tearDown(self):
        LOG.info('---------恢复默认值---------')
        check_cmd = f'''hostname'''
        LOG.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        check_cmd = f'''source {macro.DB_ENV_PATH}
                     gs_guc set -N all -D {macro.DB_INSTANCE_PATH} \
                     -c "max_connections=5000" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('------------重启数据库-----------')
        restart = self.commonsh.restart_db_cluster()
        LOG.info(restart)
        LOG.info('--查看数据库状态---')
        status = f"source {macro.DB_ENV_PATH};" \
            f"gs_om -t status --detail"
        LOG.info(status)
        status_msg = self.dbuser_node.sh(status).result()
        LOG.info(status_msg)
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0018执行结束-----')
