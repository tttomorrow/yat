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
Case Type   : 系统信息函数
Case Name   :  pg_is_other_temp_schema(oid) 查看是否为另一个会话的临时模式
Description :
    1.在同一会话中创建临时表，查看是否为另一个会话的临时模式的OID
Expect      :
     1.在同一会话中创建临时表，查看是否为另一个会话的临时模式的OID，结果为f
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0008开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.创建临时表，再查看临时模式的OID，显示临时模式OID-')
        sql_cmd = self.commonsh.execut_db_sql(
            f'create  temp table tmtable(i int, info varchar(50));'
            f'select pg_my_temp_schema();')
        LOG.info(sql_cmd)
        oid = int(sql_cmd.split('\n')[3].strip())
        LOG.info(oid)
        if oid >= 0:
            LOG.info('查看临时模式的OID成功')
        else:
            raise Exception('查看异常，请检查')
        LOG.info(f'-步骤2.pg_is_other_temp_schema(oid) 查看是否为另一个会话的临时模式-')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select  pg_is_other_temp_schema({oid});')
        LOG.info(sql_cmd)
        self.assertIn('f', sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0008结束-')
