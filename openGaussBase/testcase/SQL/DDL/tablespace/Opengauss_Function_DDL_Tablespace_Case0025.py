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
Case Name   : 表空间修改-修改所有者
Description :
    0.创建系统管理员/普通用户;
    0.创建tablespace1;
    1.修改tablespace1所有者为不存在用户;
    2.修改tablespace1所有者为存在用户com_user1;
    3.1.创建普通用户com_user2(与com_user1不存在直接间接成员关系);
    3.2.普通用户com_user1修改其所有者表空间的所有者为com_user2;
    4.1.修改com_user2为com_user1的直接成员;
    4.2.普通用户com_user1修改其所有者表空间的所有者为com_user2;
    5.1.修改com_user1为com_user2的直接成员;
    5.2.普通用户com_user1修改其所有者表空间的所有者为com_user2;
    6.1.创建普通用户com_user3;
    6.2.修改com_user2为com_user1的间接成员;
    6.3.普通用户com_user2修改其所有者表空间的所有者为com_user1;
Expect      :
    0.创建系统管理员/普通用户; expect: 创建成功
    0.创建tablespace1; expect: 创建成功
    1.修改tablespace1所有者为不存在用户; expect: 修改失败
    2.修改tablespace1所有者为存在用户com_user1; expect: 修改成功
    3.1.创建普通用户com_user2(与com_user1不存在直接间接成员关系); expect: 创建成功
    3.2.普通用户com_user1修改其所有者表空间的所有者为com_user2; expect: 修改失败
    4.1.修改com_user2为com_user1的直接成员; expect: 修改成功
    4.2.普通用户com_user1修改其所有者表空间的所有者为com_user2; expect: 修改失败
    5.1.修改com_user1为com_user2的直接成员; expect: 修改成功
    5.2.普通用户com_user1修改其所有者表空间的所有者为com_user2; expect: 修改成功
    6.1.创建普通用户com_user3; expect: 创建成功
    6.2.修改com_user2为com_user1的间接成员; expect: 修改成功
    6.3.普通用户com_user2修改其所有者表空间的所有者为com_user1; expect: 修改成功
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
        self.tbspc_name1 = 'tsp_tbspc0025'
        self.tbspc_location1 = 'tbspc0025'
        self.sys_user = 'u_tbspc0025_sys'
        self.pwd = macro.PASSWD_INITIAL
        self.com_user1 = 'u_tbspc0025_com1'
        self.com_user2 = 'u_tbspc0025_com2'
        self.com_user3 = 'u_tbspc0025_com3'
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.connect_com1 = f'-U {self.com_user1} -W {self.pwd}'
        self.connect_com2 = f'-U {self.com_user2} -W {self.pwd}'
        self.grant_success = 'GRANT ROLE'
        self.err_flag1 = f'ERROR:  role "{self.com_user2}" does not exist'
        self.err_flag2 = f'ERROR:  must be member of role'

    def test_main(self):
        step_txt = '----step0:创建系统管理员/普通用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.com_user1} cascade; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.com_user1} password '{self.pwd}';" \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        self.log.info(create_sql)
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step0:创建tablespace1; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}';"
        create_result = self.sh.execut_db_sql(create_sql,
                                              sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace1所有者--')
        check_owner = f"select spcowner from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        select_sql = f"select usesysid from pg_user where " \
            f"usename= '{self.sys_user}';"
        sys_id = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info(sys_id)
        self.assertEqual(owner1, sys_id, "执行失败" + step_txt)

        step_txt = '----step1:修改tablespace1所有者为不存在用户; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"owner to {self.com_user2};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag1, alter_result, "执行失败" + step_txt)

        step_txt = '----step2:修改tablespace1所有者为存在用户com_user1; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"owner to {self.com_user1};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace1所有者--')
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        select_sql = f"select usesysid from pg_user where " \
            f"usename= '{self.com_user1}';"
        com1_id = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info(com1_id)
        self.assertEqual(owner1, com1_id, "执行失败" + step_txt)

        step_txt = '----step3.1:创建普通用户com_user2(与com_user1不存在直接间接成员关系); ' \
                   'expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop user if exists {self.com_user2} cascade; " \
            f"create user {self.com_user2} password '{self.pwd}';"
        self.log.info(create_sql)
        create_result = self.sh.execut_db_sql(create_sql,
                                              sql_type=self.connect_sys)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)
        select_sql = f"select usesysid from pg_user where " \
            f"usename= '{self.com_user2}';"
        com2_id = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info(com2_id)

        step_txt = '----step3.2:普通用户com_user1修改其所有者表空间的所有者为com_user2; ' \
                   'expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"owner to {self.com_user2};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com1)
        self.log.info(alter_result)
        self.assertIn(self.err_flag2, alter_result, "执行失败" + step_txt)

        step_txt = '----step4.1:修改com_user2为com_user1的直接成员; expect:修改成功----'
        self.log.info(step_txt)
        grant_sql = f"grant {self.com_user1} to {self.com_user2};\du;"
        grant_result = self.sh.execut_db_sql(grant_sql,
                                             sql_type=self.connect_com1)
        self.log.info(grant_result)
        self.assertIn(self.grant_success, grant_result, "执行失败" + step_txt)

        step_txt = '----step4.2:普通用户com_user1修改其所有者表空间的所有者为com_user2; ' \
                   'expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"owner to {self.com_user2};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com1)
        self.log.info(alter_result)
        self.assertIn(self.err_flag2, alter_result, "执行失败" + step_txt)

        step_txt = '----step5.1:修改com_user1为com_user2的直接成员; expect:修改成功----'
        self.log.info(step_txt)
        grant_sql = f"revoke {self.com_user1} from {self.com_user2};" \
            f"grant {self.com_user2} to {self.com_user1};\du;"

        grant_result = self.sh.execut_db_sql(grant_sql,
                                             sql_type=self.connect_sys)
        self.log.info(grant_result)
        self.assertIn(self.grant_success, grant_result, "执行失败" + step_txt)

        step_txt = '----step5.2:普通用户com_user1修改其所有者表空间的所有者为com_user2; ' \
                   'expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"owner to {self.com_user2};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com1)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        self.assertEqual(owner1, com2_id, "执行失败" + step_txt)

        step_txt = '----step6.1:创建普通用户com_user3; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop user if exists {self.com_user3} cascade; " \
            f"create user {self.com_user3} password '{self.pwd}';"
        self.log.info(create_sql)
        create_result = self.sh.execut_db_sql(create_sql,
                                              sql_type=self.connect_sys)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step6.2:修改com_user2为com_user1的间接成员; expect:修改成功----'
        self.log.info(step_txt)
        grant_sql = f"revoke {self.com_user2} from {self.com_user1};" \
            f"grant {self.com_user1} to {self.com_user3};" \
            f"grant {self.com_user3} to {self.com_user2};\du;"
        grant_result = self.sh.execut_db_sql(grant_sql,
                                             sql_type=self.connect_sys)
        self.log.info(grant_result)
        self.assertIn(self.grant_success, grant_result, "执行失败" + step_txt)

        step_txt = '----step6.3:普通用户com_user2修改其所有者表空间的所有者为com_user1; ' \
                   'expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"owner to {self.com_user1};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com2)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        self.assertEqual(owner1, com1_id, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.com_user1} cascade; " \
            f"drop user if exists {self.com_user2} cascade; " \
            f"drop user if exists {self.com_user3} cascade; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(4, drop_user, "执行失败" + step1_txt)
        self.assertEqual(1, drop_tbspc, "执行失败" + step1_txt)
