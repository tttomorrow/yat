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
Case Type   : 自定义数据类型
Case Name   : superuser用户删除自定义类型
Description :
        1.初始用户自定义数据类型
        2.删除自定义数据类型且添加if exists选项
Expect      :
        1.创建成功
        2.删除成功
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

class Type(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0011开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('dbuser')
        self.Constant = Constant()
    def test_delete_type(self):

        # 初始用户自定义数据类型
        sql_cmd1 = '''drop type if exists t_type1 cascade;
                    CREATE TYPE t_type1 AS (f1 int, f2 DECIMAL(10,4));'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U {self.userNode.ssh_user} -c "{sql_cmd1}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_TYPE_SUCCESS_MSG,msg1)
        # 初始用户删除自定义数据类型且添加if exists选项,删除成功
        sql_cmd2 = '''drop type if exists t_type1;
                            '''
        excute_cmd2 = f'''
                                source {self.DB_ENV_PATH};
                                gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U {self.userNode.ssh_user} -c "{sql_cmd2}"
                                '''
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.DROP_TYPE_SUCCESS_MSG, msg2)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0011执行结束--------------------------')





