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
Case Type   : 拷贝数据
Case Name   : copy_error_log_create() 函数是否可以正常创建
Description :
    1.查看pgxc_copy_error_log表是否存在
    2.执行copy_error_log_create()函数创建新的pgxc_copy_error_log表
    3.进行校验
    4.清理环境
Expect      :
    1.查看pgxc_copy_error_log表成功
    2.执行copy_error_log_create()函数创建新的pgxc_copy_error_log表成功
    3.检验成功
    4.清理环境成功
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class CopyFile(unittest.TestCase):
    def setUp(self):
        logger.info('----------------------------Opengauss_Function_DML_Copy_Case0102开始执行-----------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_copy_file(self):
        logger.info('----------------------------查看pgxc_copy_error_log表是否存在，若存在，则删除-----------------------------')
        sql_cmd = 'drop table if exists pgxc_copy_error_log;'
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('------------------执行copy_error_log_create()函数创建新的pgxc_copy_error_log表-----------')
        sql_cmd = f'SELECT copy_error_log_create();'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn('t', msg.splitlines()[-2].strip())

        logger.info('---------------------验证pgxc_copy_error_log表是否创建成功-------------------------')
        sql_cmd = 'select * from pgxc_copy_error_log;'
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

    def tearDown(self):
        sql_cmd = 'drop table if exists pgxc_copy_error_log;'
        excute_cmd = f'''
                            source {self.DB_ENV_PATH} ;
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('----------------------------Opengauss_Function_DML_Copy_Case0102执行完成-----------------------------')
