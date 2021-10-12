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
Case Type   : GUC
Case Name   : 修改参数comm_no_delay为其他类型参数及超边界值，并校验其预期结果。
Description : 
              1、查看comm_no_delay默认值；
              show comm_no_delay;
              2、修改comm_no_delay分别为-1、'test'，校验其预期结果；
Expect      : 
              1、显示默认值；
              2、参数修改失败；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0254开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        showcmd = "source " + macro.DB_ENV_PATH \
                  + f";gsql -d {self.db_user_node.db_name} -p " \
                  + self.db_user_node.db_port + " -c \"show comm_no_delay\""
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn('off', check)
        self.log.info("修改comm_no_delay分别为"
                      "其他类型参数及超边界值等，校验其预期结果；")
        gucsetcmd = '''source ''' + macro.DB_ENV_PATH \
                    + ''';gs_guc set -D ''' + macro.DB_INSTANCE_PATH \
                    + ''' -c "comm_no_delay=-1"'''
        res1 = self.db_user_node.sh(gucsetcmd).result()
        self.assertIn('ERROR', res1)
        gucsetcmd = '''source ''' + macro.DB_ENV_PATH \
                    + ''';gs_guc set -D ''' + macro.DB_INSTANCE_PATH \
                    + ''' -c "comm_no_delay='test'"'''
        res1 = self.db_user_node.sh(gucsetcmd).result()
        self.assertIn('ERROR', res1)

    def tearDown(self):
        self.log.info("恢复默认值")
        gucsetcmd2 = f'''source {macro.DB_ENV_PATH};
        gs_guc set -N all -I all -c "comm_no_delay=\'off\'"'''
        self.log.info(gucsetcmd2)
        self.db_user_node.sh(gucsetcmd2)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_Connectionauthentication_Case0254完成==')
