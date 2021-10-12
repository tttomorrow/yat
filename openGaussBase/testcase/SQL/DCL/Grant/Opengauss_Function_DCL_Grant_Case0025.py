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
Case Type   : 功能测试
Case Name   : 将表的访问权限赋予指定的用户,未授权的权限操作不被允许
Description :
        1.创建普通用户，创建表，插入数据；
        2.将表的select、insert权限赋予用户；
        3.退出当前数据库，用新建用户连接数据库；
        4.对表进行select、insert操作；
        5.对表进行update、drop操作；
        6.清理环境；
Expect      :
        1.创建用户成功，创建表、插入数据成功；
        2.授权成功；
        3.连接数据库成功；
        4.select、insert操作成功；
        5.update、drop操作失败；
        6.清理环境成功；
History     :
"""


import sys
import unittest
from yat.test import Node
from yat.test import macro
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()

class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_DCL_Grant_Case0025.py start-------------------')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_server_tools(self):
        logger.info('------------------创建普通用户、创建表、插入数据------------------')
        logger.info('------------------将表的select、insert权限赋予用户------------------')
        self.user = 'p_user05'
        self.table = 'p_table'
        sql_cmd1 =f'''                    
                    drop user if exists {self.user} cascade;
                    create user {self.user} identified by '{macro.COMMON_PASSWD}';
                    drop table if exists {self.table};
                    create table {self.table}(id int,name varchar(100));
                    insert into {self.table} values(1011,'gauss');
                    grant select on table {self.table} to {self.user};
                    grant insert on table {self.table} to {self.user};
                    '''
        msg1 = self.sh_primary.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, msg1)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg1)

        logger.info('------------退出当前数据库，用新建用户连接数据库,对表进行select、insert操作--------------')
        sql_cmd2 = f'''insert into p_table values(1021,'boolean');
                       select * from p_table;'''
        execute_cmd2 = f'''
                     source {self.DB_ENV_PATH}; 
                     gsql -d {self.userNode.db_name} -U {self.user} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd2}"
                    '''
        logger.info(execute_cmd2)
        msg2 = self.userNode.sh(execute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg2)
        self.assertIn('boolean', msg2)

        logger.info('----------------------对表进行update和drop操作，无权限----------------------')
        sql_cmd3 = f'''update {self.table} set name = 'gauss_2' where id = 1011;
                       drop table p_table;'''
        execute_cmd3 = f'''
                    source {self.DB_ENV_PATH}; 
                    gsql -d {self.userNode.db_name} -U {self.user} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd3}"
                    '''
        logger.info(execute_cmd3)
        msg3 = self.userNode.sh(execute_cmd3).result()
        logger.info(msg3)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg3)

    def tearDown(self):
        logger.info('--------------清理环境-------------------')
        sql_cmd4 = f'''
                    drop table {self.table} cascade;
                    drop user {self.user} cascade;
                    '''
        msg4 = self.sh_primary.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        logger.info('------------------Opengauss_Function_DCL_Grant_Case0025.py finish------------------')
