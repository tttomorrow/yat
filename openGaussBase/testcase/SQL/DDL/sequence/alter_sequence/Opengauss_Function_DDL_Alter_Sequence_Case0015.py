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
Case Type   : DDL/sequence/alter_sequence
Case Name   : 兼容B数据库中 序列的alter cache
Description :
    1.创建兼容B的数据库
    drop database if exists db_seq015;
    create database td_compatible_db dbcompatibility 'B';
    2.创建序列 执行alter sequence cache
    drop sequence test_seq_015 cascade;
    CREATE sequence test_seq_015 cache 15;
    select last_value,cache_value from test_seq_015;
    select nextval('test_seq_015');
    alter sequence test_seq_015 cache 5;
    select nextval('test_seq_015');
    3.清理环境 删除sequence 删除数据库
    drop sequence test_seq_015 cascade;
    drop database if exists db_seq015;
Expect      :
    1.创建兼容B的数据库成功
    2.创建序列 执行alter sequence cache成功
    3.清理环境 删除sequence 删除数据库
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Sequence(unittest.TestCase):
    def setUp(self):
        LOGGER.info("=Opengauss_Function_DDL_Alter_Sequence_Case0015 start=")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")

    def test_sequence(self):
        LOGGER.info("步骤1：创建兼容B的数据库")
        result = COMMONSH.execut_db_sql("drop database if exists db_seq015;"
            "create database db_seq015 dbcompatibility 'B';")
        LOGGER.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        LOGGER.info("步骤2：创建序列 执行alter sequence cache")
        sql = '''drop sequence test_seq_015 cascade;
                CREATE sequence test_seq_015 cache 15;
                select last_value,cache_value from test_seq_015;
                select nextval('test_seq_015');
                alter sequence test_seq_015 cache 5;
                select nextval('test_seq_015');'''
        LOGGER.info(sql)
        execute_sql = f'''source {macro.DB_ENV_PATH};\
                        gsql \
                        -d db_seq015 \
                        -p {self.user_node.db_port} \
                        -U {self.user_node.ssh_user}  \
                        -c "{sql}"
                        '''
        LOGGER.info(execute_sql)
        result = self.user_node.sh(execute_sql).result()
        LOGGER.info(result)
        self.assertIn("1", result)
        self.assertIn("1\n", result)
        self.assertIn("15\n", result)
        self.assertIn("16\n", result)

        sql = '''select nextval('test_seq_015');\
            alter sequence test_seq_015 cache 10;\
            select nextval('test_seq_015');\
            select last_value,cache_value from test_seq_015;'''
        LOGGER.info(sql)
        execute_sql = f'''source {macro.DB_ENV_PATH};\
                        gsql \
                        -d db_seq015 \
                        -p {self.user_node.db_port} \
                        -U {self.user_node.ssh_user}  \
                        -c "{sql}"
                        '''
        LOGGER.info(execute_sql)
        result = self.user_node.sh(execute_sql).result()
        LOGGER.info(result)
        self.assertIn("35", result)
        self.assertIn("10\n", result)
        self.assertIn("21\n", result)
        self.assertIn("26\n", result)

        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        sql = '''select nextval('test_seq_015');\
            alter sequence test_seq_015 cache 10;\
            select nextval('test_seq_015');\
            select last_value,cache_value from test_seq_015;'''
        LOGGER.info(sql)
        execute_sql = f'''source {macro.DB_ENV_PATH};\
                        gsql \
                        -d db_seq015 \
                        -p {self.user_node.db_port} \
                        -U {self.user_node.ssh_user}  \
                        -c "{sql}"
                        '''
        LOGGER.info(execute_sql)
        result = self.user_node.sh(execute_sql).result()
        LOGGER.info(result)
        self.assertIn("55", result)
        self.assertIn("36\n", result)
        self.assertIn("46\n", result)
        self.assertIn("10\n", result)

    def tearDown(self):
        LOGGER.info("步骤3：清理环境 删除sequence 删除数据库")
        execute_sql = f'''source {macro.DB_ENV_PATH};\
                        gsql \
                        -d db_seq015 \
                        -p {self.user_node.db_port} \
                        -U {self.user_node.ssh_user}  \
                        -c "drop sequence test_seq_015 cascade;"
                        '''
        LOGGER.info(execute_sql)
        result = self.user_node.sh(execute_sql).result()
        LOGGER.info(result)
        result = COMMONSH.execut_db_sql("drop database db_seq015;")
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("=Opengauss_Function_DDL_Alter_Sequence_Case0015 finish=")
