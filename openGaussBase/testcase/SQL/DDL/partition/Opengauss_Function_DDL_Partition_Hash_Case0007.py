"""
Case Type   : hash分区表
Case Name   : 创建普通hash分区表，验证分区个数
Description :
    1、创建普通hash分区表,分区个数小于64
    2、创建普通hash分区表,分区个数等于64
    3、创建普通hash分区表,分区个数大于64
    4、清理环境
Expect      :
    1、创建hash分区表成功
    2、创建hash分区表成功
    3、创建hash分区表失败
    4、清理环境成功
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        logger.info("======检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_partition_hash(self):
        logger.info("==Opengauss_Function_DDL_Partition_Hash_Case0007开始执行==")
        logger.info("=====步骤1：创建普通hash分区表,分区个数小于64======")
        param1 = ',\n'.join([f'''partition p{str(i)}''' for i in range(20)])
        create_cmd1 = f'''drop table if exists partition_hash_tab01;
            create table partition_hash_tab01(p_id int) 
            partition by hash(p_id) ({param1});'''
        logger.info(create_cmd1)
        create_res1 = self.commonsh.execut_db_sql(create_cmd1)
        logger.info(create_res1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, create_res1)

        logger.info("=====步骤2：创建普通hash分区表,分区个数等于64======")
        param2 = ',\n'.join([f'''partition p{str(i)}''' for i in range(64)])
        create_cmd2 = f'''drop table if exists partition_hash_tab02;
            create table partition_hash_tab02(p_id int) 
            partition by hash(p_id) ({param2});'''
        create_res2 = self.commonsh.execut_db_sql(create_cmd2)
        logger.info(create_res2)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, create_res2)

        logger.info("=====步骤3：创建普通hash分区表,分区个数大于64======")
        param3 = ',\n'.join([f'''partition p{str(i)}''' for i in range(100)])
        create_cmd3 = f'''drop table if exists partition_hash_tab03;
                    create table partition_hash_tab03(p_id int) 
                    partition by hash(p_id) ({param3});'''
        create_res3 = self.commonsh.execut_db_sql(create_cmd3)
        logger.info(create_res3)
        self.assertIn('Un-support feature', create_res3)

    def tearDown(self):
        logger.info("======清理环境======")
        clear_cmd = f'''drop table partition_hash_tab01 cascade;
            drop table partition_hash_tab02 cascade;'''
        logger.info(clear_cmd)
        self.commonsh.execut_db_sql(clear_cmd)
        logger.info("==Opengauss_Function_DDL_Partition_Hash_Case0007执行结束==")
