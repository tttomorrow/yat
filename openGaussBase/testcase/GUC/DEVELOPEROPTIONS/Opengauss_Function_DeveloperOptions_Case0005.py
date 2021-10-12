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
Case Name   : 使用ALTER SYSTEM SET 法设置参数allow_system_table_mods为on，
             给系统表重命名字段
Description :
        1.查询allow_system_table_mods默认值
        2.修改参数值为on并重启数据库
        3.
        4.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.设置成功
        3.设置成功
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
        self.constant = Constant()
        LOG.info(
            '-----Opengauss_Function_DeveloperOptions_Case0005start---')

    def test_allow_system_table_mods(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show allow_system_table_mods;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('--步骤2:设置allow_system_table_mods为on并重启数据库--')
        sql_cmd = commonsh.execut_db_sql('alter system set '
                                         'allow_system_table_mods to on;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.ALTER_SYSTEM_SUCCESS_MSG, sql_cmd)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show allow_system_table_mods;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('--步骤4:查询oid大于一万的系统表并重命名字段--')
        sql_cmd = commonsh.execut_db_sql('''select oid,relname from
            gs_wlm_instance_history where oid >=10000 and relkind='r';
            alter table gs_wlm_instance_history rename column used_cpu to
            used_cpu_new;
            ''')
        LOG.info(sql_cmd)
        self.assertIn('gs_wlm_instance_history', sql_cmd)
        self.assertIn(self.constant.ALTER_TABLE_MSG, sql_cmd)
        LOG.info('--步骤5:恢复字段原名--')
        sql_cmd = commonsh.execut_db_sql('''alter table gs_wlm_instance_history
            rename column used_cpu_new to used_cpu;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.ALTER_TABLE_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('''show allow_system_table_mods;''')
        LOG.info(sql_cmd)
        if "off" != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'allow_system_table_mods=off')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show allow_system_table_mods;''')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_DeveloperOptions_Case0005执行完成-----')
