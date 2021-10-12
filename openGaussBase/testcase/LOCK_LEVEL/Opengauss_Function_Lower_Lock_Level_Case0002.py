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
Case Type   : 分区表锁降级
Case Name   : 分区表某一分区插入数据,不相邻分区同时也插入数据
Description :
    1、创建范围分区表;
    2、session1中向分区1插入数据;
    3、session2中同时在分区3插入数据;
    4、查看分区数据;
    5、清理环境;
Expect      :
    1、创建范围分区表成功;
    2、session1中插入数据成功;
    3、session2中同时插入数据成功，未阻塞;
    4、查看分区数据成功;
    5、清理环境成功;
History     :
"""

import unittest
import time
from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.CommonSQL import CommonSQL
from testcase.utils.Logger import Logger


class LockLevel(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0002开始执行--')
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.comSQL = CommonSQL('PrimaryDbUser')
        self.table_name = 't_locklevel_0002'
        self.function_name = 'f_locklevel_0002'

    def test_lock_level(self):
        self.log.info('------创建插入数据函数------')
        func_var = 'pvar'
        func_sql = f'''insert into {self.table_name} values({func_var},1);'''
        insert_func = self.comSQL.create_func(self.function_name,
                                              execute_sql=func_sql,
                                              var=func_var,
                                              start=20000,
                                              end=80000,
                                              step=20000)
        self.log.info(insert_func)
        self.assertTrue(self.function_name in insert_func)

        text = '------step1:创建范围分区表; expect:成功------'
        self.log.info(text)
        create_cmd = f'''drop table if exists {self.table_name};
            create table {self.table_name} (id1 int,id2 int) 
            partition by range (id1)
            (partition p00 values less than (20000),
             partition p01 values less than (40000),
             partition p02 values less than (60000));'''
        self.log.info(create_cmd)
        create_msg = self.comSQL.execut_db_sql(create_cmd)
        self.log.info(create_msg)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, create_msg,
                      '执行失败:' + text)

        text = '------step2:session1中向分区1插入数据; expect:成功------'
        self.log.info(text)
        insert_cmd1 = f'''select {insert_func}(19999);
            select count(*) from {self.table_name} partition for (19999);
            select pg_sleep(15);'''
        session_1 = ComThread(self.comsh.execut_db_sql, args=(insert_cmd1,))
        session_1.setDaemon(True)
        session_1.start()
        time.sleep(1)

        text = '------step3 & step4:session2中向分区3插入数据,查看分区数据; ' \
               'expect:插入数据成功,查看分区数据成功------'
        self.log.info(text)
        insert_cmd2 = f'''select {insert_func}(59999);
            select count(*) from {self.table_name} partition for (59999);'''
        session_2 = ComThread(self.comSQL.execut_db_sql, args=(insert_cmd2,))
        session_2.setDaemon(True)
        session_2.start()

        self.log.info('------session2执行结果------')
        session_2.join(10)
        session_2_result = session_2.get_result()
        self.log.info(session_2_result)
        self.assertTrue('20000' in session_2_result.splitlines()[-2],
                        "执行失败:" + text)

        text = '------session1执行结果------'
        self.log.info(text)
        session_1.join(30)
        session_1_result = session_1.get_result()
        self.log.info(session_1_result)
        self.assertTrue('20000' in session_1_result, "执行失败:" + text)

    def tearDown(self):
        text = '------step5:清理环境; expect:成功------'
        self.log.info(text)
        drop_cmd = f'''drop table {self.table_name} cascade;
            drop function {self.function_name};'''
        drop_msg = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_msg)
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0002执行完成--')
