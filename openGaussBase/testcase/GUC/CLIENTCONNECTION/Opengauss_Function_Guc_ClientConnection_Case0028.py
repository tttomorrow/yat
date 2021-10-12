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
Case Name   : 使用gs_guc set方法设置参数default_tablespace,建表指定不存在
              的表空间，合理报错
Description :
        1.查询default_tablespace默认值
        2.gs_guc set设置参数值为t_tablespace028并重启数据库
        3.查询该参数修改后的值
        4.建表，指定不存在的表空间
        5.恢复参数默认值
Expect      :
        1.显示默认值为空
        2.设置成功
        3.显示t_tablespace028
        4.合理报错
        5.默认值恢复成功
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
            '---Opengauss_Function_Guc_ClientConnection_Case0028start---')
        self.constant = Constant()
        self.expect_res = 'ERROR:  tablespace "t_tablespace027" does not exist'

    def test_defaul_tablespace(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show default_tablespace;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:gs_guc set设置参数值为t_tablespace028并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "default_tablespace='t_tablespace028'")
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show default_tablespace;''')
        LOG.info(sql_cmd)
        self.assertIn('t_tablespace028', sql_cmd)
        LOG.info('--步骤4:建表，指定不存在的表空间，报错--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_028;
            create table test_028(id int)TABLESPACE t_tablespace027;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.expect_res, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤5:清理环境--')
        sql_cmd = commonsh.execut_db_sql('''show default_tablespace;''')
        LOG.info(sql_cmd)
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "default_tablespace=''")
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show default_tablespace;''')
        LOG.info(sql_cmd)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0028执行完成---')
