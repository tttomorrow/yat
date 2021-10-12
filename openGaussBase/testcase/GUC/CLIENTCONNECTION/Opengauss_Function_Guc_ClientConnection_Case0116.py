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
Case Name   : 使用gs_guc set方法设置参数max_compile_functions为无效值，
              合理报错
Description :
        1.查询max_compile_functions默认值
        2.修改参数值为test
        3.修改参数值为1258.9558
        4.修改参数值为0
        5.修改参数值为-1
        6.恢复参数默认值
Expect      :
        1.显示默认值为1000
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
            '--Opengauss_Function_Guc_ClientConnection_Case0116start---')
        self.constant = Constant()

    def test_max_compile_functions(self):
        # 查询默认值
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 修改参数值为test，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         "max_compile_functions = 'test'")
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        self.assertIn('1000', sql_cmd)
        # 修改参数值为1258.9558，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         'max_compile_functions = 1258.9558')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        self.assertIn('1000', sql_cmd)
        # 修改参数值为0，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         'max_compile_functions = 0')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        self.assertIn('1000', sql_cmd)
        # 修改参数值为-1，报错
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                         'max_compile_functions = -1')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        self.assertIn('1000', sql_cmd)

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f'''max_compile_functions={self.res}''')
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        LOG.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0116执行完成----')
