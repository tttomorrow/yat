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
Case Name   : 使用gs_guc reload方法设置参数extra_float_digits为3 ,观察预期结果
Description :
        1.查询extra_float_digits默认值
        2.修改参数值为3；建表查询
        3.恢复参数默认值
Expect      :
        1.显示默认值为0
        2.设置成功;建表且数据插入成功
        3.默认值恢复成功
History     :
"""
import sys
import unittest
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0142start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_extra_float_digits(self):

        # 查询默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show extra_float_digits;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 设置参数值为3
        msg = self.commonsh.execute_gsguc('reload', self.Constant.GSGUC_SUCCESS_MSG, 'extra_float_digits = 3')
        self.log.info(msg)
        self.assertTrue(msg)
        # 查询参数值并建表插入FLOAT4类型数据
        sql_cmd = self.commonsh.execut_db_sql(f'''show extra_float_digits;
                                                drop table if exists float_type_t3;
                                                create table float_type_t3 (FT_COL2 FLOAT4);
                                                insert into float_type_t3 values(10.365456);
                                                select * from float_type_t3;
                                                 ''')
        self.log.info(sql_cmd)
        self.assertIn('3', sql_cmd)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd)
        self.assertIn('10.3654556', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists float_type_t3;''')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql(f'''show extra_float_digits;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('reload', self.Constant.GSGUC_SUCCESS_MSG, f'extra_float_digits={self.res}')
            self.log.info(msg)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0142执行完成---------------')
