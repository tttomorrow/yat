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
Case Name   : 显示事务drop分区提交,其他分区加入全局索引查询的计划执行成功
Description :
    1、创建范围分区表,创建全局索引;
    2、向分区1、分区2、分区3中插入数据;
    3、session1中开启事务，drop分区并提交;
    4、session2中同时执行对其他分区加入全局索引的查询计划;
    5、清理环境;
Expect      :
    1、创建范围分区表成功,创建索引成功;
    2、插入数据成功;
    3、session1中drop分区成功;
    4、session2中同时执行查询计划成功，未阻塞;
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
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0112开始执行--')
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.comSQL = CommonSQL('PrimaryDbUser')
        self.tab_name = 't_locklevel_0112'
        self.index_name = 'i_locklevel_0112'
        self.i_function_name = 'f_insert_locklevel_0112'

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

        text = '------step1:创建范围分区表,创建全局索引; expect:成功------'
        self.log.info(text)
        create_cmd = f'''drop table if exists {self.tab_name};
            drop index if exists {self.index_name};
            create table {self.tab_name} (id1 int,id2 int) 
            partition by range (id1)
            (partition p00 values less than (20000),
             partition p01 values less than (40000),
             partition p02 values less than (60000));
            create index {self.index_name} on {self.tab_name}(id1) global;'''
        self.log.info(create_cmd)
        create_msg = self.comSQL.execut_db_sql(create_cmd)
        self.log.info(create_msg)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in create_msg
                        and self.constant.CREATE_INDEX_SUCCESS in create_msg,
                        '执行失败:' + text)

        text = '-----step2:首先向分区1、分区2、分区3中插入部分数据; expect:成功-----'
        self.log.info(text)
        sql = f'''select {insert_func}(100);
            select {insert_func}(20100);
            select {insert_func}(40100);
            select count(*) from {self.tab_name};'''
        self.log.info(sql)
        msg = self.comsh.execut_db_sql(sql)
        self.log.info(msg)
        self.assertTrue('303' in msg.splitlines()[-2].strip(),
                        '执行失败' + text)

        text = '------step3:session1中开启事务,删除分区并提交; expect:成功------'
        self.log.info(text)
        update_cmd = f'''start transaction;
            alter table {self.tab_name} drop partition p00;
            select relname from pg_partition where parentid = \
            (select oid from pg_class where relname = '{self.tab_name}') \
            order by relname;
            commit;'''
        session_1 = ComThread(self.comsh.execut_db_sql, args=(update_cmd, ''))
        session_1.setDaemon(True)
        session_1.start()
        time.sleep(0.5)

        text = '---step4 & step5:session2中执行查询计划; expect:成功---'
        self.log.info(text)
        select_cmd = f'''explain select * from {self.tab_name} \
            partition for(39999) where id1=36666;'''
        session_2 = ComThread(self.comSQL.execut_db_sql, args=(select_cmd,))
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
        self.assertTrue(self.constant.ALTER_TABLE_MSG in session_1_res
                        and 'p00' not in session_1_res
                        and self.constant.COMMIT_SUCCESS_MSG in session_1_res,
                        "执行失败:" + text)

    def tearDown(self):
        text = '------step6:清理环境; expect:成功------'
        self.log.info(text)
        drop_cmd = f'''drop table {self.tab_name} cascade;
            drop function {self.i_function_name};'''
        drop_msg = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_msg)
        self.assertTrue(self.constant.DROP_FUNCTION_SUCCESS_MSG in drop_msg
                        and self.constant.DROP_TABLE_SUCCESS in drop_msg,
                        '执行失败' + text)
        text = '------Opengauss_Function_Lower_Lock_Level_Case0112执行完成------'
        self.log.info(text)
