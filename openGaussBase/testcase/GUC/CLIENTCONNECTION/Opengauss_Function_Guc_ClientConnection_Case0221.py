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
Case Name   : 使用gs_guc reload方法设置参数IntervalStyle值，检查预期结果
Description :
        1.查询IntervalStyle默认值
        2.修改参数值为sql_standard
        3.建表指定数据类型为INTERVAL并插入数据
        4.查询表数据
        5.恢复参数默认值
Expect      :
        1.显示默认值为postgres
        2.修改成功
        3.建表且插入数据成功
        4.INTERVAL DAY(3) TO SECOND (4)类型显示为3 0:00:00
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
            '---Opengauss_Function_Guc_ClientConnection_Case0221start-----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_IntervalStyle(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql(f'''show IntervalStyle;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:修改参数值为sql_standard--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          "IntervalStyle = 'sql_standard'")
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤3:查询--')
        sql_cmd = self.commonsh.execut_db_sql(f'''show IntervalStyle;''')
        self.log.info(sql_cmd)
        self.assertIn('sql_standard', sql_cmd)
        self.log.info('--步骤4:建表，插入Interval类型数据并查询--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists 
            day_type_tab221;
            create table day_type_tab221 (a int,b INTERVAL DAY(3) TO SECOND
            (4));
            insert into day_type_tab221 VALUES (1, INTERVAL '3' DAY);
            select * from day_type_tab221;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn('3 0:00:00', sql_cmd)

    def tearDown(self):
        self.log.info('--步骤4:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists
            day_type_tab221;''')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql('''show IntervalStyle;
            drop table if exists day_type_tab221;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"IntervalStyle='{self.res}'")
            self.log.info(msg)
        self.log.info(
            '-----Opengauss_Function_Guc_ClientConnection_Case0221finish--')
