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
Case Type   : 系统内部使用工具
Case Name   : 主机执行gs_ctl query查询lsn并展示最大长度是否成功
Description :
    1.查询lsn
    2.主机执行query并指定-L参数,查询lsn并展示最大长度
Expect      :
    1.查询lsn
    2.主机执行query并指定-L参数,查询lsn并展示最大长度成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0092开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('-----------------查询lsn---------------------')
        value_msg = self.sh_primary.execut_db_sql(
            'select pg_current_xlog_location();')
        LOG.info(value_msg)
        self.pv = value_msg.splitlines()[-2].strip()
        LOG.info(self.pv)

        LOG.info('-----------------查询主机状态---------------------')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl query -D {macro.DB_BACKUP_PATH} -L {self.pv} ;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        self.assertIn('MAX_LSN', query_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        # 无需清理环境
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0092执行完成---')
