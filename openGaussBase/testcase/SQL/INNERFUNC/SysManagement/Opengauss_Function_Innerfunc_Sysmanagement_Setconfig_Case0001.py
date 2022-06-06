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
Case Name   : set_config(setting_name, new_value, is_local)设置参数并返回新值。
Description :
    1. is_local为true,在事务外设置
    2. is_local为true,在事务内设置
    3. is_local为false，在事务中执行了此函数然后回滚
    4. is_local为false，事务已提交，影响将持续到会话的结束
Expect      :
    1. 设置不生效
    2. 只在事务里生效
    3. 只应用于当前事务，应用于当前会话命令的产生影响将在事务回滚之后消失
    4. 影响只持续到当前事务结束
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.commonsh = CommonSH('dbuser')
        self.log = Logger()
        self.log.info('''------------------------------------------------------
        Opengauss_Function_Innerfunc_Sysmanagement_Setconfig_Case0001开始''')

    def test_encode1(self):
        self.log.info("-----------is_local为true,在事务外设置，不生效----------")
        cmd = "select set_config('datestyle','ISO, DMY',true); show datestyle;"
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue('ISO, MDY' in msg)

    def test_encode2(self):
        self.log.info("----------is_local为true,在事务里设置，仅在事务里生效----")
        cmd = """start transaction;
                 select set_config('datestyle','ISO, DMY',true);
                 show datestyle;
                 commit;
                 show datestyle;"""
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue('ISO, DMY' in msg.splitlines()[8])
        self.assertTrue('ISO, MDY' in msg.splitlines()[-2])

    def test_encode3(self):
        self.log.info("-----------is_local为false,在事务里设置并回滚-----------")
        cmd = """start transaction;
                 select set_config('datestyle','ISO, DMY',false);
                 show datestyle;
                 rollback;
                 show datestyle;"""
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue('ISO, DMY' in msg.splitlines()[8])
        self.assertTrue('ISO, MDY' in msg.splitlines()[-2])

    def test_encode4(self):
        self.log.info("-----------is_local为false,在事务里设置并提交-----------")
        cmd = """start transaction;
                 select set_config('datestyle','ISO, DMY',false);
                 show datestyle;
                 commit;
                 show datestyle;
                 """
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue('ISO, DMY' in msg.splitlines()[8])
        self.assertTrue('ISO, DMY' in msg.splitlines()[-2])

    def tearDown(self):
        self.log.info('''------------------------------------------------------
        ---Opengauss_Function_Innerfunc_Sysmanagement_Setconfig_Case0001结束''')
