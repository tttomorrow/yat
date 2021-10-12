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
Case Name   : 使用gs_guc set方法设置参数default_transaction_read_only为on,
              建表，合理报错
Description :
        1.查询default_transaction_read_only默认值
        2.设置参数值为on并重启数据库
        3.查询该参数修改后的值
        4.建表验证
        4.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.设置成功
        3.显示on
        4.建表，报错
        5.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0062start---')
        self.constant = Constant()
        self.expect_res = 'ERROR:  cannot execute CREATE TABLE in a' \
                          ' read-only transaction'

    def test_default_transaction_read_only(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show default_transaction_read_only;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:设置参数值为on并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'default_transaction_read_only = on')
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('show default_transaction_read_only;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('--步骤4: 建表，报错--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_062;
            create table test_062(id int);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.expect_res, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤5:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('show default_transaction_read_only;')
        LOG.info(sql_cmd)
        if sql_cmd.split('\n')[-2].strip() != self.res:
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"default_transaction_read_only"
                                         f"={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        sql_cmd = commonsh.execut_db_sql('show default_transaction_read_only;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_ClientConnection_Case0062执行完成--')
