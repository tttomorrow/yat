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
Case Type   : 统计信息函数
Case Name   : pg_stat_get_wal_senders()描述：在主机端查询walsender信息。
Description :
    1.在主机端查询walsender信息，主节点查询
    2.在主机端查询walsender信息，备节点查询
Expect      :
    1.在主机端查询walsender信息，主节点查询成功
    2.在主机端查询walsender信息，备节点查询,失败
History     :
"""

import os
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf('6002 ' not in Primary_SH.get_db_cluster_status('detail'),
                 '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.commonsh = CommonSH()
        self.commonsh1 = CommonSH('Standby1DbUser')

    def test_built_in_func(self):
        text = '----step1.在主机端查询walsender信息，主节点查询----'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_stat_get_wal_senders();')
        self.log.info(sql_cmd)
        str_info = sql_cmd.split('\n')[-2]
        self.log.info(str_info)
        num = len(str_info.split(','))
        self.log.info(f'num = {num}')
        if num == 21:
            self.log.info('在主机端查询walsender信息成功')
        else:
            raise Exception(f'函数执行异常，请检查{text}')

        text = '----step2.在主机端查询walsender信息，备节点查询----'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(
            f'select pg_stat_get_wal_senders();')
        self.log.info(sql_cmd)
        str_info = sql_cmd.split('\n')[-2]
        self.log.info(str_info)
        num = len(str_info.split(','))
        self.log.info(f'num = {num}')
        if num == 1:
            self.log.info('在备机端查询walsender信息失败')

    def tearDown(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
