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
Case Name   : 使用无权限用户权限登录进行alter index操作
Description :
    1.创建用户testindex_150赋管理员权限，使用testindex_150登录创建表空间，创建表，创建索引，创建用户testindex_151不赋权
    2.使用无权限用户权限登录进行alter index操作
    3.清理环境
Expect      :
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Index_Case0150开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        # 创建无权限用户用户
        sql_cmd1 = commonsh.execut_db_sql(f'''
                                        drop user if exists testindex_150;
                                        create user testindex_150 password '{macro.COMMON_PASSWD}';
                                        grant all privileges to testindex_150;
                                        drop user if exists testindex_151;
                                        create user testindex_151 password '{macro.COMMON_PASSWD}';
                                        ''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)

        # 创建表空间
        sql_cmd2 = ('''drop tablespace if exists test_space_150_01;
        CREATE TABLESPACE test_space_150_01 RELATIVE LOCATION 'tablespace/tablespace_1';''')
        excute_cmd2 = f'''
                             source {self.DB_ENV_PATH};
                             gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_150 -W {macro.COMMON_PASSWD} -c "{sql_cmd2}"
                             '''
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.TABLESPCE_CREATE_SUCCESS, sql_cmd2)

        # 创建表和索引
        sql_cmd3 = ('''drop schema if exists test_index;
        create schema test_index;
        DROP TABLE if EXISTS test_index.test_index_table_150 CASCADE;
        create table test_index.test_index_table_150(
        c_int int,
        c_date date
        ) WITH (ORIENTATION = row) partition by range(c_date)(
        partition p1 values less than ('1990-01-01 00:00:00'),
        partition p2 values less than ('2020-01-01 00:00:00')
        );drop index if exists index_150_01;
        drop index if exists index_150_01;
        create index test_index.index_150_01 on test_index.test_index_table_150(c_date) local (PARTITION p1 ,PARTITION p2);
        select relname from pg_class where relname like 'index_150_%' order by relname;''')
        excute_cmd3 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_150 -W {macro.COMMON_PASSWD} -c "{sql_cmd3}"
                            '''
        logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        logger.info(msg3)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, msg3)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, msg3)
        self.assertIn(self.Constant.CREATE_SCHEMA_SUCCESS_MSG, msg3)

        # 无权限用户执行alter语句--RENAME TO
        sql_cmd4 = ('''ALTER index  index_150_01 RENAME TO a;
                     ALTER index  a RENAME TO index_150_01;''')
        excute_cmd4 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_151 -W {macro.COMMON_PASSWD} -c "{sql_cmd4}"
                            '''
        logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        logger.info(msg4)
        self.assertIn(self.Constant.NOT_EXIST, msg4)

        # 无权限用户执行alter语句--FILLFACTOR
        sql_cmd5 = ('''alter index index_150_01 set (fillfactor=50);''')
        excute_cmd5 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_151 -W {macro.COMMON_PASSWD} -c "{sql_cmd5}"
                            '''
        logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        logger.info(msg5)
        self.assertIn(self.Constant.NOT_EXIST, msg5)

        # 无权限用户执行alter语句--reset
        sql_cmd6 = ('''alter index index_150_01 reset (fillfactor);''')
        excute_cmd6 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_151 -W {macro.COMMON_PASSWD} -c "{sql_cmd6}"
                            '''
        logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        logger.info(msg6)
        self.assertIn(self.Constant.NOT_EXIST, msg6)

        # 无权限用户执行alter语句--UNUSABLE
        sql_cmd7 = ('''ALTER INDEX  index_150_01 UNUSABLE;
explain select * from test_index_table_150 where c_date > '1990-01-01' order by c_date desc ;''')
        excute_cmd7 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_151 -W {macro.COMMON_PASSWD} -c "{sql_cmd7}"
                            '''
        logger.info(excute_cmd7)
        msg7 = self.userNode.sh(excute_cmd7).result()
        logger.info(msg7)
        self.assertIn(self.Constant.NOT_EXIST, msg7)

        # 无权限用户执行alter语句--rebuild
        sql_cmd8 = ('''ALTER INDEX index_150_01 REBUILD;
explain select * from test_index_table_150 where c_date > '1990-01-01' order by c_date desc ;''')
        excute_cmd8 = f'''
                                source {self.DB_ENV_PATH};
                                gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_151 -W {macro.COMMON_PASSWD} -c "{sql_cmd8}"
                                '''
        logger.info(excute_cmd8)
        msg8 = self.userNode.sh(excute_cmd8).result()
        logger.info(msg8)
        self.assertIn(self.Constant.NOT_EXIST, msg8)

        # 无权限用户执行alter语句--RENAME PARTITION
        sql_cmd9 = ('''ALTER INDEX if exists index_150_01 RENAME PARTITION p1 TO p5;
select relname from PG_PARTITION where parentid=(select relfilenode from pg_class where relname='index_150_01') order by relname asc;
ALTER INDEX if exists index_150_01 RENAME PARTITION p5 TO p1;''')
        excute_cmd9 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_151 -W {macro.COMMON_PASSWD} -c "{sql_cmd9}"
                                    '''
        logger.info(excute_cmd9)
        msg9 = self.userNode.sh(excute_cmd9).result()
        logger.info(msg9)
        self.assertIn(self.Constant.NOT_EXIST, msg9)
        self.assertNotIn('p5', msg9)

        # 无权限用户执行alter语句--MOVE PARTITION
        sql_cmd10 = ('''ALTER INDEX index_150_01 MOVE PARTITION p2 TABLESPACE test_space_150_01;
select spcname from PG_TABLESPACE where oid in
(select distinct reltablespace from PG_PARTITION where parentid=
(select relfilenode from pg_class where relname='index_150_01'));''')
        excute_cmd10 = f'''
                                        source {self.DB_ENV_PATH};
                                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U testindex_151 -W {macro.COMMON_PASSWD} -c "{sql_cmd10}"
                                        '''
        logger.info(excute_cmd10)
        msg10 = self.userNode.sh(excute_cmd10).result()
        logger.info(msg10)
        self.assertIn(self.Constant.NOT_EXIST, msg10)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd11 = commonsh.execut_db_sql('''DROP TABLE if EXISTS test_index_table_150 CASCADE;''')
        logger.info(sql_cmd11)

        # 删除表空间
        sql_cmd12 = commonsh.execut_db_sql('''drop tablespace if exists test_space_150_01;''')
        logger.info(sql_cmd12)

        # 删除用户
        sql_cmd13 = commonsh.execut_db_sql('''drop user testindex_150 cascade;drop user testindex_151 cascade;''')
        logger.info(sql_cmd13)
        logger.info('------------------------Opengauss_Function_DDL_Index_Case0150执行结束--------------------------')