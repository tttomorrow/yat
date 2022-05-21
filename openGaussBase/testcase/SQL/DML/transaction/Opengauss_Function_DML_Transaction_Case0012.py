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
Case Type   : 事务控制
Case Name   : 将访问表数据语句放在匿名块变量中执行
Description : 1.新建测试表 2.使用匿名块对主机数据进行访问 3.使用匿名块对备机数据进行访问
Expect      :
    1.创建测试表并插入数据
    2.将select语句放在匿名块变量中执行，对数据进行访问成功
    3.在备机上开启事务使用匿名块进行数据访问成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class TransactionFile(unittest.TestCase):
    def setUp(self):
        logger.info('----Opengauss_Function_DML_Transaction_Case0012开始执行----')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.commonsh = CommonSH('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_transaction_file(self):
        logger.info('------若为单机环境，后续不执行，直接通过------')
        excute_cmd = f'''source {self.DB_ENV_PATH}
            gs_om -t status --detail'''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')
            logger.info('------新建测试表------')
            sql_cmd = '''drop table if exists testzl;
                create table testzl (SK INTEGER,ID CHAR(16),
                NAME VARCHAR(20),SQ_FT INTEGER);
                insert into testzl values (001,'sk1','tt',3332);'''
            excute_cmd = f'''source {self.DB_ENV_PATH} ;
                gsql -d {self.PrimaryNode.db_name} \
                -p {self.PrimaryNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg)

            logger.info('------使用匿名块对主机数据进行访问------')
            sql_cmd = f'''declare 
                            t1 int;
                            v_sql varchar;
                          begin
                            v_sql := 'select count(*) into t1 from testzl;';
                            execute immediate v_sql ;
                          end;
                          '''
            excute_cmd = f'''source {self.DB_ENV_PATH} ;
                gsql -d {self.PrimaryNode.db_name} \
                -p {self.PrimaryNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.PrimaryNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          msg)

            select_cmd = f'''select * from t1;'''
            logger.info(select_cmd)
            select_res = self.commonsh.execut_db_sql(select_cmd)
            logger.info(select_res)
            self.assertTrue(int(select_res.splitlines()[-2].strip()) == 1)

            logger.info('------使用匿名块对备机数据进行访问------')
            sql_cmd = f'''declare 
                            t2 int;
                            v_sql varchar;
                          begin
                            v_sql := 'select * from testzl;';
                            execute immediate v_sql ;
                          end;
                          '''
            excute_cmd = f'''source {self.DB_ENV_PATH} ;
                gsql -d {self.StandbyNode.db_name} \
                -p {self.StandbyNode.db_port} \
                -c "{sql_cmd}"'''
            logger.info(excute_cmd)
            msg = self.StandbyNode.sh(excute_cmd).result()
            logger.info(msg)
            self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG, msg)

    def tearDown(self):
        logger.info('------清理环境------')
        sql_cmd = f'''drop table if exists testzl;
            drop table t1 cascade;'''
        excute_cmd = f'''source {self.DB_ENV_PATH} ;
            gsql -d {self.PrimaryNode.db_name} \
            -p {self.PrimaryNode.db_port} \
            -c "{sql_cmd}"'''
        logger.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, msg)
        logger.info('------Opengauss_Function_DML_Transaction_Case0012执行完成------')
