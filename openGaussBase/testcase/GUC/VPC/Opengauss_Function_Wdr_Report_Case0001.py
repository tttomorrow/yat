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
Case Type   : 快照报告功能
Case Name   : 设置快照报告开关
Description :
    1.创建测试数据库
    2.设置快照开关
    3.清理环境
Expect      :
    1.创建测试数据库正常
    2.设置快照开关参数正常
    3.清理环境成功
History     : 
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
        logger.info('----------------------------Opengauss_Function_Wdr_Report_Case0001开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_copy_file(self):
        logger.info('----------------------------查看快照开关参数值-----------------------------')
        sql_cmd = ''' 
                show enable_wdr_snapshot;       
                '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn(self.Constant.BOOLEAN_VALUES[1], res)

        logger.info('----------------------------设置快照开关参数值-----------------------------')
        sql_cmd = ''' 
                alter system set enable_wdr_snapshot = on;       
                '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.ALTER_SYSTEM_SUCCESS_MSG, msg)

        logger.info('----------------------------查看快照开关参数值-----------------------------')
        sql_cmd = ''' 
                show enable_wdr_snapshot;       
                '''
        excute_cmd = f'''
                   source {self.DB_ENV_PATH} ;
                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                   '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn(self.Constant.BOOLEAN_VALUES[0], res)

        logger.info('----------------------------设置快照开关参数值-----------------------------')
        sql_cmd = ''' 
                alter system set enable_wdr_snapshot = off;       
                '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.ALTER_SYSTEM_SUCCESS_MSG, msg)

        logger.info('----------------------------查看快照开关参数值-----------------------------')
        sql_cmd = ''' 
                show enable_wdr_snapshot;       
                '''
        excute_cmd = f'''
                   source {self.DB_ENV_PATH} ;
                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                   '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn(self.Constant.BOOLEAN_VALUES[1], res)

    def tearDown(self):
        logger.info('----------------清理环境-----------------------')
        sql_cmd = '''
                alter system set enable_wdr_snapshot = off;
                '''
        excute_cmd = f'''    
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.ALTER_SYSTEM_SUCCESS_MSG, msg)

        logger.info('----------------------------Opengauss_Function_Wdr_Report_Case0001执行完成-----------------------------')

