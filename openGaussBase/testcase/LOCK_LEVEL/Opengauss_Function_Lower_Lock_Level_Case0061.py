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
Case Name   : alter exchange分区,同时不相邻分区delete数据
Description :
    1、分别创建同字段普通表、范围分区表,表中分别插入数据;
    2、session1中将普通表的数据交换到分区表对应分区中;
    3、session2中同时在不相邻分区中delete数据;
    4、查看分区数据;
    5、清理环境;
Expect      :
    1、创建普通表、范围分区表成功,普通表插入数据成功;
    2、session1中交换数据成功;
    3、session2中同时在不相邻分区中delete数据成功，未阻塞;
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
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0061开始执行--')
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.comSQL = CommonSQL('PrimaryDbUser')
        self.table_name_row = 't_locklevel_0061_row'
        self.table_name_part = 't_locklevel_0061_part'
        self.i_function_name = 'f_insert_locklevel_0061'
        self.d_function_name = 'f_delete_locklevel_0061'

    def test_lock_level(self):
        self.log.info('------创建插入数据函数------')
        func_var = 'pvar'
        func_sql1 = f'''insert into {self.table_name_part} \
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
        func_sql2 = f'''delete from {self.table_name_part} \
            where id1={func_var};'''
        delete_func = self.comSQL.create_func(self.d_function_name,
                                              execute_sql=func_sql2,
                                              var=func_var,
                                              start=20000,
                                              end=80000,
                                              step=20000)
        self.log.info(delete_func)
        self.assertTrue(self.d_function_name in delete_func)

        text = '------step1:创建普通表、范围分区表,插入数据; expect:成功------'
        self.log.info(text)
        create_cmd = f'''drop table if exists {self.table_name_part};
            drop table if exists {self.table_name_row};
            create table {self.table_name_part} (id1 int,id2 int) 
            partition by range (id1)
            (partition p00 values less than (20000),
             partition p01 values less than (40000),
             partition p02 values less than (60000));
            create table {self.table_name_row}(id1 int,id2 int);
            insert into {self.table_name_row} \
            values(generate_series(0,100),generate_series(0,100));
            select {insert_func}(40100);'''
        self.log.info(create_cmd)
        create_msg = self.comSQL.execut_db_sql(create_cmd)
        self.log.info(create_msg)
        self.assertTrue(
            create_msg.count(self.constant.CREATE_TABLE_SUCCESS) == 2
            and self.i_function_name in create_cmd, '执行失败:' + text)

        text = '------step2:session1中交换普通表中数据; expect:成功------'
        self.log.info(text)
        add_cmd = f'''alter table {self.table_name_part} exchange \
            partition (p00) with table {self.table_name_row};
            select count(*) from {self.table_name_row};
            select count(*) from {self.table_name_part} \
            partition for (100);'''
        session_1 = ComThread(self.comsh.execut_db_sql, args=(add_cmd, ''))
        session_1.setDaemon(True)
        session_1.start()
        time.sleep(0.5)

        text = '---step3 & step4:session2中同时在不相邻分区中delete数据; expect:删除数据成功---'
        self.log.info(text)
        select_cmd = f'''select {delete_func}(40100);
            select count(*) from {self.table_name_part} partition \
            for(40100) limit 1;'''
        session_2 = ComThread(self.comSQL.execut_db_sql, args=(select_cmd,))
        session_2.setDaemon(True)
        session_2.start()

        self.log.info('------session2执行结果------')
        session_2.join(55)
        session_2_res = session_2.get_result()
        self.log.info(session_2_res)
        self.assertTrue(self.d_function_name in session_2_res.splitlines()[0]
                        and '0' in session_2_res.splitlines()[-2].strip(),
                        "执行失败:" + text)

        text = '------session1执行结果------'
        self.log.info(text)
        session_1.join(60)
        session_1_res = session_1.get_result()
        self.log.info(session_1_res)
        self.assertTrue(self.constant.ALTER_TABLE_MSG in session_1_res
                        and '101' in session_1_res.splitlines()[-2]
                        and '0' in session_1_res.splitlines()[3].strip(),
                        "执行失败:" + text)

    def tearDown(self):
        text = '------step5:清理环境; expect:成功------'
        self.log.info(text)
        drop_cmd = f'''drop table {self.table_name_row} cascade;
            drop table {self.table_name_part} cascade;
            drop function {self.i_function_name};
            drop function {self.d_function_name};'''
        drop_msg = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_msg)
        self.assertTrue(
            drop_msg.count(self.constant.DROP_TABLE_SUCCESS) == 2
            and drop_msg.count(self.constant.DROP_FUNCTION_SUCCESS_MSG) == 2,
            '执行失败' + text)
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0061执行完成--')
