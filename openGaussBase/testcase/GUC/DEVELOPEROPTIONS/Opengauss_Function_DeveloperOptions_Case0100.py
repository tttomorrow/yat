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
Case Type   : GUC
Case Name   : 使用gs_guc set方法设置参数thread_pool_attr为无效值,合理报错
Description :
        1.查询thread_pool_attr默认值
        2.修改参数值为test
        3.修改参数值为12345
        4.恢复参数默认值
Expect      :
        1.显示默认值为'16, 2, (nobind)'
        2.合理报错
        3.合理报错
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class DeveloperOption(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '------Opengauss_Function_DeveloperOptions_Case0100start-----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_thread_pool_attr(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show thread_pool_attr;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:修改参数值为test，12345合理报错--')
        invalid_value = ['test', 12345]
        for i in invalid_value:
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'thread_pool_attr= {i}')
            self.assertFalse(msg)

    def tearDown(self):
        LOG.info('--步骤4:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show thread_pool_attr;''')
        self.log.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"thread_pool_attr='{self.res}'")
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('''show thread_pool_attr;''')
        self.log.info(sql_cmd)
        self.log.info(
            '-----Opengauss_Function_DeveloperOptions_Case0100执行完成----')
