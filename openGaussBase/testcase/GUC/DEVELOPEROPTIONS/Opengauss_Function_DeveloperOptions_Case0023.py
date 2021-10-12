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
Case Name   : 使用gs_guc set方法设置参数explain_dna_file绝对路径,观察预期结果
Description :
        1.查询explain_dna_file默认值
        2.创建csv路径
        3.修改参数值为绝对路径并重启数据库后查询
        4.恢复参数默认值
Expect      :
        1.显示默认值为空
        2.创建成功
        3.修改成功
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()
commonsh = CommonSH('dbuser')


class DeveloperOptions(unittest.TestCase):

    def setUp(self):
        LOG.info(
            '---Opengauss_Function_DeveloperOptions_Case0023start----')
        self.constant = Constant()
        self.user_node = Node('dbuser')
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH

    def test_explain_dna_file(self):
        LOG.info('-------------创建csv路径--------------------')
        excute_cmd = f'touch {self.DB_INSTANCE_PATH}/explain_test.csv';
        LOG.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        LOG.info(msg1)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg1)
        # 查询默认值
        sql_cmd = commonsh.execut_db_sql(f'''show explain_dna_file;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
       # 修改参数explain_dna_file为绝对路径
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f'''explain_dna_file = '{self.DB_INSTANCE_PATH}/explain_test.csv' ''')


        LOG.info(msg)
        self.assertTrue(msg)
        # 重启数据库
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        self.assertTrue(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        # 查询
        sql_cmd = commonsh.execut_db_sql(f'''show explain_dna_file;''')
        LOG.info(sql_cmd)
        self.assertIn('/cluster/dn1/explain_test.csv', sql_cmd)

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        excute_cmd = f'rm -rf  {self.DB_INSTANCE_PATH}/explain_test.csv';

        LOG.info(excute_cmd)
        msg1 = self.user_node.sh(excute_cmd).result()
        LOG.info(msg1)
        msg = commonsh.execute_gsguc(
'set', self.constant.GSGUC_SUCCESS_MSG, f'''explain_dna_file''')
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql(f'''show explain_dna_file;''')
        LOG.info(sql_cmd)
        LOG.info(
        '----Opengauss_Function_DeveloperOptions_Case0023执行完成-----')
