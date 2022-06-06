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
Case Type   : 功能测试-表空间
Case Name   : 表空间创建不限额生效
Description :
    1、创建tablespace设置不限额
    2、创建表设置表空间为不限额表空间
    3、不限额表空间的表插入数据后，实际占用表空间查询
Expect      :
    1、创建tablespace设置不限额成功
    2、创建表设置表空间为不限额表空间成功
    3、不限额表空间的表插入数据后，实际占用表空间正常
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro


class Tablespace(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.tbspc_name1 = 'tsp_tbspc0020'
        self.tblspace_location1 = 'tbspc0020'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0020'
        self.connect_info = f'-U {self.sys_user} -W {self.pwd}'
        self.max_num = 1000
        self.loop_num = 10
        self.table_test = 't_tbspc0020'
        self.create_sql = f'drop table if exists {self.table_test};' \
            f'create table {self.table_test}(id int) ' \
            f'tablespace {self.tbspc_name1};'
        self.insert_sql = f'''begin 
            for i in 1..{self.max_num} loop
            insert into {self.table_test} values(i);
            end loop;
            end;'''

    def test_main(self):
        step_txt = '----step0:创建系统管理员用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop table if exists {self.table_test};" \
            f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step1:创建tablespace设置不限额; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tblspace_location1}' " \
            f"maxsize 'unlimited';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result)
        self.log.info('----检查tablespace设置限额大小----')
        check_sql = f"select spcmaxsize from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(size)
        self.assertEqual(' ', size)

        step_txt = '----step2:创建表设置表空间为不限额表空间成功; expect:创建成功----'
        self.log.info(step_txt)
        create_result = self.pri_sh.execut_db_sql(self.create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:在tablespace上创建的表循环插入数据; expect:实际占用表空间正常----'
        self.log.info(step_txt)
        for i in range(self.loop_num):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = self.pri_sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
        self.log.info('----查看表空间大小----')
        check_sql = f"select pg_size_pretty(pg_tablespace_size(" \
            f"'{self.tbspc_name1}'));"
        size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2].strip()
        self.log.info(size)
        self.assertGreater(int(size.strip().split()[0]), 0, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop table if exists {self.table_test};" \
            f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, clean_result,
                      "执行失败" + step1_txt)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, clean_result,
                      "执行失败" + step1_txt)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, clean_result,
                      "执行失败" + step1_txt)
