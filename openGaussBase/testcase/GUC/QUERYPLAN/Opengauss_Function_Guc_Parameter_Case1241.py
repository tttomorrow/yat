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
Case Type   : GUC参数
Case Name   : 修改参数effective_cache_size，观察预期结果
Description :
    1.show参数默认值
    2.修改参数默认值为2MB
    3.重启数据库
    4.show参数值
    5.恢复参数默认值
Expect      :
    1.参数默认值128MB
    2.修改参数默认值为2MB成功
    3.重启数据库成功
    4.参数值修改成功，显示2MB
    5.恢复参数默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Guc_Parameter_Case1241开始')
        self.dbuser = Node('PrimaryDbUser')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_guc_parameter(self):
        text = '--step1:show参数默认值;expect:参数默认值128MB--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show effective_cache_size;')
        self.log.info(sql_cmd)
        self.default_value = sql_cmd.splitlines()[2].strip()
        self.log.info(self.default_value)

        text = '--step2:修改参数默认值为2MB;expect:修改成功--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              'effective_cache_size =2MB')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)

        text = '--step3:重启数据库;expect:重启数据库成功--'
        self.log.info(text)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step4:show参数值--;expect:参数值修改成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show effective_cache_size;')
        self.log.info(sql_cmd)
        self.assertIn('2MB', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step5:恢复参数默认值--;expect:恢复默认值成功--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'effective_cache_size = '
                                              f'{self.default_value}')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('Opengauss_Function_Guc_Parameter_Case1241结束')
