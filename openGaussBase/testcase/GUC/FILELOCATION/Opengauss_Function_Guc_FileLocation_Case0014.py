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
Case Name   : 使用gs_guc set修改参数data_directory为空值，观察预期结果；
Description :
              1、查看data_directory默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c data_directory
              2、使用设置s_guc set设置data_directory为空值
              gs_guc set -D {cluster/dn1} -c "data_directory=' '"
              3、重启使其生效，观察预期结果；
              gs_om -t stop && gs_om -t start
              4、恢复默认值；
Expect      :
              1、显示默认值；
              2、参数修改成功；
              3、重启失败。
              4、恢复默认值成功，恢复为初始设置数据目录。
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
        self.log.info('==Guc_FileLocation_Case0014开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        showcmd = '''source ''' + macro.DB_ENV_PATH \
                  + ''';gs_guc check -D ''' + macro.DB_INSTANCE_PATH \
                  + ''' -c data_directory'''
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn(macro.DB_INSTANCE_PATH, check)

        self.log.info("使用设置gs_guc set设置data_directory为空值")
        gucsetcmd = '''source ''' + macro.DB_ENV_PATH \
                    + ''';gs_guc set -D ''' + macro.DB_INSTANCE_PATH \
                    + ''' -c "data_directory=' '"'''
        self.log.info(gucsetcmd)
        gucresult = self.db_user_node.sh(gucsetcmd).result()
        self.log.info(gucresult)
        self.assertIn('Success', gucresult)

        self.log.info("重启数据库校验预期结果")
        result = COMMONSH.restart_db_cluster()
        self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        gucsetcmd2 = f'''
        source {macro.DB_ENV_PATH};
        gs_guc set -N all -I all \
        -c "data_directory='{macro.DB_INSTANCE_PATH}'"'''
        self.log.info(gucsetcmd2)
        self.db_user_node.sh(gucsetcmd2)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_FileLocation_Case0014完成==')
