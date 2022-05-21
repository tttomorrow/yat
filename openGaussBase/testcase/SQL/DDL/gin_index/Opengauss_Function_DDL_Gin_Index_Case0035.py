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
Case Type   : 功能
Case Name   : 分区表创建索引前dump，创建索引后 恢复数据
Description :
    1.执行create_partition.sql创建数据
    2.dump数据
    3.创建索引
    4.恢复数据
    5.查询索引
    6.查询
Expect      :
    1.创建表并插入数据成功
    2.dump成功
    3.创建索引成功
    4.恢复数据成功
    5.索引存在
    6.正常使用索引且查询结果正确
History     :
"""
import os
import unittest
from yat.test import Node
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
    DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
    DB_ENV_PATH = macro.DB_ENV_PATH
    commsh = CommonSH('PrimaryDbUser')
    target_path = os.path.join(macro.DB_INSTANCE_PATH, 'testscript')
    sql_path = os.path.join(target_path, 'create_partition.sql')
    dump_file_name = 'Opengauss_Gin_Index_0035.tar'

    def setUp(self):
        logger.info("-----------this is setup-----------")
        logger.info("-----------Opengauss_Gin_Index_0035 start-----------")
        self.Constant = Constant()
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        result = self.commsh.get_db_cluster_status('detail')
        logger.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        logger.info(self.node_num)
        for i in range(int(self.node_num) - 1):
            self.comshsta.append(CommonSH(self.nodelist[i]))
        logger.info("-------------------------vacuum-----------------------------")
        result = self.commsh.execut_db_sql('vacuum;')
        logger.info(result)
        self.assertIn('VACUUM', result)
        self.dump_file = os.path.join(macro.DB_INSTANCE_PATH, self.dump_file_name)
        self.dbname = 'dbsys_restore_db'
        logger.info("---------------------create database--------------------")
        result = self.commsh.execut_db_sql(f'drop database if exists {self.dbname};create database {self.dbname};')
        logger.info(result)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, result)

    def test_set_search_limit(self):
        
        logger.info('---------------execute create_partition.sql---------------------')
        common.scp_file(self.dbPrimaryUserNode, 'create_partition.sql', self.target_path)
        sql_bx_cmd = f'''
                        source {macro.DB_ENV_PATH};    
                        gsql -d {self.dbname} -p {self.dbPrimaryUserNode.db_port}  -f {self.sql_path}
                       
                        '''
        logger.info(sql_bx_cmd)
        sql_bx_msg = self.dbPrimaryUserNode.sh(sql_bx_cmd).result()
        logger.info(sql_bx_msg)
        
        logger.info('--------------------dump file-------------------------')
        dumpCmd = '''
            source {source_path};
            gs_dump {dbname} -p {port} -f {file_name} -F t'''.format(source_path = self.DB_ENV_PATH, dbname = self.dbname,port=self.dbPrimaryUserNode.db_port, file_name=self.dump_file)
        logger.info(dumpCmd)
        dumpMsg = self.dbPrimaryUserNode.sh(dumpCmd).result()
        logger.info(dumpMsg)
        flag ='dump database ' + self.dbname +' successfully'
        self.assertIn(flag, dumpMsg)
        
        logger.info('------------------create index-------------------------')
        sql = 'CREATE INDEX test_gin_student_index_row2 ON test_gin_student_row USING     GIN(to_tsvector(\'english\', data1)) LOCAL         (    PARTITION data2_index_1,    PARTITION data2_index_2,    PARTITION data2_index_3 ) ;'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find(self.Constant.CREATE_INDEX_SUCCESS_MSG)>-1)
        
        logger.info('--------------------restore file without -c--------------------------------------------------')
        dumpResult = self.commsh.restore_file(self.dump_file, ' ', self.dbname)
        logger.info(dumpResult)
        self.assertIn(self.Constant.RESTORE_SUCCESS_MSG, dumpResult)
        
        logger.info('------------------check index-------------------------')
        sql = '\di'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find('test_gin_student_index_row2')>-1)
        
        logger.info('------------------querry-------------------------')
        sql = "SET ENABLE_SEQSCAN=off;explain SELECT * FROM test_gin_student_row WHERE to_tsvector(\'english\', data1) @@ to_tsquery(\'english\', 'Mexico') ORDER BY num, data1, data2;SELECT * FROM test_gin_student_row WHERE to_tsvector(\'english\', data1) @@ to_tsquery(\'english\', \'Mexico\') ORDER BY num, data1, data2;"
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        self.assertTrue(msg.find('13 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('14 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('5001 | Mexico, officially the United Mexican States, is a federal republic in the southern part of North America. | Mexico')>-1)
        self.assertTrue(msg.find('Bitmap Index Scan on test_gin_student_index_row2')>-1)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        logger.info("-----------------build standby------------------------")
        for i in range(int(self.node_num) - 1):
            result = self.comshsta[i].execute_gsctl('build', self.Constant.BUILD_SUCCESS_MSG, '-b full')
            logger.info(result)
        logger.info('----------------drop table-----------------------')
        sql = 'drop table test_gin_student_row;'
        msg = self.commsh.execut_db_sql(sql, dbname=self.dbname)
        logger.info(msg)
        logger.info("-----------delete scripts-----------")
        cmd = 'rm -rf ' + self.target_path
        self.dbPrimaryRootNode.sh(cmd)
        logger.info("-----------delete dumpfile-----------")
        cmd = 'rm -rf ' + self.dump_file
        self.dbPrimaryRootNode.sh(cmd)
        logger.info("---------------------drop database--------------------")
        result = self.commsh.execut_db_sql(f'drop database {self.dbname};')
        logger.info(result)
        logger.info("-----------Opengauss_Gin_Index_0035 end-----------")
        
        