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
Case Name   : 表空间创建限额生效
Description :
    1、创建tablespace设置限额3M
    2、创建表设置表空间为tablespace1
    3、循环插入数据直至表空间满
    4、验证表空间实际占用空间是否小于设置限额
Expect      :
    1、创建tablespace设置限额3M成功
    2、创建表设置表空间为tablespace1成功
    3、循环插入数据直至表空间满
    4、验证表空间实际占用空间小于设置限额
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
        self.tbspc_name1 = 'tsp_tbspc0019'
        self.tblspace_location1 = 'tbspc0019'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0019'
        self.connect_info = f'-U {self.sys_user} -W {self.pwd}'
        self.maxsize = 3
        self.max_num = 10000
        self.loop_num = 20
        self.table_test = 't_tbspc0019'
        self.create_sql = f'drop table if exists {self.table_test};' \
            f'create table {self.table_test}(id int) ' \
            f'tablespace {self.tbspc_name1};'
        self.insert_sql = f'''begin 
            for i in 1..{self.max_num} loop
            insert into {self.table_test} values(i);
            end loop;
            end;'''
        self.err_flag = f'ERROR:  Insufficient storage space for ' \
            f'tablespace "{self.tbspc_name1}"'

    def test_main(self):
        step_txt = '----step0:创建系统管理员用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step1:创建tablespace设置限额单位为M; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tblspace_location1}' " \
            f"maxsize '{self.maxsize}M';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('----检查tablespace设置限额大小----')
        check_sql = f"select spcmaxsize from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        set_size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(set_size)
        self.assertEqual(str(self.maxsize * 1024),
                         set_size.strip().split()[0], "执行失败" + step_txt)

        step_txt = '----step2:创建表设置表空间为tablespace; expect:创建成功----'
        self.log.info(step_txt)
        create_result = self.pri_sh.execut_db_sql(self.create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:在tablespace上创建的表循环插入数据; expect:表空间满正常报错----'
        self.log.info(step_txt)
        for i in range(self.loop_num):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = self.pri_sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
            if self.err_flag in insert_result:
                self.assertIn(self.err_flag, insert_result, "执行失败" + step_txt)
                break
        step_txt = '----step4:验证表空间实际占用空间是否小于设置限额; expect:实际占用空间为小于设置限额----'
        self.log.info(step_txt)
        check_sql = f"select pg_size_pretty(" \
            f"pg_tablespace_size('{self.tbspc_name1}'));"
        rel_size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(rel_size)
        self.assertLessEqual(int(rel_size.strip().split()[0]),
                             int(set_size.strip().split()[0]),
                             "执行失败" + step_txt)

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
