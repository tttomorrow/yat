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
Case Name   : 检查数据库xml配置文件(路径不正确)
Description :
    1.检查数据库xml配置文件(路径不正确)
Expect      :
    1.检查配置文件失败，提示xml文件不存在
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.root_user = Node('default')

    def test_server_tools1(self):
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0047开始-')

        self.log.info('---root用户检查数据库xml配置文件(路径不正确)---')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -X /home/sj.xml'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.assertIn('The /home/sj.xml does not exist', checkos_msg)

    def tearDown(self):
        self.log.info('-----------------无需清理环境----------------')
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0047结束-')
