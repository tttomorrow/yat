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
Case Type   : upsert子查询功能
Case Name   : upsert子查询for update nowait语法验证
Description :
    1、初始创建测试数据
    2、session1以线程方式启动，对某行数据进行update后等待20s
    3、session1开始后等待5s，session2对session1事务内部相关表进行upsert子查询for update nowait
    4、验证session1未提交，session2直接返回异常；
    5、session1事务执行结果验证
    6、验证session2相关行数据未变更,session1相关数据正常update
Expect      :
    1、初始创建测试数据成功
    2、session1以线程方式启动，对某行数据进行update后等待20s
    3、session1开始后等待5s，session2对session1事务内部相关表进行upsert子查询for update nowait
    4、验证session1未提交，session2直接返回异常
    5、session1事务执行结果正常提交
    6、验证session2相关行数据未变更,session1相关数据正常update
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class UpsertCase132(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_DML_Upsert_Case0132:初始化----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t1 = 't_dml_upsert_sub0132'
        self.t2 = 't_dml_upsert0132'

    def test_main(self):
        self.log.info("--1、初始创建测试数据--")
        sql = f"drop table if exists {self.t1};" \
            f"create table {self.t1} (a int,b text);" \
            f"insert into {self.t1} values(generate_series(1,10)," \
            f"'b-'||generate_series(1,10));" \
            f"drop table if exists {self.t2};" \
            f"create table {self.t2} (a int primary key,b text,c text);" \
            f"insert into {self.t2} values (1,1,1),(2,2,2),(3,3,3);" \
            f"select * from {self.t2};select * from {self.t1};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertTrue("INSERT 0 10" in result and 'INSERT 0 3' in result)

        self.log.info("--2、session1以线程方式启动，对某行数据进行update后等待20s--")
        sql1 = f"begin;" \
            f"update {self.t1} set b ='bb-2' where a =2;" \
            f"select pg_sleep(20);" \
            f"end;"
        self.log.info(sql1)
        session1_excute = ComThread(self.pri_sh.execut_db_sql, args=(sql1,))
        session1_excute.setDaemon(True)
        session1_excute.start()
        time.sleep(5)

        self.log.info("--3、等待5s，session2对session1相关行进行子查询for update nowait--")
        sql2 = f"begin;" \
            f"insert into {self.t2} values(2) on duplicate key update b=" \
            f"(select b from {self.t1} where a = 2 for update nowait);" \
            f"end;"
        self.log.info(sql2)
        session2_result = self.pri_sh.execut_db_sql(sql2)

        self.log.info("--4、验证session1未提交，session2直接返回异常--")
        err_flag = "ERROR:  could not obtain lock on row "
        self.log.info(session2_result)
        self.assertIn(err_flag, session2_result)

        self.log.info("--5、session1事务执行结果--")
        session1_excute.join()
        session1_result = session1_excute.get_result()
        self.log.info(session1_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session1_result)

        self.log.info("--6、验证session2相关行数据未变更,session1相关数据正常update--")
        sql3 = f"select * from {self.t2} where a = 2;"
        result3 = self.pri_sh.execut_db_sql(sql3)
        self.log.info(result3)
        self.assertIn("2", result3)
        sql4 = f"select * from {self.t1} where a = 2;"
        result4 = self.pri_sh.execut_db_sql(sql4)
        self.log.info(result4)
        self.assertIn("bb-2", result4)

    def tearDown(self):
        self.log.info("--清理测试数据--")
        clean_sql = f"drop table if exists {self.t1};" \
            f"drop table if exists {self.t2};"
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)
        self.log.info('----Opengauss_Function_DML_Upsert_Case0132:用例执行完毕----')
