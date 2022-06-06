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
Case Name   : ALTER SYSTEM SET命令设置参数advance_xlog_file_num
Description :
    1. 查看默认值0
    2. 修改参数为非法值
    3. 修改参数在合法值范围内并重启检查生效
    4. 恢复默认值
Expect      : 
    1. 默认值0
    2. 合理报错
    3. 修改成功
    4. 恢复成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('''---Opengauss_Function_DML_Set_Case0040开始---''')
        self.common = Common()
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()
        self.user_node = Node('dbuser')
        self.env_path = macro.DB_ENV_PATH

    def test_alter(self):

        def check(value):
            cmd = "show advance_xlog_file_num;"
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            return self.assertTrue(value in msg)

        check('0')  # 检查默认值是0

        self.flag = True  # 恢复标志
        # 取值范围0~1000000
        var = [-1, 1000001, 20.85, 'A', 100, 0]
        for i in range(6):
            cmd = f'ALTER SYSTEM SET advance_xlog_file_num to {var[i]};'
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            if i < 4:  # 前4个非法值校验，合理报错 
                self.assertTrue('ERROR' in msg)
            else:  # 修改合法值重启验证生效
                self.commonsh.restart_db_cluster()
                status = self.commonsh.get_db_cluster_status()
                self.assertTrue("Normal" in status or 'Degraded' in status)
                check(str(var[i]))
        self.flag = False

    def tearDown(self):
        if self.flag:  # 脚本执行异常，进行恢复
            cmd = "ALTER SYSTEM SET advance_xlog_file_num to 0;"
            self.commonsh.execut_db_sql(cmd)
            self.commonsh.restart_db_cluster()
        self.log.info('''---Opengauss_Function_DML_Set_Case0040结束---''')