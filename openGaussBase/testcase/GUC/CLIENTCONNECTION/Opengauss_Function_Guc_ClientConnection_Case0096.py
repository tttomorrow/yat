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
Case Name   : 使用gs_guc set方法设置参数bytea_output为escape ,观察预期结果
Description :
        1.查询bytea_output默认值
        2.默认值hex下建表并插入数据
        3.修改参数值为escape并重启数据库
        4.查询修改后的参数值
        5.建表并插入数据
        6.恢复参数默认值
Expect      :
        1.显示默认值为hex
        2.建表并插入数据成功
        3.设置成功
        4.显示escape
        5.建表并插入数据成功
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
            '-----Opengauss_Function_Guc_ClientConnection_Case0096start----')
        self.constant = Constant()

    def test_bytea_output(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show bytea_output;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:建表并插入数据--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists 
            blob_type_t1_096 cascade;
            create table blob_type_t1_096 (bt_col1 bytea);
            insert into blob_type_t1_096 values(e'\\\\\\xdeadbeef');
            select * from blob_type_t1_096;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn('\\xdeadbeef', sql_cmd)
        LOG.info('--步骤3:修改参数值为escape并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "bytea_output = 'escape'")
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤4:查询修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('''show bytea_output;''')
        LOG.info(sql_cmd)
        self.assertIn('escape', sql_cmd)
        LOG.info('--步骤5:建表并插入数据--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists 
            blob_type_t1_096bak cascade;
            create table blob_type_t1_096bak (bt_col1 bytea);
            insert into blob_type_t1_096bak values(e'\\\\\\xdeadbeef');
            select * from blob_type_t1_096bak;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn('\\336\\255\\276\\357', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('''drop table if 
            exists blob_type_t1_096 cascade;
            drop table if exists blob_type_t1_096bak cascade;''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''show bytea_output;''')
        LOG.info(sql_cmd)
        if sql_cmd.split('\n')[-2].strip() != self.res:
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"bytea_output='{ self.res}'")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show bytea_output;''')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0096执行完成----')
