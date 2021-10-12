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
Case Name   : upsert子查询for update语法验证
Description :
    1、初始创建测试数据
    2、session1以线程方式启动，事务内部相关子查询for update后等待20s
    3、session1开始后等待5s，session2对session1相关的锁定行进行update
    4、验证session1提交后，session2才提交；
    5、session1事务执行结果验证
    6、验证session2是在session1事务提交后，才进行的update
Expect      :
    1、初始创建测试数据乘公共
    2、session1以线程方式启动，事务内部相关子查询for update后等待20s，session1开始执行
    3、session1开始后等待5s，session2对session1相关的锁定行进行update，session2开始执行
    4、验证session1提交后，session2才提交；session2事务提交总时长大于10s
    5、session1事务正常提交
    6、select方式验证，session1的update结果是session2提交之前的数据；
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class UpsertCase131(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_DML_Upsert_Case0131:初始化----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t1 = 't_dml_upsert_sub0131'
        self.t2 = 't_dml_upsert0131'

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

        self.log.info("--2、session1以线程方式启动，事务内部相关子查询for update后等待20s--")
        sql1 = f"begin;" \
            f"insert into {self.t2} values(2) on duplicate key update " \
            f"b= (select b from {self.t1} where a = excluded.a for update);" \
            f"select pg_sleep(20);" \
            f"end;"
        self.log.info(sql1)
        session1_excute = ComThread(self.pri_sh.execut_db_sql, args=(sql1,))
        session1_excute.setDaemon(True)
        session1_excute.start()
        time.sleep(5)

        self.log.info("--3、session1开始后等待5s，session2对session1相关的锁定行进行update--")
        sql2 = f"begin;" \
            f"update {self.t1} set b ='bb-2' where a =2;" \
            f"end;"
        self.log.info(sql2)
        start_time = time.time()
        session2_result = self.pri_sh.execut_db_sql(sql2)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session2_result)

        self.log.info("--4、验证session1提交后，session2才提交；session2事务提交总时长大于10s--")
        self.log.info(session2_result)
        end_time = time.time()
        self.log.info('start_time:' + str(start_time) +
                      ';end_time:' + str(end_time))
        self.log.info('session2执行等待时长' + str(end_time - start_time))
        self.assertTrue(end_time - start_time > 10)

        self.log.info("--5、session1事务执行结果--")
        session1_excute.join()
        session1_result = session1_excute.get_result()
        self.log.info(session1_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session1_result)

        self.log.info("--6、验证session2是在session1事务提交后，才进行的update--")
        sql3 = f"select * from {self.t2} where a = 2;"
        result3 = self.pri_sh.execut_db_sql(sql3)
        self.log.info(result3)
        self.assertIn("b-2", result3)
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
        self.log.info('----Opengauss_Function_DML_Upsert_Case0131:用例执行完毕----')
