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
Case Name   : 使用alter database方法设置参数lc_monetary为en_US,观察预期结果
Description :
        1.查询lc_monetary默认值
        2.创建数据库
        3.修改参数值为en_US，并使用查询
        4.删除数据库
Expect      :
        1.显示默认值C
        2.数据库创建成功
        3.设置成功；查询显示美元符号
        4.删除成功
History     :
"""
import sys
import unittest
import time
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0152start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_lc_monetary(self):

        # 查询默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show lc_monetary;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 创建数据库
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists test_spdb152;
                                                 create database test_spdb152;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        # 修改数据库级别参数
        sql_cmd = self.commonsh.execut_db_sql(f'''alter database test_spdb152 set lc_monetary to 'en_US';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        # 查询参数值并查询货币类型显示格式
        sql_cmd2 = '''show lc_monetary;
                      SELECT 12.13::money;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d test_spdb152 -p {self.userNode.db_port} -c "{sql_cmd2}"
                             '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertIn('en_US', msg1)
        self.assertIn('$12.13', msg1)


    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists test_spdb152;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0152执行完成---------------')
