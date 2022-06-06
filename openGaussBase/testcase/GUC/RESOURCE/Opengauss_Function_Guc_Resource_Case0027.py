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
Case Name   : 修改参数standby_shared_buffers_fraction，观察预期结果；
Description :
        1、查询standby_shared_buffers_fraction默认值；
        2、修改standby_shared_buffers_fraction为0.5，重启使其生效，
         并校验其预期结果；
        3、主机建表并插入数据
        4、备机执行explain
        5、恢复默认值；
Expect      :
        1、显示默认值；
        2、参数修改成功，校验修改后系统参数值为0.5；
        3、建表并插入数据成功
        4.执行explain成功，显示Buffers: shared信息
        5、恢复默认值成功；
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_Resource_Case00027.py start------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.Standby_sh = CommonSH('Standby1DbUser')

    def test_startdb(self):
        self.log.info('查询该参数默认值')
        sql_cmd = self.commonsh.execut_db_sql('''show 
            standby_shared_buffers_fraction;''')
        self.log.info(sql_cmd)
        self.assertEqual('0.3', sql_cmd.splitlines()[-2].strip())
        self.log.info('gs_guc set设置standby_shared_buffers_fraction')
        msg = self.commonsh.execute_gsguc('set',
                                          self.Constant.GSGUC_SUCCESS_MSG,
                                          'standby_shared_buffers_fraction'
                                          '=0.5')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('查询修改后的值')
        sql_cmd = self.commonsh.execut_db_sql('''show 
            standby_shared_buffers_fraction;''')
        self.log.info(sql_cmd)
        self.assertIn('0.5', sql_cmd)
        self.log.info('建表后备机执行explain')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists test027;
        create table test027(c_1 INTEGER,
                  c_2 BIGINT,
                  c_3 SMALLINT,
                  c_4 TINYINT,
                  c_5 SERIAL,
                  c_6 SMALLSERIAL,
                  c_7 BIGSERIAL,
                  c_8 FLOAT,
                  c_9 DOUBLE PRECISION,
                  c_10 DATE,
                  c_11 time without time zone,
                  c_12 timestamp without time zone,
                  c_13 CHAR(10),
                  c_14 VARCHAR(20),
                  c_15 TEXT,
                  c_16 BLOB,
                  c_17 BYTEA);
        insert into test027 values(1,10,5,25,default,default,default,1237.127,\
        123456.1234,date '12-10-2010','21:21:21','2010-12-12','测试',\
        '测试工程师','西安',empty_blob(),E'\\xDEADBEEF');''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd)
        sql_cmd = self.Standby_sh.execut_db_sql('''explain (analyze,buffers) 
        select * from test027;''')
        self.log.info(sql_cmd)
        self.log.info('Buffers: shared hit', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql('drop table if exists test027;')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql('''show 
            standby_shared_buffers_fraction;''')
        self.log.info(sql_cmd)
        if '0.3' != sql_cmd.splitlines()[-2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.Constant.GSGUC_SUCCESS_MSG,
                                              'standby_shared_buffers_fraction'
                                              '=0.3')
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '---Opengauss_Function_Guc_Resource_Case0027.py执行完成-----')
