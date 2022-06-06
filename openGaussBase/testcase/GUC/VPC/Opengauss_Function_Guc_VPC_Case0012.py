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
Case Name   : 使用gs_guc set方法设置参数transform_null_equals值为on，
             观察预期结果
Description :
        1.查询transform_null_equals默认值
        2.参数值off下，测试expr = NULL
        3.修改参数值为on并重启数据库
        4.查询修改后的参数值
        5.参数值on下，测试expr = NULL
        6.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.返回NULL（未知）
        3.修改成功
        4.显示on
        5.on状态下，expr = NULL返回f或t
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
            '------Opengauss_Function_Guc_VPC_Case0012start----')
        self.constant = Constant()

    def test_transform_null_equals(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show transform_null_equals;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('---步骤2:测试expression is [not] null即expr = NULL---')
        sql_cmd = commonsh.execut_db_sql('''select 2 is null;''')
        LOG.info(sql_cmd)
        self.assertEqual('f', sql_cmd.split('\n')[2].strip())
        sql_cmd = commonsh.execut_db_sql('''select 2 is not null;''')
        LOG.info(sql_cmd)
        self.assertEqual('t', sql_cmd.split('\n')[2].strip())
        sql_cmd = commonsh.execut_db_sql('''select 2 = null;''')
        LOG.info(sql_cmd)
        self.assertIn('', sql_cmd)
        LOG.info('---步骤3:修改参数值为on---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "transform_null_equals = on")
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('---步骤4:重启数据库---')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('---步骤5:查询修改后的参数值---')
        sql_cmd = commonsh.execut_db_sql('''show transform_null_equals;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('---步骤6:测试expr = NULL---')
        sql_cmd = commonsh.execut_db_sql('''select 2 = null;''')
        LOG.info(sql_cmd)
        self.assertEqual('f', sql_cmd.split('\n')[2].strip())
        sql_cmd = commonsh.execut_db_sql('''select null = null;''')
        LOG.info(sql_cmd)
        self.assertEqual('t', sql_cmd.split('\n')[2].strip())

    def tearDown(self):
        sql_cmd = commonsh.execut_db_sql('''show transform_null_equals;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'transform_null_equals={self.res}')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '------Opengauss_Function_Guc_VPC_Case0012finish----')
