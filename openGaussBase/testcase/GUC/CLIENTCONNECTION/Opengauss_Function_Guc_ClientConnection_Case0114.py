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
Case Name   : 使用方式四ALTER SYSTEM SET paraname 修改max_compile_functions值
Description :
        1.查看默认值max_compile_functions;
        2.方式四修改该参数值ALTER SYSTEM SET max_compile_functions to 1;
        3.重启数据库并查询gs_om -t stop && gs_om -t start
        4.恢复默认值
Expect      :
        1.默认值显示1000
        2.命令执行成功
        3.重启数据库后参数修改成功
        4.恢复默认值成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class Deletaduit(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '-----Opengauss_Function_Guc_Resource_Case0114start-----')
        self.constant = Constant()

    def test_startdb(self):
        # 查询该参数默认值
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 使用方式四ALTER SYSTEM SET paraname 修改max_compile_functions
        Sqlmdg = commonsh.execut_db_sql(
            '''ALTER SYSTEM SET max_compile_functions to 1;''')
        LOG.info(Sqlmdg)
        self.assertIn('ALTER SYSTEM SET', Sqlmdg)
        # 重启数据库
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        # 查询该参数修改值
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
        self.assertIn('1', sql_cmd)

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        sql_cmd = commonsh.execut_db_sql(f'''show max_compile_functions;''')
        LOG.info(sql_cmd)
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
            '-----Opengauss_Function_Guc_Resource_Case0114执行完成--------')
