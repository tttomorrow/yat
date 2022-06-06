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
Case Type   : 功能测试
Case Name   : 设置参数enable_delta_store值
Description :
    1. 查看默认值off
    2. ALTER SYSTEM SET修改参数为on
    3. gs_guc set恢复默认值off
Expect      : 
    1. 默认值off
    2. 修改成功
    3. 恢复成功
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('''---Opengauss_Function_DML_Set_Case0115开始---''')
        self.commonsh = CommonSH('dbuser')
        self.user_node = Node('dbuser')

    def test_alter(self):

        def check(value):
            cmd = "show enable_delta_store;"
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            return self.assertTrue(value in msg)

        def restart():
            self.commonsh.restart_db_cluster()
            status = self.commonsh.get_db_cluster_status()
            self.assertTrue("Normal" in status or 'Degraded' in status)

        try:
            # 检查默认值是off
            check('off')
            # 修改参数值为on
            cmd = 'ALTER SYSTEM SET enable_delta_store to on;'
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            restart()
            check('on')
        finally:
            # 恢复默认值off
            cmd1 = f'''source {macro.DB_ENV_PATH}
            gs_guc set -N all -I all -c "enable_delta_store='off'"'''
            self.log.info(cmd1)
            msg1 = self.user_node.sh(cmd1).result()
            self.log.info(msg1)
            restart()
            check('off')

    def tearDown(self):
        self.log.info('''---Opengauss_Function_DML_Set_Case0115结束---''')