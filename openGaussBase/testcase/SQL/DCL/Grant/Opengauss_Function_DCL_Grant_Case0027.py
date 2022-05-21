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
Case Type   : 功能测试
Case Name   : 将表中字段的访问权限赋予指定的用户
Description :
        1.创建普通用户，创建表，插入数据；
        2.查看用户是否有表字段的相关操作权限
        3.将表指定字段的select、insert权限赋予用户；
        4.退出当前数据库，用新建用户连接数据库；
        5.对表被授权字段进行select、insert操作；
        6.对表未被授权字段进行select、insert、drop操作；
        7.清理环境；
Expect      :
        1.创建用户成功，创建表、插入数据成功；
        2.无相关权限；
        3.授权成功；
        4.连接成功；
        5.select、insert操作成功；
        6.select、insert、drop操作失败；
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
        logger.info('--------------Opengauss_Function_DCL_Grant_Case0027.py start-------------------')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_grant(self):
        logger.info('------------------创建普通用户、创建表、插入数据------------------')
        self.user = 'p_user07'
        self.table = 'p_table'
        sql_cmd1 =f'''                    
                    drop user if exists {self.user} cascade;
                    create user {self.user} identified by '{macro.COMMON_PASSWD}';
                    drop table if exists {self.table};
                    create table {self.table}(id int,name varchar(100));
                    insert into {self.table} values(1011,'gauss');
                    '''
        msg1 = self.sh_primary.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, msg1)

        logger.info('-------------------查看用户是否有表字段的相关操作权限-------------------')
        logger.info('---------------将表指定字段的select、insert权限赋予用户-----------------')
        sql_cmd2 = f'''
                    select privilege_type from information_schema.column_privileges where grantee='{self.user}';
                    grant select(id),insert(name) on table {self.table} to {self.user};
                    '''
        msg2 = self.sh_primary.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn('(0 rows)', msg2)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg2)

        logger.info('------------退出当前数据库，用新建用户连接数据库,对表被授权字段进行select、insert操作--------------')
        sql_cmd3 = f'''insert into {self.table}(name) values('boolean');
                       select id from {self.table};'''
        execute_cmd3 = f'''
                     source {self.DB_ENV_PATH}; 
                     gsql -d {self.userNode.db_name} -U {self.user} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd3}"
                    '''
        logger.info(execute_cmd3)
        msg3 = self.userNode.sh(execute_cmd3).result()
        logger.info(msg3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg3)
        self.assertIn('1011', msg3)

        logger.info('------------对表未被授权字段进行select、insert、drop操作,提示权限拒绝--------------')
        sql_cmd4 = f'''insert into {self.table} values(1022,'hello');
                       select * from {self.table};
                       drop table p_table;
                        '''
        execute_cmd4 = f'''
                        source {self.DB_ENV_PATH}; 
                        gsql -d {self.userNode.db_name} -U {self.user} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd4}"
                        '''
        logger.info(execute_cmd4)
        msg4 = self.userNode.sh(execute_cmd4).result()
        logger.info(msg4)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg4)

    def tearDown(self):
        logger.info('--------------清理环境-------------------')
        sql_cmd5 = f'''
                    drop table {self.table} cascade;
                    drop user {self.user} cascade;
                    '''
        msg5 = self.sh_primary.execut_db_sql(sql_cmd5)
        logger.info(msg5)
        logger.info('------------------Opengauss_Function_DCL_Grant_Case0027.py finish------------------')
