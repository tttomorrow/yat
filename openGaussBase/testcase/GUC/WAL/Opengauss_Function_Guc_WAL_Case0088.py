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
Case Type   : 服务端工具
Case Name   : 将synchronous_commit参数分别设为remote_apply和on，对比commit时间
Description :
    1.查询参数synchronous_commit默认值
    2.事务开始,设置synchronous_commit参数设为remote_apply,建表并插入数据,然后commit
    start transaction;
    set synchronous_commit to remote_apply;
    drop table if exists tablename;
    create table tablename(id bigint,random_char character varying(50),
    random_int bigint);
    insert into tablename select generate_series(1, 300000) as id,
     md5(random()::text) as info ,trunc(random()*300000);
    select count(*) from tablename;
    truncate table tablename;
    commit;
    3.查看commit时间
    4.恢复参数值为默认
    5.删除表
    drop table tablename;
    6.事务开始,设置synchronous_commit参数设为on,建表并插入数据,然后commit
    start transaction;
    set synchronous_commit to on;
    drop table if exists tablename cascade;
    create table tablename(id bigint,random_char character varying(50),
    random_int bigint);
    insert into tablename select generate_series(1, 300000) as id,
    md5(random()::text) as info ,trunc(random()*300000);
    select count(*) from tablename;
    truncate table tablename;
    7.查看commit时间
    commit;
    8.对比参数值为remote_apply比on的commit时间长
    9.恢复参数值为默认
    10.删除表
    drop table tablename;
Expect      :
    1.查询参数synchronous_commit默认值
    2.事务开始,设置synchronous_commit参数设为remote_apply,建表并插入数据,然后commit
    3.查看commit时间
    4.恢复参数值为默认
    5.删除表
    6.事务开始,设置synchronous_commit参数设为on,建表并插入数据,然后commit
    7.查看commit时间
    8.对比参数值为remote_apply比on的commit时间长
    9.恢复参数值为默认
    10.删除表
History     :
        所以修改为500次同步，减少其他因素影响
"""

import os
import timeit
import unittest

from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.tb_name = "t_guc0088"
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')

        self.log.info('等待同步完成')
        self.node_num = self.pri_sh.get_node_num()
        self.sta_sh = []
        for i in range(int(self.node_num) - 1):
            self.sta_sh.append(CommonSH(f'Standby{i + 1}DbUser'))
            result = self.sta_sh[i].check_data_consistency()
            self.assertTrue(result)

    def test_guc(self):
        text = '--step1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.common.show_param("synchronous_commit")

        text = '--step2.事务开始,设置synchronous_commit参数设为remote_apply,' \
               '建表并插入数据,然后commit;expect:操作成功--'
        self.log.info(text)
        inner_sql_cmd = f'''drop table if  exists {self.tb_name}; 
            create table {self.tb_name}(col text);'''
        for i in range(500):
            inner_sql_cmd += f'''start transaction;
                set synchronous_commit to remote_apply;
                show synchronous_commit;
                insert into {self.tb_name} values ('test{i}');
                commit;'''
        inner_sql_cmd += f'''select count(*) from {self.tb_name};'''
        start_time1 = timeit.default_timer()
        self.log.info(start_time1)
        sql_res = self.pri_sh.execut_db_sql(inner_sql_cmd)
        self.log.info(sql_res)
        end_time1 = timeit.default_timer()
        self.log.info(end_time1)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_res,
                      '执行失败:' + text)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)

        text = '--step3.查看commit时间;expect:查询成功--'
        self.log.info(text)
        commit_time1 = end_time1 - start_time1
        self.log.info(f'参数值为remote_apply时commit的时间花费为:{commit_time1}')

        text = '--step4.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        set_cmd = self.pri_sh.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"synchronous_commit="
                                            f"{self.default_value}")
        self.log.info(set_cmd)
        self.default_value1 = self.common.show_param("synchronous_commit")
        self.assertIn(self.default_value1, self.default_value1,
                      '执行失败:' + text)

        text = '--step5.删除表;expect:删除成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop table if  exists {self.tb_name};')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        self.log.info('等待同步完成')
        self.node_num = self.pri_sh.get_node_num()
        self.sta_sh = []
        for i in range(int(self.node_num) - 1):
            self.sta_sh.append(CommonSH(f'Standby{i + 1}DbUser'))
            result = self.sta_sh[i].check_data_consistency()
            self.assertTrue(result)

        text = '--step6.事务开始,设置synchronous_commit参数设为on,' \
               '建表并插入数据,然后commit;expect:操作成功--'
        self.log.info(text)
        inner_sql_cmd = inner_sql_cmd.replace('remote_apply', 'on')
        start_time2 = timeit.default_timer()
        self.log.info(start_time2)
        sql_res = self.pri_sh.execut_db_sql(inner_sql_cmd)
        self.log.info(sql_res)
        end_time2 = timeit.default_timer()
        self.log.info(end_time2)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_res,
                      '执行失败:' + text)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)

        text = '--step7.查看commit时间;expect:查询成功--'
        self.log.info(text)
        commit_time2 = end_time2 - start_time2
        self.log.info(f'参数值为on时commit的时间花费为:{commit_time2}')

        text = '--step8.对比参数值为remote_apply和on的commit时长;' \
               'expect:参数值为remote_apply比on的commit时间长--'
        self.log.info(text)
        self.log.info(f'参数值为remote_apply的commit时长:{commit_time1}')
        self.log.info(f'参数值为on的commit时长:{commit_time2}')
        self.assertTrue(commit_time1 > commit_time2)

    def tearDown(self):
        text = '--step9.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        set_cmd = self.pri_sh.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"synchronous_commit="
                                            f"{self.default_value}")
        self.log.info(set_cmd)
        text = '--step10.删除表;expect:删除成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop table if  exists {self.tb_name};')
        self.log.info(sql_cmd)
        self.recovery_value = self.common.show_param("synchronous_commit")
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
