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
Case Type   : 拷贝数据
Case Name   : text文件中的内容是否可以导入数据库表中(不指定分隔符)
Description :
    1.创建测试表
    2.创建数据文件并写入文件内容
    3.将copydata.text文件中的数据拷贝到testzl表中
    4.进行校验
    5.清理环境
Expect      :
    1.创建测试表成功
    2.创建数据文件并写入文件内容成功
    3.将copydata.text文件中的数据拷贝到testzl表中成功
    4.校验成功
    5.清理环境成功
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
        logger.info('----------------------------Opengauss_Function_DML_Copy_Case0028开始执行-----------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_copy_file(self):
        logger.info('----------------------------创建测试表-----------------------------')
        sql_cmd = '''drop table if exists testzl;
                    CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
                    '''
        excute_cmd = f'''
                    source {self.DB_ENV_PATH} ;
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

        logger.info('----------------------------创建数据文件-----------------------------')
        excute_cmd = f'''mkdir {self.DB_INSTANCE_PATH}/pg_copydir;
                        touch {self.DB_INSTANCE_PATH}/pg_copydir/copydata.text;'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('--------------------------向新的文件中写入内容---------------------------')
        excute_cmd = f'''
                        echo "001	sk1	tt	3332" >>  {self.DB_INSTANCE_PATH}/pg_copydir/copydata.text;
                        echo "001	sk1	tt	3332" >>  {self.DB_INSTANCE_PATH}/pg_copydir/copydata.text;
                        echo "001	sk1	tt	3332" >>  {self.DB_INSTANCE_PATH}/pg_copydir/copydata.text;
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('--------------------------进行数据导入--------------------------')
        sql_cmd = f'''copy testzl from '{self.DB_INSTANCE_PATH}/pg_copydir/copydata.text';'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('---------------------------进行校验---------------------------')
        sql_cmd = f'''select count(*) from testzl ;'''
        excute_cmd = f'''
                       source {self.DB_ENV_PATH} ;
                       gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                       '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn('3', res)

    def tearDown(self):
        logger.info('----------------清理环境-----------------------')
        sql_cmd = '''drop table if exists testzl;'''
        excute_cmd = f'''    
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info(msg)
        excute_cmd = f'''rm -rf {self.DB_INSTANCE_PATH}/pg_copydir'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('----------------------------Opengauss_Function_DML_Copy_Case0028执行完成-----------------------------')
