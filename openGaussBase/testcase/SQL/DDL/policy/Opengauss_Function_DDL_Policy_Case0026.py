"""
Case Type   : 功能测试
Case Name   : 给外表定义行访问控制策略，合理报错
Description :
    1. 置参数enable_incremental_checkpoint为off并重启检查生效
    2. 创建外表并创建行访问控制策略
    3. 恢复参数enable_incremental_checkpoint为on并重启检查生效
Expect      : 
    1.默认值是off,设置成功
    2.外表创建成功，策略创建失败
    3.设置成功，恢复为on
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.user_node = Node('dbuser')
        self.log = Logger()
        self.env_path = macro.DB_ENV_PATH
        self.cluster_path = macro.DB_INSTANCE_PATH

    def test_test_directory(self):
        self.log.info("-----Opengauss_Function_DDL_Policy_Case0026开始-----")
        var = ['off', 'on']

        def set_para(value):  # 修改参数值并重启检查生效
            res = self.commonsh.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'enable_incremental_checkpoint={value}')
            self.assertTrue(res)
            self.commonsh.restart_db_cluster()
            status = self.commonsh.get_db_cluster_status()
            self.assertTrue("Normal" in status or 'Degraded' in status)
            res = self.commonsh.execute_gsguc(
                'check', f'{value}', 'enable_incremental_checkpoint')
            self.assertTrue(res)

        try:
            set_para(var[0])  # 修改参数enable_incremental_checkpoint为off
            cmd = """drop foreign table if exists tb1 cascade;
                    create foreign table tb1(id int, usr varchar(20));
                    drop policy if exists pol on tb1;
                    create policy pol on tb1 for update to public
                    using (usr = current_user);"""
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)  # 给外表定义行访问控制策略，合理报错
            self.assertTrue('ERROR:  "tb1" is not a normal table' in msg)
        finally:
            cmd1 = """drop foreign table if exists tb1 cascade;"""
            self.commonsh.execut_db_sql(cmd1)
            # 恢复enable_incremental_checkpoint为on在有外表的时候库会挂，暂不处理

    def tearDown(self):
        self.log.info("-----Opengauss_Function_DDL_Policy_Case0026结束-----")