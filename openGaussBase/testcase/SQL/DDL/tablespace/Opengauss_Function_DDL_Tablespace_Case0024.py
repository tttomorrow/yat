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
Case Name   : 表空间修改-重命名
Description :
    1、修改不存在的表空间名为另一已存在表空间名
    2、修改不存在的表空间名为另一不存在表空间名
    3、修改已存在的表空间名为另一已存在表空间名
    4、修改已存在的表空间名为pg_开头的表空间名
    5、修改已存在的表空间名为不存在表空间名
Expect      :
    1、修改不存在的表空间名为另一已存在表空间名，修改失败
    2、修改不存在的表空间名为另一不存在表空间名，修改失败
    3、修改已存在的表空间名为另一已存在表空间名，修改失败
    4、修改已存在的表空间名为pg_开头的表空间名，修改失败
    5、修改已存在的表空间名为另一不存在表空间名，修改成功
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
        self.sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.tbspc_name1 = 'tsp_tbspc0024_1'
        self.tbspc_location1 = 'tbspc0024_1'
        self.tbspc_name2 = 'tsp_tbspc0024_2'
        self.tbspc_location2 = 'tbspc0024_2'
        self.tbspc_name3 = 'tsp_tbspc0024_3'
        self.tbspc_name4 = 'pg_tsp_tbspc0024_4'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0024'
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.err_flag1 = f'ERROR:  tablespace "{self.tbspc_name2}"' \
            f' does not exist'
        self.err_flag2 = f'ERROR:  tablespace "{self.tbspc_name2}"' \
            f' already exists'
        self.err_flag3 = 'DETAIL:  The prefix "pg_" is reserved ' \
                         'for system tablespaces.'

    def test_main(self):
        step_txt = '----step0:创建系统管理员; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        self.log.info(create_sql)
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step0:创建tablespace1; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}';"

        create_result = self.sh.execut_db_sql(create_sql,
                                              sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace oid--')
        select_sql = f"select oid from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        tblspc1_oid = self.sh.execut_db_sql(select_sql).splitlines()[-2]
        self.log.info(tblspc1_oid)

        step_txt = '----step1:修改不存在的表空间名为另一已存在表空间名; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name2} " \
            f"rename to {self.tbspc_name1};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag1, alter_result, "执行失败" + step_txt)

        step_txt = '----step2:修改不存在的表空间名为另一不存在表空间名; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name2} " \
            f"rename to {self.tbspc_name3};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag1, alter_result, "执行失败" + step_txt)

        step_txt = '----step0:创建tablespace2; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name2} " \
            f"relative location '{self.tbspc_location2}';"
        create_result = self.sh.execut_db_sql(create_sql,
                                              sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:修改已存在的表空间名为另一已存在表空间名; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"rename to {self.tbspc_name2};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag2, alter_result, "执行失败" + step_txt)

        step_txt = '----step4:修改已存在的表空间名为pg_开头的表空间名; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name2} " \
            f"rename to {self.tbspc_name4};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag3, alter_result, "执行失败" + step_txt)

        step_txt = '----step5:修改已存在的表空间名为不存在表空间名; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"rename to {self.tbspc_name3};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        select_sql = f'select spcname from pg_tablespace ' \
            f'where oid = {tblspc1_oid};'
        new_name = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info(new_name)
        self.assertEqual(self.tbspc_name3, new_name)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"drop tablespace if exists {self.tbspc_name3}; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(1, drop_user, "执行失败" + step1_txt)
        self.assertEqual(3, drop_tbspc, "执行失败" + step1_txt)
