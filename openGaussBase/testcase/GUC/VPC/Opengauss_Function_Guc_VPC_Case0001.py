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
Case Name   : 使用gs_guc set方法设置参数array_nulls为off ,观察预期结果
Description :
        1.查询array_nulls默认值
        2.修改参数值为off
        3.建表指定数组类型并插入空数组
        4.恢复参数默认值
Expect      :
        1.显示默认值为on
        2.设置成功,显示off
        3.建表成功且插入数据成功
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class VersionPlatform(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '---Opengauss_Function_Guc_VPC_Case0001start---')
        self.constant = Constant()

    def test_array_nulls(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show array_nulls;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('---步骤2:修改参数值为off---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'array_nulls = off')
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('---步骤3:重启数据库---')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('---步骤4:查询修改后的参数值---')
        sql_cmd = commonsh.execut_db_sql('''show array_nulls;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('---步骤5:建表指定数组类型并插入空数组，成功---')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists
            t_test0214;
            create table t_test0214(id int[]);
            insert into t_test0214 values(null);''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('---步骤6:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''show array_nulls;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'array_nulls={self.res}')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''drop table if exists 
            t_test0214;''')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_VPC_Case0001finish---')
