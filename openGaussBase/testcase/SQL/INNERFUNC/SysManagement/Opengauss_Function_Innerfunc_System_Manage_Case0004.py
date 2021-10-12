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
Case Type   : 系统管理函数--其他函数
Case Name   : 函数get_local_active_session() ，提供当前节点保存在内存中的历史活跃session状态的采样记录
Description :
    1.函数get_local_active_session() ，提供当前节点保存在内存中的历史活跃session状态的采样记录
Expect      :
    1.获取当前节点保存在内存中的历史活跃session状态的采样记录成功
History     :
"""
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0004开始执行-')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info('---步骤1.函数get_local_active_session() ，'
                 '提供当前节点保存在内存中的历史活跃session状态的采样记录---')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select get_local_active_session() limit 1 ;')
        LOG.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        list1 = sql_cmd.split('\n')[2]
        LOG.info(list1)
        list2 = list1.split(',')
        self.assertEqual(len(list2), 26)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0004结束-')
