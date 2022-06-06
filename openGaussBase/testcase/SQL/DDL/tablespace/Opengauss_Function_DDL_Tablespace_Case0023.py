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
Case Name   : 表空间修改-用户修改权限限制
Description :
    1、系统管理员用户创建tablespace
    2、系统管理员修改本用户所有者的表空间限额
    3、普通用户修改非本用户所有者的表空间限额
    4、普通用户修改非本用户所有者表空间，new_owner与old_owner不一致
    5、普通用户修改非本用户所有者表空间，new_owner与old_owner一致
    6、系统用户修改本用户所有者表空间，new_owner与old_owner不一致
    7、系统管理员修改非本用户所有者的表空间限额
    8、普通用户修改本用户所有者的表空间
Expect      :
    1、系统管理员用户创建tablespace，创建成功，表空间所有者正确
    2、系统管理员修改本用户所有者的表空间限额，修改成功
    3、普通用户修改非本用户所有者的表空间限额，修改失败
    4、普通用户修改非本用户所有者表空间，new_owner与old_owner不一致，修改失败
    5、普通用户修改非本用户所有者表空间，new_owner与old_owner一致，修改成功
    6、系统用户修改本用户所有者表空间，new_owner与old_owner不一致，修改成功
    7、系统管理员修改非本用户所有者的表空间限额，修改成功
    8、普通用户修改本用户所有者的表空间，修改成功
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
        self.tbspc_name = 'tsp_tbspc0023'
        self.tbspc_location = 'tbspc0023'
        self.common_user = 'u_tbspc0023_1'
        self.sys_user = 'u_tbspc0023_2'
        self.pwd = macro.PASSWD_INITIAL
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.connect_com = f'-U {self.common_user} -W {self.pwd}'
        self.err_flag1 = 'ERROR:  permission denied'
        self.err_flag2 = 'ERROR:  must be owner of tablespace'

    def test_main(self):
        step_txt = '----step0:创建系统管理员/普通用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name}; " \
            f"drop user if exists {self.common_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.common_user} password '{self.pwd}';" \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        self.log.info(create_sql)
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        self.log.info('--查询系统管理员id--')
        select_sql = f"select usesysid from pg_user where " \
            f"usename= '{self.sys_user}';"
        sys_id = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info('系统管理员id' + sys_id)
        self.log.info('--查询普通用户id--')
        select_sql = f"select usesysid from pg_user where " \
            f"usename= '{self.common_user}';"
        com_id = self.sh.execut_db_sql(select_sql).splitlines()[-2].strip()
        self.log.info('普通用户id' + com_id)

        check_maxsize = f"select spcmaxsize from pg_tablespace where " \
            f"spcname = '{self.tbspc_name}';"
        check_owner = f"select spcowner from pg_tablespace where " \
            f"spcname = '{self.tbspc_name}';"

        step_txt = '----step1:系统管理员用户创建tablespace; expect:创建成功，表空间所有者正确----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name} " \
            f"relative location '{self.tbspc_location}';"
        create_result = self.sh.execut_db_sql(create_sql,
                                              sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        self.assertEqual(owner1, sys_id, "执行失败" + step_txt)

        step_txt = '----step2:系统管理员修改本用户所有者的表空间限额; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"resize maxsize '10M';"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置限额大小--')
        size = self.sh.execut_db_sql(check_maxsize).splitlines()[-2].strip()
        self.log.info(size)
        self.assertIn(str(10 * 1024), size, "执行失败" + step_txt)

        step_txt = '----step3:普通用户修改非本用户所有者的表空间限额; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"resize maxsize '20M';"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com)
        self.log.info(alter_result)
        self.assertIn(self.err_flag1, alter_result, "执行失败" + step_txt)
        self.log.info('--检查tablespace设置限额大小--')
        size = self.sh.execut_db_sql(check_maxsize).splitlines()[-2].strip()
        self.log.info(size)
        self.assertNotIn(str(20 * 1024), size, "执行失败" + step_txt)

        step_txt = '----step4:普通用户修改非本用户所有者表空间new_owner与old_owner不一致; ' \
                   'expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"owner to {self.common_user};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com)
        self.log.info(alter_result)
        self.assertIn(self.err_flag2, alter_result, "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        self.assertNotEqual(owner1, com_id, "执行失败" + step_txt)

        step_txt = '----step5:普通用户修改非本用户所有者表空间new_owner与old_owner一致; ' \
                   'expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"owner to {self.sys_user};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        self.assertEqual(owner1, sys_id, "执行失败" + step_txt)

        step_txt = '----step6:系统用户修改本用户所有者表空间，new_owner与old_owner不一致 ' \
                   'expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"owner to {self.common_user};"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace所有者--')
        owner1 = self.sh.execut_db_sql(check_owner).splitlines()[-2].strip()
        self.log.info(owner1)
        self.assertEqual(owner1, com_id, "执行失败" + step_txt)

        step_txt = '----step7:系统管理员修改非本用户所有者的表空间限额 expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"resize maxsize '30M';"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置限额大小--')
        size = self.sh.execut_db_sql(check_maxsize).splitlines()[-2].strip()
        self.log.info(size)
        self.assertIn(str(30 * 1024), size, "执行失败" + step_txt)

        step_txt = '----step8:普通用户修改本用户所有者的表空间 expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"resize maxsize '40M';"
        alter_result = self.sh.execut_db_sql(alter_sql,
                                             sql_type=self.connect_com)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置限额大小--')
        size = self.sh.execut_db_sql(check_maxsize).splitlines()[-2].strip()
        self.log.info(size)
        self.assertIn(str(40 * 1024), size, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name}; " \
            f"drop user if exists {self.common_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(2, drop_user, "执行失败" + step1_txt)
        self.assertEqual(1, drop_tbspc, "执行失败" + step1_txt)
