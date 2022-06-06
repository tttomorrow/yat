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
Case Name   : 使用gs_guc reload方法设置参数default_tablespace,建表，指定不存在的表空间，合理报错
Description :
        1.查询default_tablespace默认值
        2.修改参数值为新表空间名并查询
        3.建表，指定不存在的表空间
        4.恢复参数默认值
Expect      :
        1.显示默认值为空
        2.设置成功
        3.合理报错
        4.默认值恢复成功
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
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0027start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_default_tablespace(self):
        # 查看默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show default_tablespace;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 修改参数值为t_tablespace027
        msg = self.commonsh.execute_gsguc('reload', self.Constant.GSGUC_SUCCESS_MSG,
                                         "default_tablespace='t_tablespace027'")
        self.log.info(msg)
        self.assertTrue(msg)
        # 查询该参数修改后的值
        sql_cmd = self.commonsh.execut_db_sql(f'''show default_tablespace;''')
        self.log.info(sql_cmd)
        self.assertIn('t_tablespace027', sql_cmd)
        # 建表，指定不存在的表空间，报错
        sql_cmd = self.commonsh.execut_db_sql(f'''drop table if exists test_027;
                                                create table test_027(id int)TABLESPACE t_tablespace027;''')
        self.log.info(sql_cmd)
        self.assertIn('ERROR:  tablespace "t_tablespace027" does not exist', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''show default_tablespace;''')
        self.log.info(sql_cmd)
        current_value = sql_cmd.splitlines()[-2].strip()
        self.log.info(current_value)
        self.log.info(str(type(self.res)) + " : " + self.res)
        if self.res != current_value:
            msg = self.commonsh.execute_gsguc('reload', self.Constant.GSGUC_SUCCESS_MSG,
                                              f'''default_tablespace = '{self.res}' ''')
            self.log.info(msg)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0027执行完成---------------')
