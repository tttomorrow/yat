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
Case Name   : 使用gs_guc set方法设置参数statement_timeout为5ms,插入2000万条
              数据，合理报错
Description :
        1.建表
        2.修改参数值为5ms
        3.插入2000万条数据
        4.恢复参数默认值
Expect      :
        1.建表成功
        2.设置成功，显示5ms
        3.合理报错ERROR:  canceling statement due to statement timeout
        4.默认值恢复成功
"""
import re
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0082start---')
        self.constant = Constant()

    def test_statement_timeout(self):
        LOG.info('--步骤1:建表--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test082;
            create table test082(id int);''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        LOG.info('--步骤2:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show statement_timeout;''')
        LOG.info(sql_cmd)
        self.assertIn('0', sql_cmd)
        LOG.info('--步骤3:修改参数值为5ms--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'statement_timeout =5')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        LOG.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤4:插入2000万数据，报错--')
        sql_cmd = commonsh.execut_db_sql('''insert into test082 
            values(generate_series(1,20000000));''')
        LOG.info(sql_cmd)
        assert_msg = re.search(
            r'ERROR:(.*)canceling statement due to statement timeout', sql_cmd,
            re.I | re.S)
        self.assertTrue(assert_msg)

    def tearDown(self):
        LOG.info('--步骤5:清理环境--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"statement_timeout=0")
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show statement_timeout;''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test082;''')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0082执行完成----')
