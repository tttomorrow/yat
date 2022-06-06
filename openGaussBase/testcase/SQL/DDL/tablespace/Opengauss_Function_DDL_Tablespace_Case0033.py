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
Case Name   : 表空间删除-删除用户与owner存在成员关系
Description :
    0.创建系统用户及普通用户A;
    1.创建tablespace1，指定普通用户A为所有者;
    2.创建普通用户B;
    3.修改A为B的直接成员;
    4.B用户删除表空间;
    5.修改B为A的直接成员;
    6.B用户删除表空间;
    7.删除不存在的表空间;
Expect      :
    0.创建系统用户及普通用户A; 创建成功
    1.创建tablespace1，指定普通用户A为所有者; 创建成功
    2.创建普通用户B; 创建成功
    3.修改A为B的直接成员; 修改成功
    4.B用户删除表空间; 删除失败
    5.修改B为A的直接成员; 修改成功
    6.B用户删除表空间; 删除成功
    7.删除不存在的表空间; 删除成功
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
        self.tbspc_name = 'tsp_tbspc0033'
        self.tbspc_location = 'tbspc0033'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0033_sys'
        self.com_user1 = 'u_tbspc0033_com1'
        self.com_user2 = 'u_tbspc0033_com2'
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.connect_com1 = f'-U {self.com_user1} -W {self.pwd}'
        self.connect_com2 = f'-U {self.com_user2} -W {self.pwd}'
        self.grant_success = 'GRANT ROLE'
        self.err_flag1 = 'ERROR:  permission denied for tablespace'
        self.err_flag2 = f'ERROR:  Tablespace "{self.tbspc_name}" ' \
            f'does not exist.'

    def test_main(self):
        step_txt = '----step0:创建系统用户及普通用户A; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name}; " \
            f"drop user if exists {self.com_user1} cascade; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.com_user1} password '{self.pwd}';" \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step1:创建tablespace1，指定普通用户A为所有者; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name} " \
            f"owner {self.com_user1} " \
            f"relative location '{self.tbspc_location}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        check_owner = f"select spcowner from pg_tablespace where " \
            f"spcname = '{self.tbspc_name}';"
        owner1 = self.pri_sh.execut_db_sql(check_owner).splitlines()[-2]
        self.log.info(owner1)
        select_sql = f"select usesysid from pg_user where " \
            f"usename= '{self.com_user1}';"
        owner2 = self.pri_sh.execut_db_sql(select_sql).splitlines()[-2]
        self.log.info(owner2)
        self.assertEqual(owner1, owner2, "执行失败" + step_txt)

        step_txt = '----step2:创建普通用户B; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop user if exists {self.com_user2} cascade; " \
            f"create user {self.com_user2} password '{self.pwd}';"
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:修改A为B的直接成员; expect:修改成功----'
        self.log.info(step_txt)
        grant_sql = f"revoke {self.com_user2} from {self.com_user1};" \
            f"grant {self.com_user2} to {self.com_user1};\du;"
        grant_result = self.pri_sh.execut_db_sql(grant_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(grant_result)
        self.assertIn(self.grant_success, grant_result, "执行失败" + step_txt)

        step_txt = '----step4:B用户删除表空间; expect:删除失败----'
        self.log.info(step_txt)
        drop_sql = f"drop tablespace {self.tbspc_name} ;"
        drop_result = self.pri_sh.execut_db_sql(drop_sql,
                                                sql_type=self.connect_com2)
        self.log.info(drop_result)
        self.assertIn(self.err_flag1, drop_result, "执行失败" + step_txt)

        step_txt = '----step5:修改B为A的直接成员; expect:修改成功----'
        self.log.info(step_txt)
        grant_sql = f"revoke {self.com_user2} from {self.com_user1};" \
            f"grant {self.com_user1} to {self.com_user2};\du;"
        grant_result = self.pri_sh.execut_db_sql(grant_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(grant_result)
        self.assertIn(self.grant_success, grant_result, "执行失败" + step_txt)

        step_txt = '----step6:B用户删除表空间; expect:删除成功----'
        self.log.info(step_txt)
        drop_sql = f"drop tablespace {self.tbspc_name} ;"
        drop_result = self.pri_sh.execut_db_sql(drop_sql,
                                                sql_type=self.connect_com2)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt)

        step_txt = '----step7:删除不存在的表空间; expect:删除成功----'
        self.log.info(step_txt)
        drop_result = self.pri_sh.execut_db_sql(drop_sql,
                                                sql_type=self.connect_com1)
        self.log.info(drop_result)
        self.assertIn(self.err_flag2, drop_result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name}; " \
            f"drop user if exists {self.com_user1} cascade; " \
            f"drop user if exists {self.com_user2} cascade; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(3, drop_user, "执行失败" + step1_txt)
        self.assertEqual(1, drop_tbspc, "执行失败" + step1_txt)
