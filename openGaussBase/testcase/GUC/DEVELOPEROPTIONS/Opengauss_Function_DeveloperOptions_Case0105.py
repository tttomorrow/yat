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
Case Name   : 使用gs_guc set方法设置参数enable_partition_opfusion为on,
              观察预期结果
Description :
        1.查询enable_partition_opfusion默认值
        2.修改参数enable_partition_opfusion值为on并重启数据库
        3.创建分区表
        4.explain语句查询表
        5.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.设置成功
        3.创建分区表成功
        4.查询成功
        5.默认值恢复成功
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
            '-----Opengauss_Function_DeveloperOptions_Case0105start-----')
        self.constant = Constant()

    def test_enable_partition_opfusion(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show enable_partition_opfusion;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('--步骤2:修改参数值为on并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'enable_partition_opfusion =on')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('show enable_partition_opfusion;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('--步骤4:创建分区表--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists startend_pt;
            create table startend_pt (c1 int, c2 int) partition by range (c2) (
            partition p1 start(1) end(1000) every(200) ,
            partition p2 end(2000),
            partition p3 start(2000) end(2500) ,
            partition p4 start(2500),
            partition p5 start(3000) end(5000) every(1000) 
            )
            enable row movement;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        LOG.info('--步骤5:使用explain语句查询--')
        sql_cmd = commonsh.execut_db_sql('explain select * from startend_pt;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('drop table if exists startend_pt;')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show enable_partition_opfusion;')
        LOG.info(sql_cmd)
        if "off" != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'enable_partition_opfusion=off')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show enable_partition_opfusion;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_DeveloperOptions_Case0105finish----')
