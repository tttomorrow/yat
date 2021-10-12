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
Case Name   : \COPY FROM格式不良好导入
Description :
    1.创建测试表并插入数据
    2.构造数据文件
    3.更改数据文件使内部数据不对齐
    4.使用\COPY FROM进行数据拷贝
    5.清理环境
Expect      :
    1.创建测试表并插入数据成功
    2.构造数据文件成功
    3.更改数据文件使内部数据不对齐成功
    4.使用\COPY FROM进行数据拷贝失败
    5清理环境成功
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class CopyFile(unittest.TestCase):
    def setUp(self):
        logger.info('---------------------Opengauss_Function_DML_Copy_Case0107开始执行--------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_copy_file(self):
        logger.info('----------------------------创建测试表并对测试表插入数据-----------------------------')
        sql_cmd = '''drop table if exists testzl;
                    CREATE TABLE testzl(SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
                    insert into testzl values (1,'sk1','tt',3331);
                    insert into testzl values (2,'sk1','tt',3331);
                    insert into testzl values (3,'sk1','tt',3331);
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
                        touch {self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat;'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('------------------------向数据文件中写入数据---------------------------')
        sql_cmd = f'''copy testzl to '{self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat';'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('------------------------更改数据文件内容格式，使其不对齐--------------------------')
        excute_cmd = f'''
                        sed -i "s/2/               2/g" {self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat ;
                        cat {self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat ;
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('------------------------进行\copy from---------------------------')
        sql_cmd = f''' 
                       \copy testzl from '{self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat';
                        select count(*) from testzl;
                   '''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        res = msg.splitlines()[-2].strip()
        self.assertIn('6', res)

    def tearDown(self):
        logger.info('----------------清理环境-----------------------')
        sql_cmd = 'drop table if exists testzl;'
        excute_cmd = f'''    
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        excute_cmd = f'''rm -rf {self.DB_INSTANCE_PATH}/pg_copydir'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        logger.info('----------------------------Opengauss_Function_DML_Copy_Case0107执行完成-----------------------------')
