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
Case Name   : 使用gs_guc encrypt命令加密用户密码时，指定的-M的值为client
Description :
    1.生成加密文件时，不指定用户
    2.生成加密文件时，不指定用户密码
    3.生成加密文件时，指定用户符合要求，指定的密码不符合要求
    4.生成加密文件时，指定用户不符合要求，指定的密码符合要求
    5.生成加密文件时，指定用户和密码都不符合要求
    6.生成加密文件时指定用户和密码都符合要求
Expect      :
    1.执行成功
    2.执行成功
    3.执行失败
    4.执行成功
    5.执行失败
    6.设置成功
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
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0038开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        LOG.info('----生成加密文件时，不指定用户----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc encrypt -M client -K Haha@1234 -D {macro.DB_INSTANCE_PATH};
        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('------------------判断文件是否生成------------------')
        check_cmd = f'''du -h {macro.DB_INSTANCE_PATH}/client.key.cipher'''
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        msg = msg.split()[0]
        self.assertTrue(float(msg[:-1]) > 0)

        LOG.info('------------------删除生成文件------------------')
        check_cmd = f'''rm -rf {macro.DB_INSTANCE_PATH}/client.key.rand;
                        rm -rf {macro.DB_INSTANCE_PATH}/client.key.cipher;
                        '''
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('----生成加密文件时，不指定用户密码----')
        check_cmd = f'''source {macro.DB_ENV_PATH}
        expect <<EOF
        spawn gs_guc encrypt -M client -U {self.dbuser_node.db_user} -D \
        {macro.DB_INSTANCE_PATH}
        expect "Password:"
        send "{self.dbuser_node.db_password}\r"
        expect eof
        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('------------------删除生成文件------------------')
        check_cmd = f'''rm -rf {macro.DB_INSTANCE_PATH}/yat.key.rand;
                        rm -rf {macro.DB_INSTANCE_PATH}/yat.key.cipher;
                        '''
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('----生成加密文件时，指定用户符合要求，指定的密码不符合要求----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc encrypt -M client -K pa123!  -U {self.dbuser_node.db_user} \
        -D {macro.DB_INSTANCE_PATH};
        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Invalid password,it must contain at \
least eight characters', msg)

        LOG.info('----生成加密文件时，指定用户不符合要求，指定的密码符合要求----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_guc encrypt -M client -K passw123@  \
                        -U qwe -D {macro.DB_INSTANCE_PATH};
                        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('------------------判断文件是否生成------------------')
        check_cmd = f'''du -h {macro.DB_INSTANCE_PATH}/qwe.key.cipher'''
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        msg = msg.split()[0]
        self.assertTrue(float(msg[:-1]) > 0)

        LOG.info('------------------删除生成文件------------------')
        check_cmd = f'''rm -rf {macro.DB_INSTANCE_PATH}/qwe.key.rand;
                        rm -rf {macro.DB_INSTANCE_PATH}/qwe.key.cipher;
                           '''
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('----生成加密文件时，指定用户和密码都不符合要求----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_guc encrypt -M client -K password -U username \
                        -D {macro.DB_INSTANCE_PATH};
                        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Invalid password,it must contain at least \
three kinds of characters', msg)

        LOG.info('----生成加密文件时指定用户和密码都符合要求----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc encrypt -M client -K Haha@1234 -U {self.dbuser_node.db_user}  \
        -D {macro.DB_INSTANCE_PATH};
        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('------------------判断文件是否生成------------------')
        check_cmd = f'''du -h {macro.DB_INSTANCE_PATH}/\
                        {self.dbuser_node.db_user}.key.cipher'''
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        msg = msg.split()[0]
        self.assertTrue(float(msg[:-1]) > 0)

    def tearDown(self):
        LOG.info('------------------删除生成文件------------------')
        check_cmd = f'''
        rm -rf {macro.DB_INSTANCE_PATH}/{self.dbuser_node.db_user}.key.rand;
        rm -rf {macro.DB_INSTANCE_PATH}/{self.dbuser_node.db_user}.key.cipher;
        '''
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0038执行结束----')
