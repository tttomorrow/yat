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
Case Type   : 逻辑复制
Case Name   : 使用JDBC创建逻辑复制槽,且复制槽名称大于64个字符
Description :
    1.创建名称大于64个字符的逻辑复制槽
Expect      :
    1.创建名称大于64个字符的逻辑复制槽失败
History     :
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant

LOG = Logger()


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        LOG.info('----------------this is setup-----------------------')
        LOG.info(
            '---Opengauss_Function_Logical_Replication_Case0010开始执行-----')
        self.comsh = CommonSH('dbuser')
        self.constant = Constant()
        self.parameter_values = ''

    def test_logical_replication(self):
        LOG.info(
            '----------------设置wal_level = logical----------------------')
        msg = self.comsh.execut_db_sql('show wal_level;')
        LOG.info(msg)
        self.parameter_values = msg.splitlines()[-2].strip()
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      'wal_level=logical')
        LOG.info(msg)
        LOG.info('---------------------重启数据库--------------------')
        self.comsh.restart_db_cluster()
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        msg1 = self.comsh.execut_db_sql('show wal_level;')
        LOG.info(msg1)
        self.new_value = msg1.splitlines()[-2].strip()
        self.assertIn('logical', self.new_value)

        LOG.info(
            '---------------------创建逻辑复制槽-------------------------')
        msg = self.comsh.execut_db_sql('''
            SELECT * FROM pg_create_logical_replication_slot
            ('slot1slot1slot1slot1slot1slot1slot1slot1slot1slot1
            slot1slot1slot1slotslot', 'mppdb_decoding');''')
        LOG.info(msg)
        self.assertIn(self.constant.invalid_character, msg)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        msg = self.comsh.execut_db_sql('''
            SELECT * FROM pg_drop_replication_slot
            ('slot1slot1slot1slot1slot1slot1slot1slot1slot1
            slot1slot1slot1slot1slotslot');
                    ''')
        LOG.info(msg)
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       f"wal_level={self.parameter_values}")
        LOG.info(msg)
        stopmsg = self.comsh.stop_db_cluster()
        LOG.info(stopmsg)
        startmsg = self.comsh.start_db_cluster()
        LOG.info(startmsg)
        LOG.info(
            '-----Opengauss_Function_Logical_Replication_Case0010执行完成---')
