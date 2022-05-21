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
Case Name   : 使用gs_guc set方法设置参数gin_pending_list_limit为无效值，
              合理报错
Description :
        1.查询gin_pending_list_limit默认值
        2.修改参数值为63
        3.修改参数值为test
        4.修改参数值为-64
        5.修改参数值为2147483648
        6.恢复参数默认值
Expect      :
        1.显示默认值为4MB
        2.合理报错
        3.合理报错
        4.合理报错
        5.合理报错
        6.默认值恢复成功
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
            '---Opengauss_Function_Guc_ClientConnection_Case0122start---')
        self.constant = Constant()

    def test_gin_pending_list_limit(self):
        # 查询默认值
        sql_cmd = commonsh.execut_db_sql(
            f'''show gin_pending_list_limit;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 设置参数值为63，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         'gin_pending_list_limit = 63')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(
            f'''show gin_pending_list_limit;''')
        LOG.info(sql_cmd)
        self.assertIn('4MB', sql_cmd)
        # 设置参数值为test，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         "gin_pending_list_limit = 'test'")
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(
            f'''show gin_pending_list_limit;''')
        LOG.info(sql_cmd)
        self.assertIn('4MB', sql_cmd)
        # 设置参数值为-64，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         'gin_pending_list_limit = -64')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(
            f'''show gin_pending_list_limit;''')
        LOG.info(sql_cmd)
        self.assertIn('4MB', sql_cmd)
        # 设置参数值为2147483648，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                        'gin_pending_list_limit = 2147483648')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(
            f'''show gin_pending_list_limit;''')
        LOG.info(sql_cmd)
        self.assertIn('4MB', sql_cmd)
        # 设置参数值为空串，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         'gin_pending_list_limit = '' ')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(
            f'''show gin_pending_list_limit;''')
        LOG.info(sql_cmd)
        self.assertIn('4MB', sql_cmd)

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f'gin_pending_list_limit={self.res}')
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql(
            f'''show gin_pending_list_limit;''')
        LOG.info(sql_cmd)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0122执行完成---')
