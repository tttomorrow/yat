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
Case Name   : 通过set session和set local命令设置参数backtrace_min_messages值
            （superuser型）
Description :
        1.查询backtrace_min_messages默认值
        2.使用set session命令设置参数值为debug并查看
        3.使用set local命令设置backtrace_min_messages参数值为debug5
        4.恢复参数默认值
Expect      :
        1.显示默认值为panic
        2.设置成功,参数值为debug
        3.设置成功，查看参数值，依然还是debug，set local命令不生效
        4.默认值恢复成功
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
            '------Opengauss_Function_DML_Set_Case0041start---')
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
        LOG.info('--步骤2:set方法修改参数值--')
        sql_cmd = commonsh.execut_db_sql('''set backtrace_min_messages to 
            debug;
            show backtrace_min_messages;
            set local backtrace_min_messages to debug5;
            show backtrace_min_messages;
            reset backtrace_min_messages;
            show backtrace_min_messages;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd)
        sql_result_list = sql_cmd.splitlines()
        LOG.info(sql_result_list)
        self.assertEqual('debug', sql_result_list[3].strip())
        self.assertIn(self.constant.RESET_SUCCESS_MSG, sql_cmd)
        self.assertEqual('panic', sql_result_list[-2].strip())

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
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '----Opengauss_Function_DML_Set_Case0041执行完成------')
