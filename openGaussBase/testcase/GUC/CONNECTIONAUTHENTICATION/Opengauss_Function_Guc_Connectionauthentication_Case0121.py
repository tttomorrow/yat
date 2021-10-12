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
Case Type   : GUC参数--连接认证
Case Name   : application_name参数使用gs_guc reload 设置为其他数据类型
Description :
    1、查看application_name默认值
    2、设置参数application_name为数字
    3、设置参数application_name为空
    4、恢复默认值
Expect      :
    1、查看application_name默认值
    2、设置参数application_name为数字，合理报错
    3、设置参数application_name为空，成功
    4、恢复默认值成功
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
        LOG.info('----Connectionauthentication_Case0121开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        LOG.info('----步骤1.查看参数application_name默认值----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc  check -N all -I all -c application_name;'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('application_name=\'dn_', msg)

        LOG.info('----步骤2.设置参数application_name为数字----')
        check_cmd = f'''hostname'''
        LOG.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        LOG.info(hostname)
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N {hostname} -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"application_name=1234";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('ERROR: The value "1234" for parameter "'
                      'application_name" is incorrect', msg)

        LOG.info('----步骤3.设置参数application_name为空----')
        check_cmd = f'''hostname'''
        LOG.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        LOG.info(hostname)
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N {hostname} -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"application_name= \'\'";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)

    def tearDown(self):
        LOG.info('------步骤4.恢复环境---------')
        check_cmd = f'''hostname'''
        LOG.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        LOG.info(hostname)
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N {hostname} -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"application_name= \'dn_6001\'";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc check -N all -I all -c application_name;'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('-----Connectionauthentication_Case0121执行结束-----')
