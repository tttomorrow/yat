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
Case Name   : 使用gs_guc set方法设置参数sql_beta_feature为page_est_opt,
             观察预期结果
Description :
        1.查询sql_beta_feature默认值
        2.修改参数值为page_est_opt并重启数据库
        3.创建表和索引
        4.analyze语句检测索引文件
        5.删表并恢复参数默认值
Expect      :
        1.显示默认值为none
        2.设置成功
        3.创建表和索引成功
        4.analyze语句执行成功
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
            '---Opengauss_Function_DeveloperOptions_Case0113start--')
        self.constant = Constant()

    def test_sql_beta_feature(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show sql_beta_feature;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:修改参数值为page_est_opt并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'sql_beta_feature =page_est_opt')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('show sql_beta_feature;')
        LOG.info(sql_cmd)
        self.assertIn('page_est_opt', sql_cmd)
        LOG.info('--步骤4:创建表并建索引--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_113;
            create table test_113 (id int);
            insert into test_113 values(generate_series(1,100));
            create index u_dex113 on test_113 using btree(id);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤5:analyze语句检测索引文件--')
        sql_cmd = commonsh.execut_db_sql('''analyze verify fast u_dex113;
            select relname,relpages from pg_class where relname='u_dex113';
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, sql_cmd)
        self.assertIn('u_dex113', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('drop table if exists test_113;')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show sql_beta_feature;')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'sql_beta_feature={self.res}')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show sql_beta_feature;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_DeveloperOptions_Case0113finish-----')
