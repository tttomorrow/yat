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
Case Type   : 分区表锁降级
Case Name   : 显示事务truncate全表,不提交,其他分区的查询计划执行成功
Description :
    1、创建范围分区表,插入数据;
    2、session1中开启事务，清空全表数据，不提交;
    3、session2中同时执行对其他分区的查询计划;
    4、清理环境;
Expect      :
    1、创建范围分区表成功,插入数据成功;
    2、session1中清空数据成功，待查询计划执行完后提交事务;
    3、session2中同时执行查询计划成功;
    4、清理环境成功;
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
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0117开始执行--')
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.comSQL = CommonSQL('PrimaryDbUser')
        self.tab_name = 't_locklevel_0117'
        self.i_function_name = 'f_insert_locklevel_0117'

    def test_lock_level(self):
        self.log.info('------创建插入数据函数------')
        func_var = 'pvar'
        func_sql1 = f'''insert into {self.tab_name} values({func_var},1);'''
        insert_func = self.comSQL.create_func(self.i_function_name,
                                              execute_sql=func_sql1,
                                              var=func_var,
                                              start=20000,
                                              end=80000,
                                              step=20000)
        self.log.info(insert_func)
        self.assertTrue(self.i_function_name in insert_func)

        text = '------step1:创建范围分区表,插入数据; expect:成功------'
        create_cmd = f'''drop table if exists {self.tab_name};
            create table {self.tab_name} (id1 int,id2 int) 
            partition by range (id1)
            (partition p00 values less than (20000),
             partition p01 values less than (40000),
             partition p02 values less than (60000));
            select {insert_func}(100);
            select {insert_func}(20100);
            select {insert_func}(40100);'''
        self.log.info(create_cmd)
        create_msg = self.comsh.execut_db_sql(create_cmd)
        self.log.info(create_msg)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in create_msg
                        and create_msg.count(self.i_function_name) == 3,
                        '执行失败:' + text)

        text = '------step2:session1中开启事务,清空表中数据,不提交; expect:成功------'
        self.log.info(text)
        update_cmd = f'''start transaction;
            truncate table {self.tab_name};
            select count(*) from {self.tab_name};
            select pg_sleep(10);
            commit;'''
        session_1 = ComThread(self.comsh.execut_db_sql, args=(update_cmd, ''))
        session_1.setDaemon(True)
        session_1.start()
        time.sleep(0.5)

        text = '---step3:session2中执行其他分区的查询计划,未提交时查询阻塞,提交后查询成功; expect:成功---'
        self.log.info(text)
        select_cmd = f'''explain select * from {self.tab_name} partition \
            for(39999) where id1 > 26666;'''
        session_2 = ComThread(self.comsh.execut_db_sql, args=(select_cmd,))
        session_2.setDaemon(True)
        session_2.start()

        self.log.info('------session2执行结果------')
        session_2.join(55)
        session_2_res = session_2.get_result()
        self.log.info(session_2_res)
        self.assertTrue('Partition Iterator' in session_2_res.splitlines()[2],
                        "执行失败:" + text)

        text = '------session1执行结果------'
        self.log.info(text)
        session_1.join(60)
        session_1_res = session_1.get_result()
        self.log.info(session_1_res)
        self.assertTrue(self.constant.TRUNCATE_SUCCESS_MSG in session_1_res
                        and '0' in session_1_res.splitlines()[4]
                        and self.constant.COMMIT_SUCCESS_MSG in session_1_res,
                        "执行失败:" + text)

    def tearDown(self):
        text = '------step4:清理环境; expect:成功------'
        self.log.info(text)
        drop_cmd = f'''drop table {self.tab_name} cascade;
            drop function {self.i_function_name};'''
        drop_msg = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_msg)
        self.assertTrue(self.constant.DROP_FUNCTION_SUCCESS_MSG in drop_msg
                        and self.constant.DROP_TABLE_SUCCESS in drop_msg,
                        '执行失败' + text)
        text = '------Opengauss_Function_Lower_Lock_Level_Case0117执行完成------'
        self.log.info(text)
