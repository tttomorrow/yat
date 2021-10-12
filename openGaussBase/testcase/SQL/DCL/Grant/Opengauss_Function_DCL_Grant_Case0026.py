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
Case Name   : 声明with grant option,将表的访问权限赋予指定的用户,被授权用户可将相应权限赋予其他用户
Description :
        1.创建2个普通用户，创建表，插入数据；
        2.查看用户1和用户2是否有表的相关操作权限
        3.将表的select、insert权限赋予用户1且声明with grant option；
        4.将用户1的权限再次赋予用户2
        5.退出当前数据库，用新建用户2连接数据库；
        6.对表进行select、insert操作；
        7.清理环境；
Expect      :
        1.创建用户成功，创建表、插入数据成功；
        2.无相关权限；
        3.授权成功；
        4.再次赋权成功；
        5.连接成功；
        6.select、insert操作成功；
        7.清理环境成功；
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

class Grant(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_DCL_Grant_Case0026.py start-------------------')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_grant(self):
        logger.info('------------------创建2个普通用户、创建表、插入数据------------------')
        self.user1 = 'p_user06_1'
        self.user2 = 'p_user06_2'
        self.table = 'p_table'
        sql_cmd1 =f'''                    
                    drop user if exists {self.user1} cascade;
                    drop user if exists {self.user2} cascade;
                    create user {self.user1} identified by '{macro.COMMON_PASSWD}';
                    create user {self.user2} identified by '{macro.COMMON_PASSWD}';
                    drop table if exists {self.table};
                    create table {self.table}(id int,name varchar(100));
                    insert into {self.table} values(1011,'gauss');
                    '''
        msg1 = self.sh_primary.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, msg1)

        logger.info('-------------------查看用户1和用户2是否有表的操作权限-------------------')
        logger.info('---------------将表的select、insert权限赋予用户1且声明with grant option---------------')
        logger.info('---------------------将用户1的权限再次赋予用户2-----------------------')
        sql_cmd2 = f'''
                    --步骤1
                    select privilege_type from information_schema.table_privileges where grantee = '{self.user1}';
                    select privilege_type from information_schema.table_privileges where grantee = '{self.user2}';
                    --步骤2
                    grant select on table {self.table} to {self.user1} with grant option;
                    grant insert on table {self.table} to {self.user1} with grant option;
                    --步骤3
                    grant {self.user1} to {self.user2};
                    '''
        msg2 = self.sh_primary.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn('(0 rows)', msg2)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg2)

        logger.info('------------退出当前数据库，用新建用户2连接数据库,对表进行select、insert操作--------------')
        sql_cmd3 = f'''insert into {self.table} values(1021,'boolean');
                       select * from {self.table};'''
        execute_cmd3 = f'''
                     source {self.DB_ENV_PATH}; 
                     gsql -d {self.userNode.db_name} -U {self.user2} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd3}"
                    '''
        logger.info(execute_cmd3)
        msg3 = self.userNode.sh(execute_cmd3).result()
        logger.info(msg3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg3)
        self.assertIn('boolean', msg3)


    def tearDown(self):
        logger.info('--------------清理环境-------------------')
        sql_cmd4 = f'''
                    drop table {self.table} cascade;
                    drop user {self.user1} cascade;
                    drop user {self.user2} cascade;
                    '''
        msg4 = self.sh_primary.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        logger.info('------------------Opengauss_Function_DCL_Grant_Case0026.py finish------------------')
