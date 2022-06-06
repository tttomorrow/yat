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
Case Name   : 对索引copy from 是否成功
Description :
    1. 创建测试表与索引
    2.构造数据文件
    3.对索引copy from
    4.清理环境
Expect      :
    1. 创建测试表与索引成功
    2.构造数据文件成功
    3.对索引copy from 失败
    4.清理环境
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class CopyFile(unittest.TestCase):
    def setUp(self):
        logger.info('------Opengauss_Function_DML_Copy_Case0005开始执行------')
        self.userNode = Node('PrimaryDbUser')
        self.Constant = Constant()
        self.tb_name = 't_copy_0005'

    def test_copy_file(self):
        logger.info('------建表建索引------')
        sql_cmd = f'''drop table if exists {self.tb_name};
            create table {self.tb_name}(sk integer,id char(16),
            name varchar(20),sq_ft integer);
            insert into {self.tb_name} values (001,'sk1','tt',3332);
            insert into {self.tb_name} values (001,'sk1','tt',3332);
            insert into {self.tb_name} values (001,'sk1','tt',3332);
            create index {self.tb_name}_idx on {self.tb_name}(sk);
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d {self.userNode.db_name} \
            -p {self.userNode.db_port} \
            -c "{sql_cmd}"'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertTrue(self.Constant.CREATE_TABLE_SUCCESS in msg and
                        self.Constant.CREATE_INDEX_SUCCESS_MSG in msg)

        logger.info('------构造数据文件------')
        excute_cmd = f'''mkdir {macro.DB_INSTANCE_PATH}/pg_copydir;
            touch {macro.DB_INSTANCE_PATH}/pg_copydir/{self.tb_name}.dat;'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        logger.info('------对索引copy from------')
        sql_cmd = f'''copy {self.tb_name}_idx from \
            '{macro.DB_INSTANCE_PATH}/pg_copydir/{self.tb_name}.dat';'''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.userNode.db_name} \
            -p {self.userNode.db_port}  \
            -c "{sql_cmd}"'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.COPY_INDEX_FAIL_MSG, msg)

    def tearDown(self):
        logger.info('------清理环境------')
        sql_cmd = f'''drop table if exists {self.tb_name} cascade;'''
        excute_cmd = f'''rm -rf {macro.DB_INSTANCE_PATH}/pg_copydir;
            source {macro.DB_ENV_PATH} ;
            gsql -d {self.userNode.db_name} \
            -p {self.userNode.db_port} \
            -c "{sql_cmd}"'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('------Opengauss_Function_DML_Copy_Case0005执行完成------')
