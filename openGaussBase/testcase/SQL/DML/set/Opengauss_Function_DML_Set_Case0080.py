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
Case Type   : 系统操作
Case Name   : shutdown跟无效参数,合理报错
Description :
        1.创建用户
        2.切换用户至xi，执行shutdown命令
        3.清理环境
Expect      :
        1.创建成功
        2.合理报错
        3.清理环境完成
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0080开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_shutdown(self):
        # 创建用户
        sql_cmd1 = commonsh.execut_db_sql(f'''drop user if exists xi cascade;
                                  create user xi with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
       # 切换用户至xi，执行shutdown命令，合理报错
        sql_cmd2 = '''shutdown fasty;
        shutdown immediately;'''
        excute_cmd1 = f'''
                           source {self.DB_ENV_PATH};
                           gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U xi -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                           '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  unknow parameter: fasty', msg1)
        self.assertIn('ERROR:  unknow parameter: immediately', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop user xi cascade;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0080执行结束--------------------------')
