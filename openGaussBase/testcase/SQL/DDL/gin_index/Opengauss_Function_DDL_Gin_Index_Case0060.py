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

Case Type： 数据库系统
Case Name： 分区表创建索引后backup备份数据库，进行alter操作后恢复数据库
Case No:    Opengauss_Gin_Index_0060
Descption:  1.create_partition_little.sql创建数据2.创建索引3.dumpall数据4. alter索引名称5.恢复数据6.查询索引7.删除索引8.恢复数据9.查询索引\10.查询
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
TPCC_RES = queue.Queue()


class set_search_limit(unittest.TestCase):

    dbPrimaryUserNode = Node(node='PrimaryDbUser')
    dbPrimaryRootNode = Node(node='PrimaryRoot')
    DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
    DB_ENV_PATH = macro.DB_ENV_PATH
    GSGUC_SUCCESS_MSG = Constant.GSGUC_SUCCESS_MSG
    RESTART_SUCCESS_MSG = Constant.RESTART_SUCCESS_MSG
    commsh = CommonSH('PrimaryDbUser')
    target_path = macro.DB_INSTANCE_PATH + '/testscript'
    sql_path = target_path + '/create_partition_little.sql'
    dump_file_name = 'Opengauss_Gin_Index_0060.tar'
    CREATE_INDEX_SUCCESS_MSG = Constant.CREATE_INDEX_SUCCESS_MSG
    RESTORE_SUCCESS_MSG = Constant.RESTORE_SUCCESS_MSG
    DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
    backup_path = macro.PG_LOG_PATH + '/back'
    ALTER_INDEX_SUCCESS_MSG = Constant.ALTER_INDEX_SUCCESS_MSG
    RESTART_SUCCESS_MSG = Constant.RESTART_SUCCESS_MSG
    DUMPALL_SUCCESS_MSG = Constant.DUMPALL_SUCCESS_MSG
    GSQL_RESTORE_SUCCESS_MSG = Constant.GSQL_RESTORE_SUCCESS_MSG
    DROP_INDEX_SUCCESS_MSG = Constant.DROP_INDEX_SUCCESS_MSG

    def setUp(self):
        logger.info("-----------this is setup-----------")
        logger.info("-----------Opengauss_Gin_Index_0060 start-----------")

    def test_set_search_limit(self):
        
        logger.info('---------------execute create_partition_little.sql---------------------')
        common.scp_file(self.dbPrimaryUserNode, 'create_partition_little.sql', self.target_path)
        sql_bx_cmd = f'''
                        source {macro.DB_ENV_PATH};    
                        gsql -d {self.dbPrimaryUserNode.db_name} -p {self.dbPrimaryUserNode.db_port}  -f {self.sql_path}
                       
                        '''
        logger.info(sql_bx_cmd)
        sql_bx_msg = self.dbPrimaryUserNode.sh(sql_bx_cmd).result()
        logger.info(sql_bx_msg)
        
        logger.info('------------------create index-------------------------')
        sql = 'CREATE INDEX test_gin_student_index_row2 ON test_gin_student_row USING     GIN(to_tsvector(\'english\', data1)) LOCAL         (    PARTITION data2_index_1,    PARTITION data2_index_2,    PARTITION data2_index_3 ) ;'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find(self.CREATE_INDEX_SUCCESS_MSG)>-1)
        
        logger.info('--------------------backup-------------------------')
        cmd = 'mkdir ' + self.backup_path
        logger.info(cmd)
        self.dbPrimaryUserNode.sh(cmd)
        dumpCmd = '''
            source {source_path};
            gs_dumpall -p {port} -f {backup_path}'''.format(source_path = self.DB_ENV_PATH, port = self.dbPrimaryUserNode.db_port , backup_path = self.backup_path+'/dump')
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.DUMPALL_SUCCESS_MSG) > -1)
        
        logger.info('----------------alter index-----------------------')
        sql = 'alter index test_gin_student_index_row2 rename to test_gin_2_first_name;'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find(self.ALTER_INDEX_SUCCESS_MSG)>-1)

        logger.info('--------------------restore database-------------------------')
        dumpCmd = '''
            source {source_path};
            gsql -d {dbname} -p {port} -r -f {backup_path}'''.format(source_path = self.DB_ENV_PATH, dbname = self.dbPrimaryUserNode.db_name ,port = self.dbPrimaryUserNode.db_port , backup_path = self.backup_path+'/dump')
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.CREATE_INDEX_SUCCESS_MSG) > -1)
        
        logger.info('------------------check index-------------------------')
        sql = '\di'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find('test_gin_2_first_name')>-1)
        self.assertTrue(msg.find('test_gin_student_index_row2')>-1)
        
        logger.info('----------------drop index-----------------------')
        sql = 'drop index test_gin_student_index_row2;'
        msg = self.commsh.execut_db_sql(sql)
        self.assertTrue(msg.find(self.DROP_INDEX_SUCCESS_MSG)> -1)
        
        logger.info('--------------------restore database-------------------------')
        dumpCmd = '''
            source {source_path};
            gsql -d {dbname} -p {port} -r -f {backup_path}'''.format(source_path = self.DB_ENV_PATH, dbname = self.dbPrimaryUserNode.db_name ,port = self.dbPrimaryUserNode.db_port , backup_path = self.backup_path+'/dump')
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.CREATE_INDEX_SUCCESS_MSG) > -1)

        logger.info('------------------check index-------------------------')
        sql = '\di'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find('test_gin_2_first_name')>-1)
        self.assertTrue(msg.find('test_gin_student_index_row2')>-1)
        
        logger.info('------------------querry-------------------------')
        sql = "SET ENABLE_SEQSCAN=off;explain SELECT * FROM test_gin_student_row WHERE to_tsvector(\'english\', data1) @@ to_tsquery(\'english\', 'Mexico') ORDER BY num, data1, data2;SELECT * FROM test_gin_student_row WHERE to_tsvector(\'english\', data1) @@ to_tsquery(\'english\', \'Mexico\') ORDER BY num, data1, data2;"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find('13 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('14 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('5001 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('Bitmap Index Scan on test_gin_student_index_row2')>-1)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        logger.info('----------------drop table-----------------------')
        sql = 'drop table test_gin_student_row;'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        logger.info("-----------delete scripts-----------")
        cmd = 'rm -rf ' + self.target_path
        self.dbPrimaryRootNode.sh(cmd)
        logger.info("-----------delete backup-----------")
        cmd = 'rm -rf ' + self.backup_path
        self.dbPrimaryUserNode.sh(cmd)
        logger.info("-----------Opengauss_Gin_Index_0060 end-----------")
        
        