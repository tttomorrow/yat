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
Case Name   : 使用gs_guc reload方法设置参数bytea_output为escape ,观察预期结果
Description :
        1.查询bytea_output默认值
        2.建表插入bytea类型数据
        3.修改参数值为escape
        4.建表插入bytea类型数据
        5.恢复参数默认值
Expect      :
        1.显示默认值为hex
        2.建表成功且插入数据成功
        3.设置成功
        4.建表成功且插入数据成功
        5.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0097start-----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_bytea_output(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show bytea_output;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:建表并插入数据--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists
            blob_type_t1_097 cascade;
            CREATE TABLE blob_type_t1_097 (BT_COL1 BYTEA);
            INSERT INTO blob_type_t1_097 VALUES(E'\\\\\\xDEADBEEF');
            SELECT * FROM blob_type_t1_097;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn('\\xdeadbeef', sql_cmd)
        self.log.info('--步骤3:修改参数为escape--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          "bytea_output = 'escape'")
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤4:查询修改后的参数值--')
        sql_cmd = self.commonsh.execut_db_sql('''show bytea_output;''')
        self.log.info(sql_cmd)
        self.assertIn('escape', sql_cmd)
        self.log.info('--步骤5:建表并插入数据--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if 
            exists blob_type_t1_097bak cascade;
            CREATE TABLE blob_type_t1_097bak (BT_COL1 BYTEA);
            INSERT INTO blob_type_t1_097bak VALUES(E'\\\\\\xDEADBEEF');
            SELECT * FROM blob_type_t1_097bak;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn('\\336\\255\\276\\357', sql_cmd)

    def tearDown(self):
        self.log.info('--步骤6:清理环境--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists
            blob_type_t1_097;
            drop table if exists blob_type_t1_097bak;''')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql('''show bytea_output;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"bytea_output='{self.res}'")
            self.log.info(msg)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0097执行完成----')
