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
Case Name   : 分区表某一分区插入数据,跨分区同时查看数据
Description :
    1、创建范围分区表;
    2、向分区2、分区3中插入数据;
    3、session1中开启事务，向分区1插入数据;
    4、session2中同时在分区2、分区3查看数据;
    5、清理环境;
Expect      :
    1、创建范围分区表成功;
    2、插入数据成功;
    3、session1中插入数据成功;
    4、session2中同时查看数据成功，未阻塞;
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
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0095开始执行--')
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.comSQL = CommonSQL('PrimaryDbUser')
        self.table_name = 't_locklevel_0095'
        self.function_name = 'f_insert_locklevel_0095'

    def test_lock_level(self):
        self.log.info('------创建插入数据函数------')
        func_var = 'pvar'
        func_sql1 = f'''insert into {self.table_name} values({func_var},1);'''
        insert_func = self.comSQL.create_func(self.function_name,
                                              execute_sql=func_sql1,
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

        text = '-----step2:首先向分区2和分区3中插入数据; expect:成功-----'
        self.log.info(text)
        sql = f'''select {insert_func}(20100);
            select {insert_func}(40100);
            select count(*) from {self.table_name};'''
        self.log.info(sql)
        msg = self.comsh.execut_db_sql(sql)
        self.log.info(msg)
        self.assertTrue('202' in msg.splitlines()[-2].strip(),
                        '执行失败' + text)

        text = '------step3:session1中开启事务,向分区1插入数据; expect:成功------'
        self.log.info(text)
        insert_cmd = f'''start transaction;
            select {insert_func}(100);
            select pg_sleep(5);
            commit;'''
        session_1 = ComThread(self.comsh.execut_db_sql, args=(insert_cmd, ''))
        session_1.setDaemon(True)
        session_1.start()
        time.sleep(1)

        text = '------step4:session2中在分区2和分区3中查看数据; expect:查看数据成功------'
        self.log.info(text)
        select_cmd = f'''select count(*) from {self.table_name};'''
        session_2 = ComThread(self.comSQL.execut_db_sql, args=(select_cmd,))
        session_2.setDaemon(True)
        session_2.start()

        self.log.info('------session2执行结果------')
        session_2.join(50)
        session_2_result = session_2.get_result()
        self.log.info(session_2_result)
        self.assertTrue('202' in session_2_result.splitlines()[-2],
                        "执行失败:" + text)

        text = '------session1执行结果------'
        self.log.info(text)
        session_1.join(60)
        session_1_result = session_1.get_result()
        self.log.info(session_1_result)
        self.assertTrue(self.constant.COMMIT_SUCCESS_MSG in session_1_result,
                        "执行失败:" + text)

    def tearDown(self):
        text = '------step5:清理环境; expect:成功------'
        self.log.info(text)
        drop_cmd = f'''drop table {self.table_name} cascade;
            drop function {self.function_name};'''
        drop_msg = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_msg)
        self.assertTrue(self.constant.DROP_TABLE_SUCCESS in drop_msg and
                        self.constant.DROP_FUNCTION_SUCCESS_MSG in drop_msg,
                        '执行失败' + text)
        text = '------Opengauss_Function_Lower_Lock_Level_Case0095执行完成------'
        self.log.info(text)
