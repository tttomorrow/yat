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

'''

Case Type： DDL
Case Name： 在同一列上创建部分索引 和普通索引，再进行部分索引设置范围内的查询
Case No:    Opengauss_Gin_Index_0018
Descption:  

history：
'''
import os
import unittest
from yat.test import Node
import time
import _thread
import queue
from yat.test import macro
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
logger = Logger()
common = Common()


class createGinIndex(unittest.TestCase):

    dbPrimaryUserNode = Node(node='PrimaryDbUser')
    dbPrimaryRootNode = Node(node='PrimaryRoot')
    DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
    DB_ENV_PATH = macro.DB_ENV_PATH
    commsh = CommonSH('PrimaryDbUser')
    DROP_INDEX_SUCCESS_MSG = Constant.DROP_INDEX_SUCCESS_MSG
    target_path = macro.DB_INSTANCE_PATH + '/testscript'
    sql_path = target_path + '/Opengauss_Gin_Index_0018.sql'

    def setUp(self):
        logger.info("-----------this is setup-----------")
        logger.info("-----------Opengauss_Gin_Index_0018 start-----------")

    def test_create_gin_index(self):
     
        query_result1 = "2 | America is a rock band, formed in England in 1970 by multi-instrumentalists Dewey Bunnell, Dan Peek, and Gerry Beckley. | America"
        query_result2 = "5001 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico"
        explain_result1 = "Bitmap Heap Scan on test_gin_row2"
        explain_result2 = "Bitmap Index Scan on test_gin_row2_first_name_idx2"
        explain_result3 = "Index Cond: (to_tsvector('english'::regconfig, first_name) @@ '''form'''::tsquery)"
        explain_result4 = "Bitmap Index Scan on test_gin_row2_first_name_idx"
        explain_result5 = "Index Cond: (to_tsvector('english'::regconfig, first_name) @@ '''mexico'''::tsquery"
        explain_result6 = "Index Cond: (to_tsvector('english'::regconfig, first_name) @@ '''mexico'''::tsquery)"
        
        logger.info('---------------create table---------------------')
        common.scp_file(self.dbPrimaryUserNode, 'Opengauss_Gin_Index_0018.sql', self.target_path)
        sql_bx_cmd = f'''
                        source {macro.DB_ENV_PATH};    
                        gsql -d {self.dbPrimaryUserNode.db_name} -p {self.dbPrimaryUserNode.db_port}  -f {self.sql_path}
                        '''
        logger.info(sql_bx_cmd)
        sql_bx_msg = self.dbPrimaryUserNode.sh(sql_bx_cmd).result()
        logger.info(sql_bx_msg)
        
        logger.info('------------------query -------------------------')
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;SELECT * FROM test_gin_row2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'formed\');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(query_result1,msg)
        
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;explain SELECT * FROM test_gin_row2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'formed\');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(explain_result1,msg)
        self.assertIn(explain_result2,msg)
        self.assertIn(explain_result3,msg)
        
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(query_result2,msg)
        
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(explain_result1,msg)
        self.assertIn(explain_result4,msg)
        self.assertIn(explain_result5,msg)
        
        logger.info('------------------query ENABLE_SEQSCAN=on-------------------------')
        sql = "SET ENABLE_SEQSCAN=on;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'formed');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(query_result1,msg)
        
        sql = "SET ENABLE_SEQSCAN=on;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'formed');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(explain_result1,msg)
        self.assertIn(explain_result2,msg)
        self.assertIn(explain_result3,msg)
        
        sql = "SET ENABLE_SEQSCAN=on;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(query_result2,msg)
        
        sql = "SET ENABLE_SEQSCAN=on;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(explain_result1,msg)
        self.assertIn(explain_result4,msg)
        self.assertIn(explain_result6,msg)
        
        logger.info('---------------drop index---------------------')
        sql = "drop index test_gin_row2_first_name_idx;"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(self.DROP_INDEX_SUCCESS_MSG,msg)
        
        logger.info('------------------query -------------------------')
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;SELECT * FROM test_gin_row2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'formed\');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(query_result1,msg)
        
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;explain SELECT * FROM test_gin_row2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'formed\');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(explain_result1,msg)
        self.assertIn(explain_result2,msg)
        
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertIn(query_result2,msg)
        
        sql = "SET ENABLE_SEQSCAN=off;RESET ENABLE_INDEXSCAN;RESET ENABLE_BITMAPSCAN;explain SELECT * FROM test_gin_row2 WHERE to_tsvector('english', first_name) @@ to_tsquery('english', 'Mexico');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertFalse(msg.find('test_gin_row2_first_name_idx')>-1)


    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        logger.info('----------------drop table-----------------------')
        sql = 'DROP TABLE IF EXISTS test_gin_row2;'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        
        logger.info("-----------delete scripts-----------")
        cmd = 'rm -rf ' + self.target_path
        self.dbPrimaryRootNode.sh(cmd)