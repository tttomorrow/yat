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
Case Name   : 使用gs_guc set方法设置参数gin_fuzzy_search_limit为1000 ,
              观察预期结果
Description :
        1.查询gin_fuzzy_search_limit默认值
        2.修改参数值为1000并重启数据库
        3.查询修改后的参数值
        4.恢复参数默认值
Expect      :
        1.显示默认值为0
        2.设置成功
        3.显示1000
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0162start----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_gin_fuzzy_search_limit(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show gin_fuzzy_search_limit;')
        self.log.info(sql_cmd)
        self.assertEqual('0', sql_cmd.split('\n')[-2].strip())
        self.log.info('--步骤2:设置参数值为1000并重启数据库--')
        msg = self.commonsh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'gin_fuzzy_search_limit = 1000')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤3:查询修改后的参数值--')
        sql_cmd = self.commonsh.execut_db_sql('show gin_fuzzy_search_limit;')
        self.log.info(sql_cmd)
        self.assertEqual('1000', sql_cmd.split('\n')[-2].strip())

    def tearDown(self):
        self.log.info('--步骤4:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show gin_fuzzy_search_limit;')
        self.log.info(sql_cmd)
        if sql_cmd.split('\n')[-2].strip() != '0':
            msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              'gin_fuzzy_search_limit=0')
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0162执行完成---')
