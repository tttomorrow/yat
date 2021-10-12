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
Case Type   : 基础功能-SQL语法-DDL-partition
Case Name   : 取消分区表中分区对应的物理文件的读写权限后，向分区插入数据 合理报错
Description :
    1.建表造数据
    2.查询表文件并取消其读写权限
    3.向该分区插入数据
    4.查看有无core文件生成
    5.恢复其读写权限 清理环境
Expect      :
    1.建表造数据成功
    2.查询表文件并取消其读写权限成功
    3.向该分区插入数据失败 报错无权限
    4.查看无core文件生成
    5.恢复其读写权限 清理环境
History     :
"""

import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node, macro


class DDLCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("==Opengauss_Function_DDL_Partition_Case0071开始执行==")
        self.primary_sh = CommonSH("PrimaryDbUser")
        self.constant = Constant()
        self.com = Common()
        self.user_node = Node("PrimaryDbUser")
        text = "执行前db状态检查"
        self.log.info(text)
        status = self.primary_sh.get_db_cluster_status()
        assert_1 = "Degraded" in status or "Normal" in status
        self.assertTrue(assert_1, "执行失败:" + text)
        self.t_name = "t_partition_0071"

    def test_ddl_partition(self):
        text = "--step1:建表造数据;expect:建表造数据成功"
        self.log.info(text)
        sql = f'''drop table if exists {self.t_name};
            create table {self.t_name}(
            col_1 smallint,
            col_2 char(30),
            col_3 int,
            col_4 date,
            col_5 boolean,
            col_6 nchar(30),
            col_7 float)
            partition by range (col_4)
            interval ('1 month')
            (partition t_partition_0071_p1
            values less than ('2020-03-01'),
            partition t_partition_0071_p2
            values less than ('2020-04-01'),
            partition t_partition_0071_p3
            values less than ('2020-05-01'));
            insert into {self.t_name} 
            values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);'''
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        assert_2 = "INSERT" in result
        self.log.info(assert_2)
        assert_3 = "CREATE TABLE" in result
        self.log.info(assert_3)
        assert_4 = "ERROR" not in result
        self.log.info(assert_4)
        self.assertTrue(assert_2 and assert_3 and assert_4, "执行失败:" + text)

        text = "--step2:查询表文件并取消其读写权限;expect:取消其读写权限成功"
        self.log.info(text)
        sql = f"select relfilenode from pg_partition " \
              f"where parentid = (select oid from pg_class " \
              f"where relname = '{self.t_name}') " \
              f"and relname = 'sys_p1'order by relname;"
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        assert_5 = "ERROR" not in result
        self.log.info(assert_5)
        self.assertTrue(assert_5, "执行失败:" + text)

        text = "查找文件"
        self.log.info(text)
        table_oid = result.splitlines()[-2].strip()
        self.log.info(table_oid)
        cmd = f"find {macro.DB_INSTANCE_PATH} -name {table_oid}"
        result = self.com.get_sh_result(self.user_node, cmd)
        self.log.info(result)
        assert_6 = "bash" not in result
        self.log.info(assert_6)
        self.assertTrue(assert_6, "执行失败:" + text)
        self.file_name = result
        self.log.info(self.file_name)

        text = "取消读写权限"
        self.log.info(text)
        cmd = f"chmod -rw {self.file_name};ls -l {self.file_name}"
        result = self.com.get_sh_result(self.user_node, cmd)
        self.log.info(result)
        assert_7 = "bash" not in result
        self.log.info(assert_7)
        assert_8 = "----------" in result
        self.log.info(assert_8)
        self.assertTrue(assert_7 and assert_8, "执行失败:" + text)

        text = "查看无core文件数量"
        self.log.info(text)
        cmd = f'''ls -l {macro.DB_CORE_PATH} |grep "^-"| wc -l'''
        result = self.com.get_sh_result(self.user_node, cmd)
        self.log.info(result)
        assert_9 = "bash" not in result
        self.log.info(assert_9)
        self.assertTrue(assert_9, "执行失败:" + text)
        num1 = int(result)

        text = "--step3:向该分区插入数据;expect:插入数据失败 报错无权限"
        self.log.info(text)
        sql = f"insert into {self.t_name} " \
              f"values (4,'ddd',4,'2020-05-24',false,'ddd',4.4);"
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        assert_10 = "INSERT" not in result
        self.log.info(assert_10)
        assert_11 = "ERROR" in result
        self.log.info(assert_11)
        assert_12 = "Permission denied" in result
        self.log.info(assert_12)
        self.assertTrue(assert_10 and assert_11 and assert_12, "执行失败:" + text)

        text = "--step4:查看无core文件产生;expect:无core文件产生"
        self.log.info(text)
        result = self.com.get_sh_result(self.user_node, cmd)
        self.log.info(result)
        assert_13 = "bash" not in result
        self.log.info(assert_13)
        self.assertTrue(assert_13, "执行失败:" + text)
        num2 = int(result)

        text = "比对数据插入前后core文件数量"
        self.log.info(text)
        self.log.info(num1, num2)
        assert_14 = num1 >= num2
        self.log.info(assert_14)
        self.assertTrue(assert_14, "执行失败:" + text)

    def tearDown(self):
        text = "--step5:恢复环境;expect:恢复环境成功"
        self.log.info(text)
        self.log.info("恢复读写权限")
        cmd = f"chmod +rw {self.file_name};ls -l {self.file_name}"
        res = self.com.get_sh_result(self.user_node, cmd)
        self.log.info(res)

        self.log.info("删除表")
        result = self.primary_sh.execut_db_sql(f"drop table "
            f"if exists {self.t_name} cascade;")
        self.log.info(result)

        text = "执行结束db状态核对"
        self.log.info(text)
        status = self.primary_sh.get_db_cluster_status()
        assert_15 = "Degraded" in status or "Normal" in status
        self.log.info(assert_15)
        self.assertTrue(assert_15, "执行失败:" + text)
        self.log.info("==Opengauss_Function_DDL_Partition_Case0071执行结束==")
