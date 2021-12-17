"""
Case Type   : hash分区表
Case Name   : 未赋权用户对hash分区表执行alter操作
Description :
    1、初始用户创建两个用户，part_user1和part_user2
    2、创建普通hash分区表
    3、将hash分区表的alter权限赋予part_user1
    4、连接part_user1，对分区表进行alter操作
    5、连接part_user2，对分区表进行alter操作
    5、清理环境
Expect      :
    1、创建用户成功
    2、创建hash分区表成功
    3、赋权成功
    4、part_user1下可以执行alter操作
    5、part_user2下无权限执行alter操作
    6、清理环境成功
History     :
"""

import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.user1 = 'part_user1'
        self.user2 = 'part_user2'
        self.table = 'partition_hash_tab'
        logger.info("======检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_partition_hash(self):
        logger.info("==Opengauss_Function_DDL_Partition_Hash_Case0015开始执行==")
        logger.info("=====步骤1：创建两个用户，part_user1和part_user2======")
        creat_cmd = f"""drop user if exists {self.user1} cascade;
            drop user if exists {self.user2} cascade;
            create user {self.user1} password '{macro.COMMON_PASSWD}';
            create user {self.user2} password '{macro.COMMON_PASSWD}';
            """
        logger.info(creat_cmd)
        creat_res = self.commonsh.execut_db_sql(creat_cmd)
        logger.info(creat_res)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, creat_res)

        logger.info("====步骤2&3：创建hash分区表，并将hash分区表的insert权限赋予part_user1====")
        grant_cmd = f'''drop table if exists {self.table} cascade;
            create table {self.table}(p_id int,p_name varchar,p_age int) 
            partition by hash(p_id)
            (partition p1,
             partition p2,
             partition p3);
            grant insert on table {self.table} to {self.user1};
            '''
        logger.info(grant_cmd)
        grant_res = self.commonsh.execut_db_sql(grant_cmd)
        logger.info(grant_res)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, grant_res)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, grant_res)

        logger.info("======连接part_user1，对分区表进行insert操作，可执行======")
        sql_cmd = f'''insert into {self.table} values(40);'''
        conn_cmd1 = f'''source {macro.DB_ENV_PATH}; \
            gsql -d {self.user_node.db_name} \
            -U {self.user1} \
            -W {macro.COMMON_PASSWD} \
            -p {self.user_node.db_port} \
            -c "{sql_cmd}"'''
        logger.info(conn_cmd1)
        conn_res1 = self.user_node.sh(conn_cmd1).result()
        logger.info(conn_res1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, conn_res1)

        logger.info("======连接part_user2，对分区表进行insert操作，无权限======")
        conn_cmd2 = f'''source {macro.DB_ENV_PATH}; \
            gsql -d {self.user_node.db_name} \
            -U {self.user2} \
            -W {macro.COMMON_PASSWD} \
            -p {self.user_node.db_port} \
            -c "{sql_cmd}"'''
        logger.info(conn_cmd2)
        conn_res2 = self.user_node.sh(conn_cmd2).result()
        logger.info(conn_res2)
        self.assertIn(self.constant.PERMISSION_DENIED, conn_res2)

    def tearDown(self):
        logger.info("======清理环境======")
        clear_cmd = f'''drop table {self.table} cascade;
            drop user {self.user1} cascade;
            drop user {self.user2} cascade;
            '''
        logger.info(clear_cmd)
        self.commonsh.execut_db_sql(clear_cmd)
        logger.info("==Opengauss_Function_DDL_Partition_Hash_Case0015执行结束==")
