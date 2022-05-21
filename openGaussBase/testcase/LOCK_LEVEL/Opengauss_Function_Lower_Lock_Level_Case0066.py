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
Case Name   : truncate表,同时update数据
Description :
    1、创建范围分区表,插入数据;
    2、session1中truncate表中数据;
    3、session2中同时在某一分区update数据;
    4、查看表中数据;
    5、清理环境;
Expect      :
    1、创建范围分区表成功,插入数据成功;
    2、session1中truncate表中数据成功;
    3、session2中同时update数据成功，未阻塞;
    4、查看数据成功;
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
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0066开始执行--')
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.comSQL = CommonSQL('PrimaryDbUser')
        self.table_name = 't_locklevel_0066'
        self.i_function_name = 'f_insert_locklevel_0066'
        self.u_function_name = 'f_update_locklevel_0066'

    def test_lock_level(self):
        self.log.info('------创建插入数据函数------')
        func_var = 'pvar'
        func_sql1 = f'''insert into {self.table_name} \
            values({func_var},1);'''
        insert_func = self.comSQL.create_func(self.i_function_name,
                                              execute_sql=func_sql1,
                                              var=func_var,
                                              start=20000,
                                              end=80000,
                                              step=20000)
        self.log.info(insert_func)
        self.assertTrue(self.i_function_name in insert_func)

        self.log.info('------创建更新数据函数------')
        func_sql2 = f'''update {self.table_name} set id2 = 8 
            where id1={func_var};'''
        update_func = self.comSQL.create_func(self.u_function_name,
                                              execute_sql=func_sql2,
                                              var=func_var,
                                              start=20000,
                                              end=80000,
                                              step=20000)
        self.log.info(update_func)
        self.assertTrue(self.u_function_name in update_func)

        text = '------step1:创建范围分区表,插入数据;  expect:成功------'
        self.log.info(text)
        create_cmd = f'''drop table if exists {self.table_name};
            create table {self.table_name} (id1 int,id2 int) 
            partition by range (id1)
            (partition p00 values less than (20000),
             partition p01 values less than (40000),
             partition p02 values less than (60000));
            select {insert_func}(20100);'''
        self.log.info(create_cmd)
        create_msg = self.comSQL.execut_db_sql(create_cmd)
        self.log.info(create_msg)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in create_msg
                        and create_msg.count(self.i_function_name) == 1,
                        '执行失败:' + text)

        text = '------step2:session1中truncate表中数据; expect:成功------'
        self.log.info(text)
        add_cmd = f'''truncate table {self.table_name};'''
        session_1 = ComThread(self.comsh.execut_db_sql, args=(add_cmd, ''))
        session_1.setDaemon(True)
        session_1.start()
        time.sleep(1)

        text = '---step3 & step4:session2中同时在分区中update数据; expect:更新数据成功---'
        self.log.info(text)
        select_cmd = f'''select {update_func}(20100);
            select * from {self.table_name} partition for(20100) limit 1;'''
        session_2 = ComThread(self.comSQL.execut_db_sql, args=(select_cmd,))
        session_2.setDaemon(True)
        session_2.start()

        self.log.info('------session1执行结果------')
        session_1.join(55)
        session_1_res = session_1.get_result()
        self.log.info(session_1_res)
        self.assertTrue(self.constant.TRUNCATE_SUCCESS_MSG in session_1_res,
                        "执行失败:" + text)

        text = '------session2执行结果------'
        self.log.info(text)
        session_2.join(60)
        session_2_res = session_2.get_result()
        self.log.info(session_2_res)
        self.assertTrue(self.u_function_name in session_2_res
                        and '(0 rows)' in session_2_res.splitlines()[-1],
                        "执行失败:" + text)

    def tearDown(self):
        text = '------step5:清理环境; expect:成功------'
        self.log.info(text)
        drop_cmd = f'''drop table {self.table_name} cascade;
            drop function {self.i_function_name};
            drop function {self.u_function_name};'''
        drop_msg = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_msg)
        self.assertTrue(
            drop_msg.count(self.constant.DROP_FUNCTION_SUCCESS_MSG) == 2
            and self.constant.DROP_TABLE_SUCCESS in drop_msg,
            '执行失败' + text)
        text = '------Opengauss_Function_Lower_Lock_Level_Case0066执行完成------'
        self.log.info(text)
