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
Case Name   : 使用ALTER SYSTEM SET 设置参数default_transaction_read_only
              合理报错
Description :
        1.查询default_transaction_read_only默认值
        2.修改参数值为on
        3.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.合理报错
        3.默认值恢复成功
History     :
        这个参数在分布式场景下是sighup的；但是在集中式场景下是USERSET
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0064start-----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_default_transaction_read_only(self):
        self.log.info('--步骤1:查询默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show 
            default_transaction_read_only;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        self.log.info('--步骤2:修改参数为on--')
        sql_cmd = self.commonsh.execut_db_sql('''alter system set
            default_transaction_read_only to on;''')
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)

    def tearDown(self):
        self.log.info('--步骤3恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show 
            default_transaction_read_only;''')
        self.log.info(sql_cmd)
        if sql_cmd.split('\n')[2].strip() != "off":
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'default_transaction_read_only'
                                              f'=off')
            self.log.info(msg)
        self.log.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0064执行完成---')
