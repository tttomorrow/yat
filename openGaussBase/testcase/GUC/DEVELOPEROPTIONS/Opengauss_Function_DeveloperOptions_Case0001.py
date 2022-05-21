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
Case Name   : 使用gs_guc set方法设置参数allow_system_table_mods为on，
              给系统表增加字段(只能修改oid大于等于一万的系统表)
Description :
        1.查询allow_system_table_mods默认值
        2.修改参数值为on并重启数据库
        3.给系统表oid大于一万的表添加字段
        4.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.修改成功，显示on
        3.添加成功
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
        self.constant = Constant()
        self.user_node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        LOG.info(
            '------Opengauss_Function_DeveloperOptions_Case0001start------')

    def test_allow_system_table_mods(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show allow_system_table_mods;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('--步骤2:设置allow_system_table_mods为on并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'allow_system_table_mods =on')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('show allow_system_table_mods;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)
        LOG.info('--步骤4:查询oid大于一万的系统表并给系统表添加字段--')
        sql_cmd = '''select oid,relname from pg_class where oid >=10000 \
            and relkind='r';
            alter table gs_wlm_instance_history add testname varchar(20);
            '''
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f' gsql -d postgres  ' \
                      f'-p {self.user_node.db_port}' \
                      f' -c "{sql_cmd}" '
        LOG.info(excute_cmd1)
        msg1 = self.user_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn('gs_wlm_instance_history', msg1)
        self.assertIn(self.constant.ALTER_TABLE_MSG, msg1)
        LOG.info('--步骤5:系统表gs_wlm_instance_history删除字段--')
        sql_cmd = 'alter table gs_wlm_instance_history drop column testname;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f' gsql -d postgres' \
                      f' -p {self.user_node.db_port} ' \
                      f' -c "{sql_cmd}" '
        LOG.info(excute_cmd1)
        msg1 = self.user_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.constant.ALTER_TABLE_MSG, msg1)

    def tearDown(self):
        LOG.info('--步骤6:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('show allow_system_table_mods;')
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
        sql_cmd = commonsh.execut_db_sql('show allow_system_table_mods;')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_DeveloperOptions_Case0001执行完成-----')
