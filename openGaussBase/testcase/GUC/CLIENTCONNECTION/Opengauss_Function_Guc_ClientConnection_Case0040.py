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
Case Name   : 使用alter database方法设置参数temp_tablespaces为不存在的表空间名称,合理报错
Description :
        1.查询temp_tablespaces默认值
        2.创建数据库
        3.修改参数值为不存在名称
        4.删除数据库
Expect      :
        1.显示默认值为空
        2.数据库创建成功
        3.合理报错
        4.删除成功
History     :
"""
import sys
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
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0040start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_temp_tablespaces(self):
        # 查看默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show temp_tablespaces;''')
        self.log.info(sql_cmd)
        self.assertTrue(sql_cmd.splitlines()[-2].strip() == '', sql_cmd)
        # 创建数据库
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists test_spdb040 ;
                                                 create database test_spdb040;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        # 使用alter database设置temp_tablespaces为t_temp_tablespaces040
        sql_cmd = self.commonsh.execut_db_sql(f'''alter database test_spdb040 set temp_tablespaces to 't_temp_tablespaces040';''')
        self.log.info(sql_cmd)
        self.assertIn('NOTICE:  tablespace "t_temp_tablespaces040" does not exist', sql_cmd)
        sql_cmd2 = '''show temp_tablespaces;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d test_spdb040 -p {self.userNode.db_port} -c "{sql_cmd2}"
                             '''
        self.log.info(sql_cmd2)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.log.info(msg1)
        self.assertTrue(msg1.splitlines()[-2].strip() == '', msg1)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists test_spdb040;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0040执行完成---------------')
