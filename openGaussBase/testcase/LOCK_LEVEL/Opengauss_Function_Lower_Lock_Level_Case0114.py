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
Case Name   : 显示事务exchange分区，不提交,其他分区的查询计划执行成功
Description :
    1、分别创建同字段普通表、范围分区表,普通表中插入数据;
    2、session1中开启事务，将普通表的数据交换到分区表对应分区中，不提交;
    3、session2中同时执行对其他分区的查询计划;
    4、清理环境;
Expect      :
    1、创建普通表、范围分区表成功,普通表插入数据成功;
    2、session1中交换数据成功，待查询计划执行完后提交事务;
    3、session2中同时执行查询计划成功，未阻塞;
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
        self.log.info('--Opengauss_Function_Lower_Lock_Level_Case0114开始执行--')
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.p_tab = 't_locklevel_0114_part'
        self.r_tab = 't_locklevel_0114_row'

    def test_lock_level(self):
        text = '------step1:创建范围分区表,创建同字段行存表; expect:成功------'
        create_cmd = f'''drop table if exists {self.p_tab};
            drop table if exists {self.r_tab};
            create table {self.p_tab} (id1 int,id2 int) 
            partition by range (id1)
            (partition p00 values less than (20000),
             partition p01 values less than (40000),
             partition p02 values less than (60000));
            create table {self.r_tab}(id1 int,id2 int);
            insert into {self.r_tab} \
            values(generate_series(0,100),generate_series(0,100));'''
        self.log.info(create_cmd)
        create_msg = self.comsh.execut_db_sql(create_cmd)
        self.log.info(create_msg)
        self.assertTrue(
            create_msg.count(self.constant.CREATE_TABLE_SUCCESS) == 2,
            '执行失败:' + text)

        text = '------step2:session1中开启事务,将普通表的数据交换到分区表对应分区中，不提交; ' \
               'expect:成功------'
        self.log.info(text)
        update_cmd = f'''start transaction;
            alter table {self.p_tab} exchange partition (p00) \
            with table {self.r_tab};
            select count(*) from {self.r_tab};
            select count(*) from {self.p_tab} partition for (19999);
            select pg_sleep(10);
            commit;'''
        session_1 = ComThread(self.comsh.execut_db_sql, args=(update_cmd, ''))
        session_1.setDaemon(True)
        session_1.start()
        time.sleep(0.5)

        text = '---step3:session2中执行其他分区的查询计划,未提交时查询阻塞,提交后查询成功; expect:成功---'
        self.log.info(text)
        select_cmd = f'''explain select count(*) from {self.p_tab} \
            partition for(39999);'''
        session_2 = ComThread(self.comsh.execut_db_sql, args=(select_cmd,))
        session_2.setDaemon(True)
        session_2.start()

        self.log.info('------session2执行结果------')
        session_2.join(20)
        session_2_res = session_2.get_result()
        self.log.info(session_2_res)
        self.assertTrue('Partition Iterator' in session_2_res.splitlines()[3],
                        "执行失败:" + text)

        text = '------session1执行结果------'
        self.log.info(text)
        session_1.join(30)
        session_1_res = session_1.get_result()
        self.log.info(session_1_res)
        self.assertTrue(self.constant.ALTER_TABLE_MSG in session_1_res
                        and '101' in session_1_res.splitlines()[9]
                        and '0' == session_1_res.splitlines()[4].strip()
                        and self.constant.COMMIT_SUCCESS_MSG in session_1_res,
                        "执行失败:" + text)

    def tearDown(self):
        text = '------step4:清理环境; expect:成功------'
        self.log.info(text)
        drop_cmd = f'''drop table {self.p_tab} cascade;
            drop table {self.r_tab} cascade;'''
        drop_msg = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_msg)
        self.assertTrue(drop_msg.count(self.constant.DROP_TABLE_SUCCESS) == 2,
                        '执行失败' + text)
        text = '------Opengauss_Function_Lower_Lock_Level_Case0114执行完成------'
        self.log.info(text)
