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
Case Name   : 缺省及指定不同用户为所有者创建表空间，表空间所有者正确
Description :
    1、创建系统管理员用户和普通用户
    2、指定不存在用户为所有者创建tablespace
    3、缺省所有者创建tablespace
    4、指定非当前用户为所有者创建tablespace
Expect      :
    1、创建系统管理员用户和普通用户成功
    2、指定不存在用户为所有者创建tablespace，创建失败
    3、缺省所有者创建tablespace，所有者为当前用户
    4、指定非当前用户为所有者创建tablespace，所有者为指定用户
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
        self.tbspc_name1 = 'tsp_tbspc0015_1'
        self.tbspc_location1 = 'tbspc0015_location_1'
        self.tbspc_name2 = 'tsp_tbspc0015_2'
        self.tbspc_location2 = 'tbspc0015_location_2'
        self.pwd = macro.PASSWD_INITIAL
        self.common_user = 'u_tbspc0015_1'
        self.sys_user = 'u_tbspc0015_2'
        self.none_user = 'u_tbspc0015_3'
        self.comm_connect = f'-U {self.common_user} -W {self.pwd}'
        self.sys_connect = f'-U {self.sys_user} -W {self.pwd}'

    def test_main(self):
        step_txt = '----step1:创建系统管理员用户和普通用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2};" \
            f"drop user if exists {self.common_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"drop user if exists {self.none_user} cascade; " \
            f"create user {self.common_user} password '{self.pwd}';" \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step2:指定不存在用户为所有者创建tablespace; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"owner {self.none_user} " \
            f"relative location '{self.tbspc_location1}';"
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        err_flag = f'ERROR:  role "{self.none_user}" does not exist'
        self.assertIn(err_flag, create_result, "执行失败" + step_txt)

        step_txt = '----step3:缺省所有者创建tablespace; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}';"
        create_result2 = self.sh.execut_db_sql(create_sql,
                                               sql_type=self.sys_connect)
        self.log.info(create_result2)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result2,
                      "执行失败" + step_txt)

        self.log.info('--查询tablespace所有者id--')
        select_sql = f"select spcowner from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        owner1 = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info('tablespace所有者id:' + owner1)
        self.log.info('--查询创建用户id--')
        select_sql = f"select usesysid from pg_user where " \
            f"usename='{self.sys_user}';"
        owner2 = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info('创建用户id:' + owner2)
        self.assertEqual(owner1, owner2, "执行失败" + step_txt)

        step_txt = '----step4:指定非当前用户为所有者创建tablespace; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name2} " \
            f"owner {self.common_user} " \
            f"relative location '{self.tbspc_location2}';"
        create_result2 = self.sh.execut_db_sql(create_sql,
                                               sql_type=self.sys_connect)
        self.log.info(create_result2)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result2)

        self.log.info('--查询tablespace所有者--')
        select_sql = f"select spcowner from pg_tablespace where " \
            f"spcname = '{self.tbspc_name2}';"
        owner1 = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info('tablespace所有者id:' + owner1)
        select_sql = f"select usesysid from pg_user where " \
            f"usename='{self.common_user}';"
        owner2 = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info('创建用户id:' + owner2)
        self.assertEqual(owner1, owner2, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2};" \
            f"drop user if exists {self.common_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(2, drop_user, "执行失败" + step_txt)
        self.assertEqual(2, drop_tbspc, "执行失败" + step_txt)
