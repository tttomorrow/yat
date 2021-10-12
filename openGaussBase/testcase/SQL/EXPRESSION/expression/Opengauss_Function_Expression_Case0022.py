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
Case Type   :功能测试
Case Name   :兼容PG的数据库，比较表达式null操作符
Description :
    1.创建兼容PG的数据库
    2.测试“”和null
    3.测试“”和notnull
    4.删除兼容PG的数据库
Expect      :
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

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Expression_Case0022开始执行-----------------------------')
        self.userNode = Node('dbuser')

        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        logger.info('----------------------------创建兼容PG的数据库-----------------------------')
        sql_cmd = '''
                    drop database if exists pguser;
                    create database pguser DBCOMPATIBILITY 'PG';
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, msg)

        logger.info('----------------------------测试“”和null-----------------------------')
        sql_cmd = '''
                    select '' IS NULL AS RESULT;
                    select '' ISNULL AS RESULT;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("f", msg)

        logger.info('----------------------------测试“”和notnull-----------------------------')
        sql_cmd = '''
                    select '' IS NOT NULL AS RESULT;
                    select '' NOTNULL AS RESULT;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d pguser -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("t", msg)
        self.assertNotIn("f", msg)

    # 清理环境
    def tearDown(self):
        logger.info('----------------------------删除兼容PG的数据库-----------------------------')
        sql_cmd = '''
                    drop database if exists pguser;
                    '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('------------------------Opengauss_Function_Expression_Case0022执行结束--------------------------')
