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
Case Name   : 使用gs_guc reload为"max_connections" 恢复默认值
Description :
    1.查看max_connections默认路径
    2.使用gs_guc reload为"max_connections" 修改默认值
    3.查看设置后的参数值
    4.使用gs_guc reload为"max_connections" 恢复默认值
    5.查看设置后的参数值
Expect      :
    1.默认值
    2.修改成功
    3.显示修改后的值
    4.恢复完成
    5.显示成功
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
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0017开始执行-----')
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
        self.assertIn('5000', msg)

        LOG.info('---使用gs_guc reload为"max_connections" 修改默认值---')
        check_cmd = f'''source {macro.DB_ENV_PATH};
               gs_guc reload  -N all -D {macro.DB_INSTANCE_PATH} -c \
                "max_connections=4900" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("Success to perform gs_guc!", msg)

        LOG.info('---------查看设置后的参数值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                      gs_guc check -N all -D {macro.DB_INSTANCE_PATH}\
                      -c "max_connections"'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("max_connections=4900", msg)

    def tearDown(self):
        LOG.info('---------恢复默认值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH}
                gs_guc reload -N all -D {macro.DB_INSTANCE_PATH} \
                -c "max_connections=5000" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('---------重启数据库---------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail;' \
            f'gs_om -t restart;'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0017执行结束-----')
