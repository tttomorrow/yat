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
Case Name   : 将pg_temp模式加入search_path设为搜素路径最后位置, 有告警提示;创建函数，查询模式
Description :
        1.查询search_path默认值
        2.将pg_temp加入搜索模式最后位置
        3.创建函数
        4.查询函数模式
        5.删除函数
        6.恢复参数默认值
Expect      :
        1.显示默认值
        2.弹出警告信息
        3.函数创建成功
        4.显示public模式
        5.函数删除成功
        6.参数默认值恢复成功
History     :
"""
import sys
import time
import unittest

from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0013start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')

    def test_search_path(self):
        # 查看默认值;将搜索路径pg_temp加入最后位置；创建函数；查询函数模式
        sql_cmd = self.commonsh.execut_db_sql(f'''show search_path;
                                               set search_path to public,pg_temp;
       CREATE OR REPLACE FUNCTION func_increment_plsql(i integer) RETURNS integer AS \$\$
     BEGIN
                RETURN i + 1;
     END;
 \$\$ LANGUAGE plpgsql;
     \\sf+ func_increment_plsql''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.assertIn('WARNING:', sql_cmd)
        self.assertIn(self.Constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd)
        self.assertIn('public', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop function func_increment_plsql(i integer) cascade;
                                                set search_path to default;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0013执行完成---------------')
