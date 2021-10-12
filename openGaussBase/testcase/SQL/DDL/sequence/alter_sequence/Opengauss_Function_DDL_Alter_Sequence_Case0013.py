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
Case Type   : DDL/sequence/alter_sequence
Case Name   : 序列alter cache权限测试
Description :
    1.sysadmin用户创建序列
    drop sequence if exists test_seq_013;
    CREATE sequence test_seq_013;
    select last_value,cache_value from test_seq_013;
    select nextval('test_seq_013');
    2.sysadmin用户alter cache
    alter sequence test_seq_013 cache 5;
    3.重启会话查询cache_value和last_value
    select last_value,cache_value from test_seq_013;
    select nextval('test_seq_013');
    4.初始用户alter cache
    alter sequence test_seq_013 cache 10;
    5.重启数据库后查询cache_value和last_value
    gs_om -t restart
    select last_value,cache_value from test_seq_013;
    select nextval('test_seq_013');
    6.创建测试用户user_seq_013
    drop user if exists user_seq_013;
    create user user_seq_013 pasword "";
    7.user_seq_013用户alter cache
    alter sequence test_seq_013 cache 15;
    8.sysadmin用户给user_seq_013用户赋序列的alter权限
    grant alter on sequence test_seq_013 to user_seq_013;
    9.user_seq_013用户alter cache
    alter sequence test_seq_013 cache 15;
    10.同一会话 修改最大值后查询cache_value和last_value
    alter sequence test_seq_010 maxvalue 100;
    select last_value,cache_value from test_seq_013;
    select nextval('test_seq_013');
    11.清理环境
    drop sequence test_seq_013 cascade;
    drop owned by user_seq_013 cascade;
    drop user user_seq_013;
Expect      :
    1.创建序列成功
    2.alter 成功
    3.查询cache被清空重来
    4.alter 成功
    5.查询cache被清空重来
    6.创建测试用户成功
    7.alter 失败 报错无权限
    8.赋权成功
    9.alter 成功
    10.修改最大值成功 查询cache被清空重来
    11.清理环境
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
        LOGGER.info("=Opengauss_Function_DDL_Alter_Sequence_Case0013 start=")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.user_node = Node("PrimaryDbUser")

    def test_sequence(self):
        LOGGER.info("步骤1：sysadmin用户创建序列")
        result = COMMONSH.execut_db_sql("drop sequence if exists "
            "test_seq_013;"
            "CREATE sequence test_seq_013;"
            "select nextval('test_seq_013');"
            "select last_value,cache_value from test_seq_013;")
        LOGGER.info(result)
        self.assertIn("1\n", result)
        self.assertIn("CREATE SEQUENCE", result)

        LOGGER.info("步骤2：sysadmin用户alter cache")
        result = COMMONSH.execut_db_sql("alter sequence test_seq_013 cache 5")
        LOGGER.info(result)
        self.assertIn("ALTER SEQUENCE", result)

        LOGGER.info("步骤3：重启会话查询cache_value和last_value")
        result = COMMONSH.execut_db_sql("select last_value,cache_value "
            "from test_seq_013;select nextval('test_seq_013');")
        LOGGER.info(result)
        self.assertIn("1", result)
        self.assertIn("5\n", result)
        self.assertIn("2\n", result)

        LOGGER.info("步骤4：sysadmin用户alter cache")
        sql = "alter sequence test_seq_013 cache 10"
        LOGGER.info(sql)
        execute_sql = f'''source {macro.DB_ENV_PATH};\
                        gsql \
                        -d {self.user_node.db_name} \
                        -p {self.user_node.db_port} \
                        -U {self.user_node.ssh_user}  \
                        -c "{sql}"
                        '''
        LOGGER.info(execute_sql)
        result = self.user_node.sh(execute_sql).result()
        LOGGER.info(result)
        self.assertIn("ALTER SEQUENCE", result)

        LOGGER.info("步骤5：重启数据库查询cache_value和last_value")
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        result = COMMONSH.execut_db_sql("select last_value,cache_value "
            "from test_seq_013;select nextval('test_seq_013');")
        LOGGER.info(result)
        self.assertIn("6", result)
        self.assertIn("10\n", result)
        self.assertIn("7\n", result)

        LOGGER.info("步骤6：创建测试用户user_seq_013")
        result = COMMONSH.execut_db_sql(f'''drop user if exists user_seq_013;\
            create user user_seq_013 password \\"{macro.COMMON_PASSWD}\\";''')
        LOGGER.info(result)
        self.assertIn("CREATE ROLE", result)

        LOGGER.info("步骤7：user_seq_013用户alter cache")
        sql = "alter sequence test_seq_013 cache 15"
        LOGGER.info(sql)
        execute_sql = f'''source {macro.DB_ENV_PATH};\
                        gsql \
                        -d {self.user_node.db_name} \
                        -p {self.user_node.db_port} \
                        -U user_seq_013 \
                        -W {macro.COMMON_PASSWD}\
                        -c "{sql}"
                        '''
        LOGGER.info(execute_sql)
        result = self.user_node.sh(execute_sql).result()
        LOGGER.info(result)
        self.assertNotIn("ALTER SEQUENCE", result)
        self.assertIn(self.constant.PERMISSION_DENIED, result)

        LOGGER.info("步骤8：sysadmin用户给user_seq_013用户赋序列的alter权限")
        result = COMMONSH.execut_db_sql("grant alter on sequence "
                                        "test_seq_013 to user_seq_013;")
        LOGGER.info(result)
        self.assertIn("GRANT", result)

        LOGGER.info("步骤9：user_seq_013用户alter cache")
        sql = "alter sequence test_seq_013 cache 15"
        LOGGER.info(sql)
        execute_sql = f'''source {macro.DB_ENV_PATH};\
                        gsql \
                        -d {self.user_node.db_name} \
                        -p {self.user_node.db_port} \
                        -U user_seq_013 \
                        -W {macro.COMMON_PASSWD}\
                        -c "{sql}"
                        '''
        LOGGER.info(execute_sql)
        result = self.user_node.sh(execute_sql).result()
        LOGGER.info(result)
        self.assertIn("ALTER SEQUENCE", result)
        self.assertNotIn(self.constant.PERMISSION_DENY_MSG, result)

        LOGGER.info("步骤10：修改最大值后查询cache_value和last_value")

        result = COMMONSH.execut_db_sql("alter sequence test_seq_010 "
            "maxvalue 100;"
            "select last_value,cache_value "
            "from test_seq_013;select nextval('test_seq_013');")
        LOGGER.info(result)
        self.assertIn("16", result)
        self.assertIn("15\n", result)
        self.assertIn("17\n", result)

    def tearDown(self):
        LOGGER.info("步骤11：清理环境")
        result = COMMONSH.execut_db_sql("drop sequence test_seq_013 cascade;"
                                        "drop owned by user_seq_013 cascade;"
                                        "drop user if exists user_seq_013;")
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.assertTrue("DROP ROLE" in result and "DROP SEQUENCE" in result)
        LOGGER.info("=Opengauss_Function_DDL_Alter_Sequence_Case0013 finish=")
