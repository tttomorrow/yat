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
Case Name   : 使用gs_guc set方法设置参数max_function_args为12345,合理报错
Description :
        1.查询max_function_args默认值
        2.创建函数，参数个数为666个，实际创建时超过
        pg_proc_proname_args_nsp_index的
         也会报错最大值2704
        3.修改参数值为12345
        4.恢复参数默认值
Expect      :
        1.显示默认值为666
        2.创建失败
        3.合理报错，为固定参数，用户无法修改此参数，只能查看
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class DeveloperOptions(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '------Opengauss_Function_DeveloperOptions_Case0052start------')
        self.constant = Constant()
        self.args = ','.join(['para' + str(i) + ' int' for i in range(1, 667)])

    def test_max_function_args(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show max_function_args;''')
        LOG.info(sql_cmd)
        self.assertEqual('666', sql_cmd.split('\n')[2].strip())
        LOG.info('--步骤2:创建函数--')
        sql_cmd = commonsh.execut_db_sql(f'''create or replace function 
        func_052 ({self.args})returns SETOF RECORD
        as \$\$
        begin
            result_1 = i + 1;
            result_2 = i * 10;
        return next;
        end;
        \$\$language plpgsql;
        ''')
        LOG.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)
        LOG.info('--步骤3:设置参数为12345并重启数据库--')
        sql_cmd = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'max_function_args = 12345')
        LOG.info(sql_cmd)
        self.assertFalse(sql_cmd)
        LOG.info('--步骤4:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show max_function_args;''')
        LOG.info(sql_cmd)
        self.assertIn('666', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤5:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('''show max_function_args;''')
        LOG.info(sql_cmd)
        if "666" != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'max_function_args=666')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show max_function_args;''')
        LOG.info(sql_cmd)
        LOG.info(
            '----Opengauss_Function_DeveloperOptions_Case0052finish---')
