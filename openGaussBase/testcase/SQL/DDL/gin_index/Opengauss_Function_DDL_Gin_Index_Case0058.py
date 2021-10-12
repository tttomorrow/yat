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
Case Name： 普通表创建索引后backup备份数据，进行alter操作后恢复数据库
Case No:    Opengauss_Gin_Index_0058
Descption:1.执行create_column.sql创建数据2.创建索引3.备份数据库4.进行alter等操作5.恢复数据库6.查询索引7.查询

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
    sql_path = target_path + '/create_column.sql'
    dump_file_name = 'Opengauss_Gin_Index_0058.tar'
    CREATE_INDEX_SUCCESS_MSG = Constant.CREATE_INDEX_SUCCESS_MSG
    RESTORE_SUCCESS_MSG = Constant.RESTORE_SUCCESS_MSG
    DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
    backup_path = macro.PG_LOG_PATH + '/back'
    ALTER_INDEX_SUCCESS_MSG = Constant.ALTER_INDEX_SUCCESS_MSG
    RESTART_SUCCESS_MSG = Constant.RESTART_SUCCESS_MSG
    BACKUP_SUCCESS_MSG = Constant.BACKUP_SUCCESS_MSG
    BACKUP_RESTORE_SUCCESS_MSG = Constant.BACKUP_RESTORE_SUCCESS_MSG

    def setUp(self):
        logger.info("-----------this is setup-----------")
        logger.info("-----------Opengauss_Gin_Index_0058 start-----------")

    def test_set_search_limit(self):
        
        logger.info('---------------execute create_column.sql---------------------')
        common.scp_file(self.dbPrimaryUserNode, 'create_column.sql', self.target_path)
        sql_bx_cmd = f'''
                        source {macro.DB_ENV_PATH};    
                        gsql -d {self.dbPrimaryUserNode.db_name} -p {self.dbPrimaryUserNode.db_port}  -f {self.sql_path}
                       
                        '''
        logger.info(sql_bx_cmd)
        sql_bx_msg = self.dbPrimaryUserNode.sh(sql_bx_cmd).result()
        logger.info(sql_bx_msg)
        
        logger.info('------------------create index-------------------------')
        sql = 'CREATE INDEX  test_gin_2_first_name_idx  ON test_gin_2 USING GIN(to_tsvector(\'english\', first_name));'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find(self.CREATE_INDEX_SUCCESS_MSG)>-1)
        
        logger.info('--------------------backup-------------------------')
        cmd = 'mkdir ' + self.backup_path
        logger.info(cmd)
        self.dbPrimaryUserNode.sh(cmd)
        dumpCmd = '''
            source {source_path};
            gs_backup -t backup --backup-dir={backup_path} --all'''.format(source_path = self.DB_ENV_PATH, backup_path = self.backup_path)
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.BACKUP_SUCCESS_MSG) > -1)
        
        logger.info('----------------alter index-----------------------')
        sql = 'alter index test_gin_2_first_name_idx rename to test_gin_2_first_name;'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find(self.ALTER_INDEX_SUCCESS_MSG)>-1)
        
        
        logger.info('--------------------restore database-------------------------')
        dumpCmd = '''
            source {source_path};
            gs_backup -t restore --backup-dir={backup_path} --all'''.format(source_path = self.DB_ENV_PATH, backup_path = self.backup_path)
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        self.assertTrue(dumpMsg.find(self.BACKUP_RESTORE_SUCCESS_MSG) > -1)
        
        logger.info('------------------check index-------------------------')
        sql = '\di'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertFalse(msg.find('test_gin_2_first_name_idx')>-1)
        self.assertTrue(msg.find('test_gin_2_first_name')>-1)
        
        logger.info('------------------querry-------------------------')
        sql = "SET ENABLE_SEQSCAN=off;SELECT * FROM test_gin_2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'Mexico\');explain SELECT * FROM test_gin_2 WHERE to_tsvector(\'english\', first_name) @@ to_tsquery(\'english\', \'Mexico\');"
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        self.assertTrue(msg.find('13 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('14 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexicox')>-1)
        self.assertTrue(msg.find('15 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexicos')>-1)
        self.assertTrue(msg.find('CStore Index Ctid Scan on test_gin_2_first_name')>-1)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        logger.info('----------------drop table-----------------------')
        sql = 'drop table test_gin_2;'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        logger.info("-----------delete scripts-----------")
        cmd = 'rm -rf ' + self.target_path
        self.dbPrimaryRootNode.sh(cmd)
        logger.info("-----------delete backup-----------")
        cmd = 'rm -rf ' + self.backup_path
        self.dbPrimaryUserNode.sh(cmd)
        logger.info("-----------Opengauss_Gin_Index_0058 end-----------")
        
        