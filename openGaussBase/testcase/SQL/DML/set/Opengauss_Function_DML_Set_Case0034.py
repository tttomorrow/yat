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
Case Type   : 系统操作
Case Name   : 使用set session和set local命令，设置xml解析方式
Description :
        1.查看默认xml解析方式
        2.set session命令设置xml解析方式为document
        3.查看默认xml解析方式
        4.通过系统表查看该参数运行时的具体信息
        5.重新连接数据库,查看默认xml解析方式
        6.set local命令设置xml解析方式为document
        7.查看默认xml解析方式
Expect      :
        1.解析方式为CONTENT
        2.设置成功
        3.显示document
        4.查询成功
        5.恢复为默认值CONTENT
        6.设置成功
        7.仍然是默认值CONTENT，local命令不生效
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0034开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_set(self):
        # 查看默认xml解析方式为CONTENT
        # set session命令设置xml解析方式为document
        # 查看默认xml解析方式
        # 通过系统表查看该参数运行时的具体信息
        sql_cmd1 = commonsh.execut_db_sql('''show xmloption;
                                      set session xml option document;
                                      show xmloption;
                                      select name,setting from pg_settings where name ='xmloption';''')
        logger.info(sql_cmd1)
        self.assertIn('content', sql_cmd1)
        self.assertIn(self.Constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('document', sql_cmd1)
        # 重新连接数据库,查看默认xml解析方式,恢复为默认值CONTENT
        sql_cmd2 = ('''show xmloption;''')
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port}  -c "{sql_cmd2}"
                                  '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('content', msg1)
        # set local命令设置xml解析方式为document
        # 查看默认xml解析方式，仍然是默认值CONTENT，local命令不生效
        sql_cmd3 = commonsh.execut_db_sql('''set local xml option document;
                                      show xmloption;''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.SET_SUCCESS_MSG, sql_cmd3)
        self.assertIn('content', sql_cmd3)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0034执行结束--------------------------')
