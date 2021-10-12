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
Case Name   : copy from 与copy to进行大数据量copy
Description :
    1.创建测试表并插入大量数据
    2.构造数据文件,进行大数据量COPY TO
    3.进行大数据量COPY FROM
    4.清理环境
Expect      :
    1.创建测试表并插入大量数据
    2.构造数据文件,进行大数据量COPY TO
    3.进行大数据量COPY FROM
    4.清理环境
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
        logger.info('------------------------Opengauss_Function_DML_Copy_Case0006开始执行-----------------------------')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
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

        logger.info('----------------------------插入数据-----------------------------')
        for i in range(0, 1000):
            insert_sql = f"insert into testzl values ({i},'sk1','tt',3332);"
            insert_cmd = f'''
                   source {self.DB_ENV_PATH};
                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{insert_sql}";
                   '''
            insert_msg = self.userNode.sh(insert_cmd).result()
            logger.info(insert_msg)
        logger.info('insert completed')

        logger.info('-----------------构造数据文件,进行大数据量COPY TO------------------')
        sql_cmd = f'''copy testzl to '{self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat';'''
        excute_cmd = f'''mkdir {self.DB_INSTANCE_PATH}/pg_copydir;
                        touch {self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat;
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('----------------------进行大数据量的COPY FROM--------------------------')
        sql_cmd = f'''copy testzl from '{self.DB_INSTANCE_PATH}/pg_copydir/testzl.dat';'''
        excute_cmd = f'''
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port}  -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

    def tearDown(self):
        logger.info('----------------------------清理环境-----------------------------')
        sql_cmd = '''drop table if exists testzl cascade;'''
        excute_cmd = f'''
                        rm -rf {self.DB_INSTANCE_PATH}/pg_copydir;
                        source {self.DB_ENV_PATH} ;
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('----------------------------Opengauss_Function_DML_Copy_Case0006执行完成-----------------------------')
