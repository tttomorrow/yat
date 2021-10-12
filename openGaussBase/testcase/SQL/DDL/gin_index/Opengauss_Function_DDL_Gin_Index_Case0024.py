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
Case Name   : 设置gin_fuzzy_search_limit为正常范围
Description :
    1.设置gin_fuzzy_search_limit=2
    2.重启数据库
    3.创建gin索引并查询
Expect      :
    1.设置guc参数成功
    2.重启数据库成功
    3.查询显示行数小于80（软上限）
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
    sql_path = os.path.join(target_path, 'Opengauss_Gin_Index_0024.sql')

    def setUp(self):
        logger.info("-----------this is setup-----------")
        self.Constant = Constant()
        logger.info("-----------Opengauss_Gin_Index_0024 start-----------")

    def test_set_search_limit(self):
        logger.info("-----------gin_fuzzy_search_limit=2-----------")
        self.commsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'gin_fuzzy_search_limit=2')

        logger.info("-----------restart opengauss -----------")
        result = self.commsh.stop_db_cluster()
        self.assertTrue(result)
        result = self.commsh.start_db_cluster()
        logger.info(result)
        time.sleep(10)

        status = self.commsh.check_connection_status(self.Constant.START_STATUS_MSG)
        if not status:
            logger.info(f'--------------------waiting for openGauss recovery----------------')
            time.sleep(20)
            for i in range(30):
                status = self.commsh.check_connection_status(self.Constant.START_STATUS_MSG)
                if status:
                    break

        logger.info('---------------execute Opengauss_Gin_Index_0024.sql---------------------')
        common.scp_file(self.dbPrimaryUserNode, 'Opengauss_Gin_Index_0024.sql', self.target_path)
        sql_bx_cmd = f'''
                        source {macro.DB_ENV_PATH};    
                        gsql -d {self.dbPrimaryUserNode.db_name} -p {self.dbPrimaryUserNode.db_port}  -f {self.sql_path}
                       
                        '''
        logger.info(sql_bx_cmd)
        sql_bx_msg = self.dbPrimaryUserNode.sh(sql_bx_cmd).result()
        logger.info(sql_bx_msg)
        self.assertTrue(sql_bx_msg.find(self.Constant.TABLE_CREATE_SUCCESS)>-1)
        self.assertTrue(sql_bx_msg.find("INSERT 0 200000")>-1)
        
        logger.info('---------------query---------------------')
        for i in range(1,3):
            sql = 'SET ENABLE_SEQSCAN=off;SELECT * FROM test_gin_student_column WHERE to_tsvector(\'english\', data1) @@ to_tsquery(\'english\', \'China\');'
            msg = self.commsh.execut_db_sql(sql)
            logger.info(msg)
            msgtmp = msg.split('\n')
            if len(msgtmp) > 2:
                rownum = msgtmp[len(msgtmp)-1].split(' ')[0].split('(')[1]
                logger.info(rownum)
                self.assertTrue(int(rownum)<70)
            else:
                self.assertTrue(False)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        logger.info("-----------reset gin_fuzzy_search_limit-----------")
        self.commsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'gin_fuzzy_search_limit=0')
        logger.info("-----------restart opengauss -----------")
        result = self.commsh.stop_db_cluster()
        logger.info(result)
        result = self.commsh.start_db_cluster()
        logger.info(result)
        time.sleep(5)
        logger.info("-----------delete scripts-----------")
        cmd = 'rm -rf ' + self.target_path
        self.dbPrimaryRootNode.sh(cmd)
        
        logger.info('----------------drop table-----------------------')
        sql = 'drop table test_gin_student_column;'
        msg = self.commsh.execut_db_sql(sql)
        logger.info(msg)
        logger.info("-----------Opengauss_Gin_Index_0024 end-----------")
        