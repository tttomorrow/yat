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
Case Type   : set
Case Name   : 通过set session/local config_parameter  from current命令设置
              参数backtrace_min_messages
Description :
        1.使用set backtrace_min_messages from current设置参数并查看;
        2.使用set allocate_mem_cost from current设置参数并查看;
        3.恢复参数默认值
Expect      :
        1.显示为panic
        2.显示0
        3.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class Set(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '------Opengauss_Function_DML_Set_Case0042start------')
        self.constant = Constant()

    def test_set(self):
        LOG.info('--步骤1:查看默认值--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'backtrace_min_messages=panic')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show backtrace_min_messages;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.assertEqual('panic', self.res)
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'allocate_mem_cost=0')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show allocate_mem_cost;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.assertEqual('0', self.res)
        sql_cmd = commonsh.execut_db_sql('''set backtrace_min_messages from 
            current;
            show backtrace_min_messages;
            set allocate_mem_cost from current;
            show allocate_mem_cost;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd)
        sql_result_list = sql_cmd.splitlines()
        LOG.info(sql_result_list)
        self.assertEqual('panic', sql_result_list[3].strip())
        self.assertEqual('0', sql_result_list[-2].strip())

    def tearDown(self):
        LOG.info('--步骤3:恢复参数值--')
        sql_cmd = commonsh.execut_db_sql('''show backtrace_min_messages;''')
        LOG.info(sql_cmd)
        if "panic" != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'backtrace_min_messages=panic')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        sql_cmd = commonsh.execut_db_sql('''show allocate_mem_cost;''')
        LOG.info(sql_cmd)
        if "0" != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'allocate_mem_cost=0')
            LOG.info(msg)
            self.assertTrue(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '-----Opengauss_Function_DML_Set_Case0042执行完成--------')
