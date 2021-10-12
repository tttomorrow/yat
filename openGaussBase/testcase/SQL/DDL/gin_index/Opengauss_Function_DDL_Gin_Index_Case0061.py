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
Case Type   : 功能
Case Name   : 分区表创建索引后dump，reindex索引， 恢复数据
Description :
    1.执行create_column.sql创建数据仅插入10行，该备份方式不适合大数据量
    2.创建索引
    3.dumpall数据
    4. alter索引名称
    5.恢复数据
    6.查询索引
    7.删除索引
    8.恢复数据
    9.查询索引
    10.查询
Expect      :
    1.创建表并插入数据成功
    2.创建索引成功
    3.dump成功
    4. alter 索引名称成功
    5.恢复数据成功
    6.索引存在
    7.删除索引成功
    8.恢复数据成功
    9.查询索引存在
    10.正常使用索引且查询结果正确
History     :
"""
import os
import unittest
from yat.test import Node
import time
from yat.test import macro
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
logger = Logger()
common = Common()

class set_search_limit(unittest.TestCase):

    dbPrimaryUserNode = Node(node='PrimaryDbUser')
    dbPrimaryRootNode = Node(node='PrimaryRoot')
    commsh = CommonSH('PrimaryDbUser')
    target_path = os.path.join(macro.DB_INSTANCE_PATH, 'testscript')
    sql_path = os.path.join(target_path, 'create_column_little.sql')
    dump_file_name = 'Opengauss_Gin_Index_0061.tar'
    backup_path = os.path.join(macro.PG_LOG_PATH, 'back')

    def setUp(self):
        logger.info("-----------this is setup-----------")
        self.Constant = Constant()
        logger.info("-----------Opengauss_Gin_Index_0061 start-----------")
        self.dbname = 'dbsys_restore_db'
        logger.info("---------------------create database--------------------")
        result = self.commsh.execut_db_sql(f'drop database if exists {self.dbname};create database {self.dbname};')
        logger.info(result)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, result)

    def test_set_search_limit(self):
        
        logger.info('---------------execute create_column_little.sql---------------------')
        common.scp_file(self.dbPrimaryUserNode, 'create_column_little.sql', self.target_path)
        sql_bx_cmd = f'''
                        source {macro.DB_ENV_PATH};    
                        gsql -d {self.dbname} -p {self.dbPrimaryUserNode.db_port}  -f {self.sql_path}
                       
                        '''
        logger.info(sql_bx_cmd)
        sql_bx_msg = self.dbPrimaryUserNode.sh(sql_bx_cmd).result()
        logger.info(sql_bx_msg)
        
        logger.info('------------------create index-------------------------')
        sql = 'CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector(\'english\', first_name));'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find(self.Constant.CREATE_INDEX_SUCCESS_MSG)>-1)
        
        logger.info('--------------------backup-------------------------')
        cmd = 'mkdir ' + self.backup_path
        logger.info(cmd)
        self.dbPrimaryUserNode.sh(cmd)
        dumpCmd = '''
            source {source_path};
            gs_dumpall -p {port} -f {backup_path}'''.format(source_path = macro.DB_ENV_PATH, port = self.dbPrimaryUserNode.db_port , backup_path = self.backup_path+'/dump')
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.Constant.DUMPALL_SUCCESS_MSG) > -1)
        
        logger.info('----------------alter index-----------------------')
        sql = 'alter index test_gin_2_first_name_idx rename to test_idex;'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find(self.Constant.ALTER_INDEX_SUCCESS_MSG)>-1)

        logger.info('--------------------restore database-------------------------')
        dumpCmd = '''
            source {source_path};
            gsql -d {dbname} -p {port} -r -f {backup_path}'''.format(source_path = macro.DB_ENV_PATH, dbname = self.dbname ,port = self.dbPrimaryUserNode.db_port , backup_path = self.backup_path+'/dump')
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.Constant.CREATE_INDEX_SUCCESS_MSG) > -1)
        
        logger.info('------------------check index-------------------------')
        sql = '\di'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find('test_idex')>-1)
        self.assertTrue(msg.find('test_gin_2_first_name_idx')>-1)
        
        logger.info('----------------drop index-----------------------')
        sql = 'drop index test_gin_2_first_name_idx;'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        self.assertTrue(msg.find(self.Constant.DROP_INDEX_SUCCESS_MSG)> -1)
        
        logger.info('--------------------restore database-------------------------')
        dumpCmd = '''
            source {source_path};
            gsql -d {dbname} -p {port} -r -f {backup_path}'''.format(source_path = macro.DB_ENV_PATH, dbname = self.dbname ,port = self.dbPrimaryUserNode.db_port , backup_path = self.backup_path+'/dump')
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.Constant.CREATE_INDEX_SUCCESS_MSG) > -1)

        logger.info('------------------check index-------------------------')
        sql = '\di'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find('test_idex')>-1)
        self.assertTrue(msg.find('test_gin_2_first_name_idx')>-1)
        
        logger.info('------------------querry-------------------------')
        sql = "SET ENABLE_SEQSCAN=off;SELECT * FROM test_gin_2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'Mexico\');explain SELECT * FROM test_gin_2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'Mexico\');"
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find('13 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('14 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexicox')>-1)
        self.assertTrue(msg.find('15 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexicos')>-1)
        self.assertTrue(msg.find('CStore Index Ctid Scan on test_gin_2_first_name_idx')>-1)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        logger.info('----------------drop table-----------------------')
        sql = 'drop table test_gin_2;'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        logger.info("-----------delete scripts-----------")
        cmd = 'rm -rf ' + self.target_path
        self.dbPrimaryRootNode.sh(cmd)
        logger.info("-----------delete backup-----------")
        cmd = 'rm -rf ' + self.backup_path
        self.dbPrimaryUserNode.sh(cmd)
        logger.info("---------------------drop database--------------------")
        result = self.commsh.execut_db_sql(f'drop database {self.dbname};')
        logger.info(result)
        logger.info("-----------Opengauss_Gin_Index_0061 end-----------")
        
        