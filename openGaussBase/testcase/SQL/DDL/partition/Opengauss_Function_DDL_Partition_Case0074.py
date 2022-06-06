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
Case Type   : 基础功能-SQL语法-DDL-partition
Case Name   : 分区表分区1执行事务未提交，分区2执行sql语句执行成功
Description :
    1.建表造数据
    2.线程1 alter 分区p1 启事务 不commmit
    3.线程2 select 分区p2
    4.清理环境
Expect      :
    1.建表造数据成功
    2.线程1不执行commmit
    3.线程1未结束时线程2已执行结束
    4.清理环境
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class DDLCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("==Opengauss_Function_DDL_Partition_Case0074开始执行==")
        self.primary_sh = CommonSH("PrimaryDbUser")
        self.constant = Constant()
        self.com = Common()
        self.user_node = Node("PrimaryDbUser")
        text = "执行前db状态检查"
        self.log.info(text)
        status = self.primary_sh.get_db_cluster_status()
        assert_1 = "Degraded" in status or "Normal" in status
        self.log.info(assert_1)
        self.assertTrue(assert_1, "执行失败:" + text)
        self.t_name = "t_partition_0074"

    def test_ddl_partition(self):
        text = "--step1:建表造数据;expect:建表造数据成功"
        self.log.info(text)
        sql = f'''drop table if exists {self.t_name};
            create table {self.t_name} (a int, b int)
            partition by range(a)
            (
            partition p1 values less than (2000),
            partition p2 values less than (3000),
            partition p3 values less than (4000),
            partition p4 values less than (5000),
            partition p5 values less than (6000)
            );
            insert into {self.t_name} 
            values(1000),(2000),(3000),(4000),(5000);
            insert into {self.t_name} 
            values(generate_series(1,5999));'''
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        assert_2 = "INSERT" in result
        self.log.info(assert_2)
        assert_3 = "CREATE TABLE" in result
        self.log.info(assert_3)
        assert_4 = "ERROR" not in result
        self.log.info(assert_4)
        self.assertTrue(assert_2 and assert_3 and assert_4, "执行失败:" + text)

        text = "--step2:线程1 alter 分区p1 启事务 不commmit;expect:线程1不执行commmit"
        self.log.info(text)
        sql = f"start transaction;" \
              f"alter table {self.t_name} drop partition p1;" \
              f"select pg_sleep(60)"
        session1 = ComThread(self.primary_sh.execut_db_sql,
                             args=(sql,))
        session1.setDaemon(True)
        session1.start()
        time.sleep(1)

        text = "--step3:线程2 select 分区p2;expect:线程1未结束时线程2已执行结束"
        self.log.info(text)
        sql = f"select count(*) from {self.t_name} partition (p2);"
        session2 = ComThread(self.primary_sh.execut_db_sql,
                             args=(sql,))
        session2.setDaemon(True)
        session2.start()

        self.log.info("线程2结果")
        session2.join(30)
        result = session2.get_result()
        self.log.info(result)
        assert_5 = "1001\n" in result
        self.log.info(assert_5)
        self.assertTrue(assert_5, "执行失败:" + text)

        self.log.info("线程1结果")
        session1.join(120)
        result = session1.get_result()
        self.log.info(result)
        assert_6 = "ERROR" not in result
        self.log.info(assert_6)
        self.assertTrue(assert_6, "执行失败:" + text)

    def tearDown(self):
        self.log.info("--step4:恢复环境:expect:恢复环境成功")
        self.log.info("删除表")
        result = self.primary_sh.execut_db_sql(f"drop table "
            f"if exists {self.t_name} cascade;")
        self.log.info(result)

        text = "执行结束db状态核对"
        self.log.info(text)
        status = self.primary_sh.get_db_cluster_status()
        assert_7 = "Degraded" in status or "Normal" in status
        self.log.info(assert_7)
        self.assertTrue(assert_7, "执行失败:" + text)
        self.log.info("==Opengauss_Function_DDL_Partition_Case0074执行结束==")
